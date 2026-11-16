"""Gaussian-splat objects inside the MuJoCo scene (CPU, torch).

MuJoCo can't draw splats, so the sim renders RGB + depth as usual and each object
splat (tools/crop_object_splat.py output: metres, origin at the centre of the base,
z up) is rasterised from the same camera at its body's current pose, depth-tested
against MuJoCo's depth, and composited on top. The object's MuJoCo geoms stay for
physics and are hidden from the render (geom group HIDDEN_GROUP).

    from rebot_sim import RealSetupEnv
    from rebot_sim.splat_render import SplatObject, SplatCompositor
    env = RealSetupEnv(cfg)                      # cfg has the proxy objects
    comp = SplatCompositor(env, {"towel": SplatObject.load("splats/towel_object.ply")})
    img = comp.render("cam_corner")

Rasterisation follows 3DGS (EWA projection with a 0.3 px blur, SH up to degree 3,
front-to-back alpha blending); it's slow-ish on CPU (about a second per object at
1080p) but needs no GPU.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import mujoco
import numpy as np
import torch

HIDDEN_GROUP = 3

_C0 = 0.28209479177387814
_C1 = 0.4886025119029199
_C2 = (1.0925484305920792, -1.0925484305920792, 0.31539156525252005,
       -1.0925484305920792, 0.5462742152960396)
_C3 = (-0.5900435899266435, 2.890611442640554, -0.4570457994644658, 0.3731763325901154,
       -0.4570457994644658, 1.445305721320277, -0.5900435899266435)


def read_ply(path) -> np.ndarray:
    types = {"float": "f4", "double": "f8", "uchar": "u1", "int": "i4", "uint": "u4",
             "short": "i2"}
    with open(path, "rb") as f:
        header = []
        while (line := f.readline().decode("ascii").strip()) != "end_header":
            header.append(line)
        n = next(int(h.split()[2]) for h in header if h.startswith("element vertex"))
        props = [(h.split()[2], "<" + types[h.split()[1]])
                 for h in header if h.startswith("property")]
        return np.fromfile(f, dtype=np.dtype(props), count=n)


def _quat_to_mat(q):
    q = q / q.norm(dim=1, keepdim=True)
    w, x, y, z = q.unbind(1)
    return torch.stack([
        1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y),
        2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x),
        2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)], 1).view(-1, 3, 3)


def _sh_color(dc, rest, d):
    """3DGS colour from SH (dc: N x 3, rest: N x K x 3) for unit view dirs d (N x 3)."""
    x, y, z = d.unbind(1)
    c = _C0 * dc
    k = rest.shape[1]
    if k >= 3:
        c = c - _C1 * y[:, None] * rest[:, 0] + _C1 * z[:, None] * rest[:, 1] \
            - _C1 * x[:, None] * rest[:, 2]
    if k >= 8:
        xx, yy, zz = x * x, y * y, z * z
        b = [_C2[0] * x * y, _C2[1] * y * z, _C2[2] * (2 * zz - xx - yy), _C2[3] * x * z,
             _C2[4] * (xx - yy)]
        for i, bi in enumerate(b):
            c = c + bi[:, None] * rest[:, 3 + i]
    if k >= 15:
        b = [_C3[0] * y * (3 * xx - yy), _C3[1] * x * y * z, _C3[2] * y * (4 * zz - xx - yy),
             _C3[3] * z * (2 * zz - 3 * xx - 3 * yy), _C3[4] * x * (4 * zz - xx - yy),
             _C3[5] * z * (xx - yy), _C3[6] * x * (xx - 3 * yy)]
        for i, bi in enumerate(b):
            c = c + bi[:, None] * rest[:, 8 + i]
    return (c + 0.5).clamp(min=0.0)


@dataclass
class SplatObject:
    """Gaussians in the object's frame (metres)."""
    means: torch.Tensor      # N x 3
    cov: torch.Tensor        # N x 3 x 3
    opacity: torch.Tensor    # N
    dc: torch.Tensor         # N x 3
    rest: torch.Tensor       # N x K x 3

    @classmethod
    def load(cls, path: Path | str, min_opacity: float = 0.02) -> "SplatObject":
        v = read_ply(path)
        f = lambda *ks: torch.from_numpy(np.stack([v[k] for k in ks], 1).astype(np.float32))
        op = torch.sigmoid(f("opacity")[:, 0])
        keep = op > min_opacity
        scale = torch.exp(f("scale_0", "scale_1", "scale_2"))[keep]
        R = _quat_to_mat(f("rot_0", "rot_1", "rot_2", "rot_3")[keep])
        cov = R @ torch.diag_embed(scale ** 2) @ R.transpose(1, 2)
        rest_keys = sorted((k for k in v.dtype.names if k.startswith("f_rest_")),
                           key=lambda k: int(k.split("_")[-1]))
        m = len(rest_keys) // 3
        rest = f(*rest_keys).view(-1, 3, m).transpose(1, 2) if m else torch.zeros(len(v), 0, 3)
        return cls(f("x", "y", "z")[keep], cov, op[keep], f("f_dc_0", "f_dc_1", "f_dc_2")[keep],
                   rest[keep])


class SplatCompositor:
    """Renders an env's camera with splat objects drawn on their bodies."""

    def __init__(self, env, splats: dict[str, SplatObject], depth_eps: float = 0.004):
        self.env, self.splats, self.eps = env, splats, depth_eps
        m = env.model
        for name in splats:  # hide the proxy geoms; physics is unchanged
            bid = m.body(name).id
            m.geom_group[m.geom_bodyid == bid] = HIDDEN_GROUP
        self.opt = mujoco.MjvOption()
        self.opt.geomgroup[HIDDEN_GROUP] = 0
        self._r: dict[tuple[int, int], mujoco.Renderer] = {}

    def _renderer(self, w, h):
        if (w, h) not in self._r:
            self._r[(w, h)] = mujoco.Renderer(self.env.model, height=h, width=w)
        return self._r[(w, h)]

    def render(self, camera: str = "cam_corner", width: int | None = None,
               height: int | None = None, splats: bool = True,
               proxies: bool = False) -> np.ndarray:
        """`splats=False, proxies=True` shows the physics shapes instead."""
        env = self.env
        if width is None or height is None:
            width, height = env.info.camera_resolutions.get(camera, (640, 480))
        r = self._renderer(width, height)
        opt = self.opt
        if proxies:
            opt = mujoco.MjvOption()
            opt.geomgroup[HIDDEN_GROUP] = 1
        r.update_scene(env.data, camera=camera, scene_option=opt)
        rgb = r.render().astype(np.float32) / 255
        if not splats or not self.splats:
            return (rgb * 255).astype(np.uint8)
        r.enable_depth_rendering()
        r.update_scene(env.data, camera=camera, scene_option=self.opt)
        depth = r.render().copy()
        r.disable_depth_rendering()

        cam = env.model.camera(camera).id
        pc = torch.tensor(env.data.cam_xpos[cam], dtype=torch.float32)
        Rc = torch.tensor(env.data.cam_xmat[cam].reshape(3, 3), dtype=torch.float32)
        # world -> OpenCV camera (x right, y down, z forward); MuJoCo cams look along -z
        W = (Rc @ torch.diag(torch.tensor([1.0, -1.0, -1.0]))).T
        fy = 0.5 * height / np.tan(np.radians(env.model.cam_fovy[cam]) / 2)
        K = (fy, fy, width / 2, height / 2)

        layers = []
        for name, s in self.splats.items():
            b = env.data.body(name)
            Rb = torch.tensor(b.xmat.reshape(3, 3), dtype=torch.float32)
            pb = torch.tensor(b.xpos, dtype=torch.float32)
            mw = s.means @ Rb.T + pb
            d_obj = (mw - pc) @ Rb  # view direction in the object's frame (for SH)
            d_obj = d_obj / d_obj.norm(dim=1, keepdim=True)
            layers.append((mw, Rb @ s.cov @ Rb.T, s.opacity, _sh_color(s.dc, s.rest, d_obj)))
        mw, cov, op, col = (torch.cat(t) for t in zip(*layers))
        out, T = _rasterise(mw, cov, op, col, W, pc, K, width, height,
                            torch.from_numpy(depth) + self.eps)
        img = out + T[..., None] * torch.from_numpy(rgb)
        return (img.clamp(0, 1).numpy() * 255).astype(np.uint8)

    def close(self):
        for r in self._r.values():
            r.close()
        self._r.clear()


def _rasterise(mw, cov, op, col, W, pc, K, width, height, zbuf, chunk=256):
    fx, fy, cx, cy = K
    pcam = (mw - pc) @ W.T
    z = pcam[:, 2]
    ok = z > 0.02
    pcam, cov, op, col, z = pcam[ok], cov[ok], op[ok], col[ok], z[ok]
    x, y = pcam[:, 0], pcam[:, 1]
    u, v = fx * x / z + cx, fy * y / z + cy
    J = torch.zeros(len(z), 2, 3)
    J[:, 0, 0], J[:, 0, 2] = fx / z, -fx * x / (z * z)
    J[:, 1, 1], J[:, 1, 2] = fy / z, -fy * y / (z * z)
    M = J @ W
    c2 = M @ cov @ M.transpose(1, 2) + 0.3 * torch.eye(2)
    det = c2[:, 0, 0] * c2[:, 1, 1] - c2[:, 0, 1] ** 2
    inv = torch.stack([c2[:, 1, 1], -c2[:, 0, 1], c2[:, 0, 0]], 1) / det[:, None]
    mid = 0.5 * (c2[:, 0, 0] + c2[:, 1, 1])
    rad = 3 * torch.sqrt(mid + torch.sqrt((mid * mid - det).clamp(min=0.1)))
    vis = (det > 0) & (u + rad > 0) & (u - rad < width) & (v + rad > 0) & (v - rad < height)
    idx = torch.nonzero(vis)[:, 0]
    idx = idx[torch.argsort(z[idx])]
    out = torch.zeros(height, width, 3)
    T = torch.ones(height, width)
    if len(idx) == 0:
        return out, T
    # only the pixels the splats can touch
    x0 = int((u[idx] - rad[idx]).min().clamp(0, width - 1))
    x1 = int((u[idx] + rad[idx]).max().clamp(0, width - 1)) + 1
    y0 = int((v[idx] - rad[idx]).min().clamp(0, height - 1))
    y1 = int((v[idx] + rad[idx]).max().clamp(0, height - 1)) + 1
    gy, gx = torch.meshgrid(torch.arange(y0, y1, dtype=torch.float32) + 0.5,
                            torch.arange(x0, x1, dtype=torch.float32) + 0.5, indexing="ij")
    px, py = gx.reshape(-1), gy.reshape(-1)
    zb = zbuf[y0:y1, x0:x1].reshape(-1)
    acc = torch.zeros(len(px), 3)
    Tp = torch.ones(len(px))
    for s in range(0, len(idx), chunk):
        i = idx[s:s + chunk]
        # each chunk only touches its own bounding box
        bx0 = (u[i] - rad[i]).min() - x0
        bx1 = (u[i] + rad[i]).max() - x0
        by0 = (v[i] - rad[i]).min() - y0
        by1 = (v[i] + rad[i]).max() - y0
        w_ = x1 - x0
        cols = torch.arange(max(0, int(bx0)), min(w_, int(bx1) + 1))
        rows = torch.arange(max(0, int(by0)), min(y1 - y0, int(by1) + 1))
        if len(cols) == 0 or len(rows) == 0:
            continue
        pix = (rows[:, None] * w_ + cols[None, :]).reshape(-1)
        live = pix[Tp[pix] > 1e-3]
        if len(live) == 0:
            continue
        dx = px[live][None, :] - u[i][:, None]
        dy = py[live][None, :] - v[i][:, None]
        a, b_, c = inv[i, 0:1], inv[i, 1:2], inv[i, 2:3]
        power = -0.5 * (a * dx * dx + c * dy * dy) - b_ * dx * dy
        alpha = (op[i][:, None] * torch.exp(power.clamp(max=0))).clamp(max=0.99)
        alpha = torch.where((alpha > 1 / 255) & (z[i][:, None] < zb[live][None, :]), alpha,
                            torch.zeros(()))
        trans = torch.cumprod(torch.cat([torch.ones(1, len(live)), 1 - alpha[:-1]]), 0)
        wgt = alpha * trans * Tp[live][None, :]
        acc[live] += wgt.T @ col[i]
        Tp[live] = Tp[live] * trans[-1] * (1 - alpha[-1])
    out[y0:y1, x0:x1] = acc.view(y1 - y0, x1 - x0, 3)
    T[y0:y1, x0:x1] = Tp.view(y1 - y0, x1 - x0)
    return out, T
