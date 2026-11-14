#!/usr/bin/env python3
"""Build the hub, fit matrix, per-track shortlists and developer cheat sheet for the
Leukerbad hackathon knowledge base from the frontmatter/content of the company docs.

Usage: build_kb.py <DocsPipline root> [--check] [--fix-images] [--final]
  --check       report broken relative links / image embeds / missing docs
  --fix-images  remove image-embed lines whose file is missing, drop non-image files in assets/,
                downscale very large pictures (only run when image agents are finished)
"""
import datetime
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(sys.argv[1])
FLAGS = set(sys.argv[2:])
COMP = os.path.join(ROOT, "Companies")
CHAL = os.path.join(ROOT, "Challenges")
NOW = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
TODAY = datetime.date.today().isoformat()

TRACKS = [
    ("T01", "T01-Autonomous-Urban-Services", "Autonomous Urban Services", "🏙️",
     "Robots that move, deliver and maintain the city."),
    ("T02", "T02-Resilient-and-Safe-City", "Resilient & Safe City", "🛡️",
     "Systems that respond, protect and keep infrastructure running."),
    ("T03", "T03-Sustainable-City", "Sustainable City", "🌱",
     "Automation for lower emissions, less waste, smarter resources."),
    ("T04", "T04-Elderly-Care-and-Rehabilitation", "Elderly Care & Rehabilitation", "❤️",
     "Assistive robotics for independence, recovery and care."),
]

COMPANIES = [
    ("AGIBOT", "AGIBOT", "https://www.linkedin.com/company/agibotofficial/"),
    ("Binabik-AI", "Binabik AI", "https://www.linkedin.com/company/binabik/"),
    ("coprod", "coprod Inc.", "https://www.linkedin.com/company/coprod-inc/"),
    ("D-Robotics", "D-Robotics", "https://www.linkedin.com/company/d-robotics/"),
    ("Dobot", "Dobot Robotics", "https://www.linkedin.com/company/dobotrobotics/"),
    ("Flexiv", "Flexiv Robotics", "https://www.linkedin.com/company/flexiv-robotics/"),
    ("Galaxea", "Galaxea", "https://www.linkedin.com/company/galaxeadynamics/"),
    ("Galbot", "Galbot", "https://www.linkedin.com/company/galbot-robotics/"),
    ("Genisom-AI", "Genisom AI", "https://www.linkedin.com/company/genisomai/"),
    ("Leadshine", "Leadshine Technology", "https://www.linkedin.com/company/leadshine-technology-co.-ltd./"),
    ("Magiclab", "Magiclab Robotics", "https://www.linkedin.com/company/magiclabrobotics/"),
    ("Omnicor-AI", "Omnicor AI", "https://www.linkedin.com/company/omnicor-ai/"),
    ("OriginFlow", "OriginFlow", "https://www.linkedin.com/company/originflow/"),
    ("ROKAE", "ROKAE Robotics", "https://www.linkedin.com/company/rokae-robotics/"),
    ("SKYLANDX", "SKYLANDX", "https://www.linkedin.com/company/skylandx/"),
    ("Spirit-AI", "Spirit AI", "https://www.linkedin.com/company/spiritai-robotics/"),
    ("Unitree", "Unitree Robotics", "https://www.linkedin.com/company/unitreerobotics/"),
    ("UniX-AI", "UniX AI", "https://www.linkedin.com/company/unix-ai/"),
    ("WUJI", "WUJI", "https://www.linkedin.com/company/wuji-tech/"),
    ("XREAL", "XREAL", "https://www.linkedin.com/company/xreal-com/"),
]

CATEGORY_LABELS = [
    ("humanoid", "Humanoids"),
    ("mobile-manipulator", "Wheeled dual-arm / mobile manipulators"),
    ("quadruped", "Quadrupeds"),
    ("arm", "Robotic arms and cobots"),
    ("dexterous-hand", "Dexterous hands"),
    ("xr", "XR / spatial interfaces"),
    ("sensors", "Sensors and 3D scanning"),
    ("compute", "Edge compute"),
    ("components", "Actuators and motion components"),
    ("software", "Software / AI platforms"),
    ("data", "Data capture"),
]


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def size(path):
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def frontmatter(text):
    out = {}
    if not text.startswith("---"):
        return out
    parts = text.split("\n")
    for line in parts[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            out[key] = [v.strip().strip("\"'") for v in val[1:-1].split(",") if v.strip()]
        else:
            out[key] = val.strip("\"'")
    return out


def num(val):
    if val is None:
        return None
    m = re.search(r"\d+(?:\.\d+)?", str(val))
    if not m:
        return None
    v = float(m.group(0))
    if v > 5:
        return None
    return int(v) if v == int(v) else v


def cell(text, limit=220):
    """Make text safe for a markdown table cell."""
    t = re.sub(r"\s+", " ", (text or "")).strip().replace("|", "/")
    if len(t) > limit:
        t = t[: limit - 1].rstrip() + "…"
    return t


def dot(fit):
    if fit is None:
        return "·"
    if fit >= 4:
        return "🟢"
    if fit >= 3:
        return "🟡"
    if fit >= 2:
        return "🟠"
    return "🔴"


def profile_path(slug):
    return os.path.join(COMP, slug, slug + ".md")


def brief_path(slug, code, folder):
    return os.path.join(COMP, slug, folder, "%s-%s-1-Brief.md" % (slug, code))


def expected_docs(slug):
    docs = [profile_path(slug)]
    for suffix in ("Products", "Developer-Guide", "Roadmap-and-Strategy", "Solutions-and-Projects", "Papers-and-Research"):
        docs.append(os.path.join(COMP, slug, "%s-%s.md" % (slug, suffix)))
    for code, folder, _t, _e, _g in TRACKS:
        for suffix in ("1-Brief", "2-Products-and-Solutions", "3-Playbook", "4-Solutions-Register-and-Papers"):
            docs.append(os.path.join(COMP, slug, folder, "%s-%s-%s.md" % (slug, code, suffix)))
    return docs


def one_liner(text):
    m = re.search(r"\*\*One-liner:\*\*\s*(.+)", text)
    return m.group(1).strip() if m else ""


def brief_info(slug, code, folder):
    path = brief_path(slug, code, folder)
    text = read(path)
    info = {"exists": size(path) > 400, "fit": None, "verdict": "", "rows": {}}
    if not text:
        return info
    fm = frontmatter(text)
    info["fit"] = num(fm.get("fit"))
    m = re.search(r"\*\*Fit:?\s*([0-9.]+)\s*/\s*5\s*\*\*\s*[—–\-:]*\s*(.*)", text)
    if m:
        if info["fit"] is None:
            info["fit"] = num(m.group(1))
        info["verdict"] = m.group(2).strip()
    for line in text.split("\n"):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        label = re.sub(r"[*_`]", "", cells[0]).lower()
        value = " / ".join(cells[1:]).strip()
        for key, needle in (("best", "best hardware"), ("proof", "strongest proof"),
                            ("demo", "fastest"), ("risk", "biggest risk"), ("pair", "pairs well")):
            if label.startswith(needle) and key not in info["rows"]:
                info["rows"][key] = value
    return info


def collect():
    data = []
    for slug, name, linkedin in COMPANIES:
        ptext = read(profile_path(slug))
        fm = frontmatter(ptext)
        docs = expected_docs(slug)
        have = [d for d in docs if size(d) > 400]
        briefs = {}
        for code, folder, _t, _e, _g in TRACKS:
            b = brief_info(slug, code, folder)
            if b["fit"] is None:
                b["fit"] = num(fm.get("fit_" + code.lower()))
                b["from_profile"] = True
            briefs[code] = b
        assets_dir = os.path.join(COMP, slug, "assets")
        pics = [f for f in os.listdir(assets_dir)] if os.path.isdir(assets_dir) else []
        pics = [f for f in pics if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
        data.append({
            "slug": slug, "name": name, "linkedin": linkedin, "fm": fm,
            "profile": size(profile_path(slug)) > 400, "one_liner": one_liner(ptext),
            "docs_have": len(have), "docs_total": len(docs), "briefs": briefs, "pics": len(pics),
        })
    return data


def rel(path, start=ROOT):
    return os.path.relpath(path, start).replace(os.sep, "/")


def link(label, path, start=ROOT):
    return "[%s](%s)" % (label, rel(path, start))


def exists_link(label, path, start=ROOT, missing="…"):
    return link(label, path, start) if size(path) > 400 else missing


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def build_hub(data):
    n_prof = sum(1 for d in data if d["profile"])
    n_docs = sum(d["docs_have"] for d in data)
    n_total = sum(d["docs_total"] for d in data)
    n_folders = sum(1 for d in data for c in d["briefs"] if d["briefs"][c]["exists"])
    n_pics = sum(d["pics"] for d in data)
    L = []
    L += ["---", "type: hub", "updated: " + TODAY, "tags: [leukerbad-hackathon, hub]", "---",
          "# Leukerbad Robotics Hackathon 2026 — Knowledge Base", "",
          "> **Nov 14 (10:00) – Nov 16 (17:00), 2026 · Sportarena Leukerbad, Römerweg 5 · 4 tracks · 20 hardware and platform companies · CHF 50k prizes**",
          "> Build status (%s): **%d/20** company profiles · **%d/80** track folders started · **%d/%d** docs · **%d** product pictures"
          % (NOW, n_prof, n_folders, n_docs, n_total, n_pics), ""]
    L += ["## 60-second routine when a challenge statement is announced", "",
          "1. Open the **track overview** below and fill in its *Official statement* checklist.",
          "2. Open that track's **hardware shortlist** — every company ranked by fit (0–5) with a one-line verdict.",
          "3. For the top 3–5 companies open their track folder: **Brief** (one screen) → **Playbook** (3–4 build concepts with 48-hour plans) → **Products and solutions** (specs, pictures, proof points).",
          "4. Before committing to hardware, read the company's **Developer guide** → *First 60 minutes checklist*.",
          "5. Ask the vendor engineers the questions listed at the end of each Playbook.", ""]
    L += ["## Tracks", "",
          "| Track | What it is | Overview | Official directions: who has what | Hardware shortlist | Solution patterns | Cross-vendor solutions | Research library | All solutions and projects |",
          "|---|---|---|---|---|---|---|---|---|"]
    for code, folder, title, emoji, tagline in TRACKS:
        base = os.path.join(CHAL, folder)
        L.append("| %s **%s %s** | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            emoji, code, title, tagline,
            exists_link("Overview", os.path.join(base, code + "-0-Track-Overview.md")),
            exists_link("Directions", os.path.join(base, code + "-6-Official-Directions-Who-Has-What.md")),
            exists_link("Shortlist", os.path.join(base, code + "-2-Hardware-Shortlist.md")),
            exists_link("Patterns", os.path.join(base, code + "-1-Solution-Patterns.md")),
            exists_link("Combos", os.path.join(base, code + "-3-Cross-Vendor-Solutions.md")),
            exists_link("Papers", os.path.join(base, code + "-4-Research-Library.md")),
            exists_link("Everything", os.path.join(base, code + "-5-All-Solutions-and-Projects.md"))))
    L += ["", "## Companies × tracks — fit matrix", "",
          "Fit 0–5: 🟢 4–5 strong · 🟡 3 usable / part of a combo · 🟠 2 supporting role · 🔴 0–1 weak. Each score opens that company's track brief.", "",
          "| Company | What they are | Likely on site | T01 Urban | T02 Safe | T03 Sustainable | T04 Care | More |",
          "|---|---|---|---|---|---|---|---|"]
    for d in data:
        slug = d["slug"]
        fits = []
        for code, folder, _t, _e, _g in TRACKS:
            b = d["briefs"][code]
            if b["fit"] is None:
                fits.append("…")
            elif b["exists"]:
                fits.append("%s %s" % (dot(b["fit"]), link(str(b["fit"]), brief_path(slug, code, folder))))
            else:
                fits.append("%s %s" % (dot(b["fit"]), b["fit"]))
        more = " · ".join(x for x in [
            exists_link("Products", os.path.join(COMP, slug, slug + "-Products.md"), missing=""),
            exists_link("Dev guide", os.path.join(COMP, slug, slug + "-Developer-Guide.md"), missing=""),
            exists_link("Roadmap", os.path.join(COMP, slug, slug + "-Roadmap-and-Strategy.md"), missing=""),
            exists_link("Solutions", os.path.join(COMP, slug, slug + "-Solutions-and-Projects.md"), missing=""),
            exists_link("Papers", os.path.join(COMP, slug, slug + "-Papers-and-Research.md"), missing=""),
        ] if x) or "…"
        name = link("**" + d["name"] + "**", profile_path(slug)) if d["profile"] else "**%s** (in progress)" % d["name"]
        L.append("| %s | %s | %s | %s | %s |" % (
            name, cell(d["one_liner"], 170) or "…", cell(d["fm"].get("on_site_guess", ""), 120) or "…",
            " | ".join(fits), more))
    L += ["", "## By hardware class", ""]
    for key, label in CATEGORY_LABELS:
        members = [d for d in data if key in [c.lower() for c in (d["fm"].get("categories") or [])]]
        if members:
            L.append("- **%s:** %s" % (label, " · ".join(link(m["name"], profile_path(m["slug"])) for m in members)))
    L += ["", "## Cross-company pages", "",
          "- %s — how to program each platform (TL;DR per company)" % exists_link("Developer cheat sheet", os.path.join(ROOT, "02-Developer-Cheatsheet.md"), missing="Developer cheat sheet (in progress)"),
          "- %s — public information about the hackathon, organizers, judging and Leukerbad" % exists_link("Event intel", os.path.join(ROOT, "Event", "Event-Intel.md"), missing="Event intel (in progress)"),
          "- [Saved event page](<Leukerbad Robotics Hackathon 2026 · Swiss Alps.html>) (original HTML)",
          "- %s — which docs exist for every company, with counts of pictures, solutions, projects and papers" % exists_link("Coverage audit", os.path.join(ROOT, "01-Coverage-Audit.md"), missing="Coverage audit (in progress)"),
          "- Visual map: open `Hackathon-Map.canvas` in Obsidian; table view: `Companies.base`", ""]
    L += ["## Folder layout", "", "```",
          "DocsPipline/",
          "├── 00-START-HERE.md                 ← this page",
          "├── 02-Developer-Cheatsheet.md",
          "├── Event/Event-Intel.md",
          "├── Challenges/<track>/              ← cross-company view of each track",
          "│   ├── T0x-0-Track-Overview.md      (problem space, archetypes, Leukerbad scenarios, judging)",
          "│   ├── T0x-1-Solution-Patterns.md   (reference architectures, building blocks, idea bank)",
          "│   ├── T0x-2-Hardware-Shortlist.md  (all 20 companies ranked for the track)",
          "│   ├── T0x-3-Cross-Vendor-Solutions.md",
          "│   ├── T0x-4-Research-Library.md    (papers per company relevant to the track)",
          "│   ├── T0x-5-All-Solutions-and-Projects.md (every solution, project and future plan of every company for the track)",
          "│   └── T0x-6-Official-Directions-Who-Has-What.md (the 7 official directions × every company)",
          "└── Companies/<Company>/",
          "    ├── <Company>.md                 (profile, portfolio, fit table, verification log)",
          "    ├── <Company>-Products.md        (full catalogue with specs and pictures)",
          "    ├── <Company>-Developer-Guide.md (SDKs, first-60-minutes checklist, gotchas)",
          "    ├── <Company>-Roadmap-and-Strategy.md",
          "    ├── <Company>-Solutions-and-Projects.md (every solution, past/current project and future plan)",
          "    ├── <Company>-Papers-and-Research.md   (company papers, third-party papers, datasets, models)",
          "    ├── assets/                      (product pictures)",
          "    └── T01…T04-<track>/             ← one folder per challenge",
          "        ├── <Company>-T0x-1-Brief.md                  (one screen: fit, best hardware, fastest demo, risk)",
          "        ├── <Company>-T0x-2-Products-and-Solutions.md (relevant products, what they already do, what is next)",
          "        ├── <Company>-T0x-3-Playbook.md               (3–4 build concepts, 48-h plans, questions to ask)",
          "        └── <Company>-T0x-4-Solutions-Register-and-Papers.md (second pass: complete list of solutions, projects, future plans, papers, pictures)",
          "```", "",
          "Conventions: ✅ shipping · 🧪 announced/preview · 🔭 roadmap · ⚠️ unverified. Every doc ends with its sources; each company profile carries a dated verification log.", ""]
    write(os.path.join(ROOT, "00-START-HERE.md"), "\n".join(L))


def build_shortlists(data):
    for code, folder, title, emoji, tagline in TRACKS:
        base = os.path.join(CHAL, folder)
        rows = []
        for d in data:
            b = d["briefs"][code]
            rows.append((b["fit"] if b["fit"] is not None else -1, d, b))
        rows.sort(key=lambda r: (-r[0], r[1]["name"].lower()))
        L = ["---", "type: track-shortlist", "challenge: " + code, 'challenge_title: "%s"' % title,
             "updated: " + TODAY, "tags: [leukerbad-hackathon, %s, shortlist]" % code.lower(), "---",
             "# %s %s — Hardware Shortlist" % (code, title), "",
             "> %s %s" % (emoji, tagline),
             "> Generated %s from the company briefs (fit 0–5). 🟢 4–5 · 🟡 3 · 🟠 2 · 🔴 0–1" % NOW, "",
             "%s · %s · %s · %s" % (
                 link("Start here", os.path.join(ROOT, "00-START-HERE.md"), base),
                 exists_link("Track overview", os.path.join(base, code + "-0-Track-Overview.md"), base, "Track overview"),
                 exists_link("Solution patterns", os.path.join(base, code + "-1-Solution-Patterns.md"), base, "Solution patterns"),
                 exists_link("Cross-vendor solutions", os.path.join(base, code + "-3-Cross-Vendor-Solutions.md"), base, "Cross-vendor solutions")),
             "", "## Ranking", "",
             "| # | Company | Fit | Verdict | Best hardware | Fastest 48-h demo | Biggest risk | Open |",
             "|---|---|---|---|---|---|---|---|"]
        for i, (fit, d, b) in enumerate(rows, 1):
            slug = d["slug"]
            cdir = os.path.join(COMP, slug, folder)
            opens = " · ".join(x for x in [
                exists_link("Brief", os.path.join(cdir, "%s-%s-1-Brief.md" % (slug, code)), base, ""),
                exists_link("Products", os.path.join(cdir, "%s-%s-2-Products-and-Solutions.md" % (slug, code)), base, ""),
                exists_link("Playbook", os.path.join(cdir, "%s-%s-3-Playbook.md" % (slug, code)), base, ""),
                exists_link("Register", os.path.join(cdir, "%s-%s-4-Solutions-Register-and-Papers.md" % (slug, code)), base, ""),
            ] if x) or "…"
            name = link("**" + d["name"] + "**", profile_path(slug), base) if d["profile"] else "**%s**" % d["name"]
            L.append("| %d | %s | %s %s | %s | %s | %s | %s | %s |" % (
                i, name, dot(b["fit"]), b["fit"] if b["fit"] is not None else "…",
                cell(b["verdict"], 200) or "…", cell(b["rows"].get("best", ""), 160) or "…",
                cell(b["rows"].get("demo", ""), 200) or "…", cell(b["rows"].get("risk", ""), 160) or "…", opens))
        groups = (("Top picks (fit 4–5)", lambda f: f >= 4), ("Usable or part of a combo (fit 3)", lambda f: 3 <= f < 4),
                  ("Supporting roles (fit 2)", lambda f: 2 <= f < 3), ("Weak fit (0–1)", lambda f: 0 <= f < 2))
        for label, test in groups:
            members = [(d, b) for fit, d, b in rows if fit >= 0 and test(fit)]
            if not members:
                continue
            L += ["", "## " + label, ""]
            for d, b in members:
                slug = d["slug"]
                cdir = os.path.join(COMP, slug, folder)
                L.append("- **%s** (%s/5) — %s%s%s" % (
                    d["name"], b["fit"], cell(b["verdict"], 260) or cell(d["one_liner"], 200),
                    (" · proof: " + cell(b["rows"]["proof"], 200)) if b["rows"].get("proof") else "",
                    (" → " + link("Playbook", os.path.join(cdir, "%s-%s-3-Playbook.md" % (slug, code)), base))
                    if size(os.path.join(cdir, "%s-%s-3-Playbook.md" % (slug, code))) > 400 else ""))
        pending = [d["name"] for fit, d, b in rows if fit < 0]
        if pending:
            L += ["", "## Not scored yet", "", "- " + ", ".join(pending)]
        L.append("")
        write(os.path.join(base, code + "-2-Hardware-Shortlist.md"), "\n".join(L))


def section(text, heading_prefix):
    lines = text.split("\n")
    out, on = [], False
    for line in lines:
        if line.startswith("## "):
            if on:
                break
            if line[3:].strip().lower().startswith(heading_prefix.lower()):
                on = True
                continue
        elif on:
            out.append(line)
    return "\n".join(out).strip()


def build_cheatsheet(data):
    L = ["---", "type: dev-cheatsheet", "updated: " + TODAY, "tags: [leukerbad-hackathon, dev-guide]", "---",
         "# Developer cheat sheet — how to program each platform", "",
         "> Generated %s from each company's Developer guide (TL;DR section). Open the full guide for SDK tables, the first-60-minutes checklist and gotchas." % NOW,
         "", link("Start here", os.path.join(ROOT, "00-START-HERE.md")), ""]
    count = 0
    for d in data:
        slug = d["slug"]
        gpath = os.path.join(COMP, slug, slug + "-Developer-Guide.md")
        text = read(gpath)
        if size(gpath) < 400:
            continue
        tl = section(text, "TL;DR")
        if not tl:
            continue
        count += 1
        L += ["## " + d["name"], "", tl, "", "→ " + link("Full developer guide", gpath) + " · " + link("Profile", profile_path(slug)), ""]
    if count:
        write(os.path.join(ROOT, "02-Developer-Cheatsheet.md"), "\n".join(L))
    return count


LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+(?:\s[^)]*)?)\)")


def check(data, fix_images=False):
    broken_links, broken_imgs, files = [], [], 0
    for base, _dirs, names in os.walk(ROOT):
        for n in names:
            if not n.endswith(".md"):
                continue
            path = os.path.join(base, n)
            files += 1
            text = read(path)
            new_lines, changed = [], False
            in_code = False
            for line in text.split("\n"):
                if line.strip().startswith("```"):
                    in_code = not in_code
                drop = False
                if not in_code:
                    for m in LINK_RE.finditer(line):
                        target = m.group(3).strip()
                        if target.startswith("<") and target.endswith(">"):
                            target = target[1:-1]
                        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                            continue
                        target = target.split("#")[0].split(" ")[0] if not m.group(3).strip().startswith("<") else target
                        target = target.replace("%20", " ")
                        if not target:
                            continue
                        full = os.path.normpath(os.path.join(base, target))
                        if not os.path.exists(full):
                            if m.group(1) == "!":
                                broken_imgs.append((rel(path), target))
                                if fix_images and line.strip().startswith("!["):
                                    drop = True
                            else:
                                broken_links.append((rel(path), target))
                if drop:
                    changed = True
                    continue
                new_lines.append(line)
            if changed:
                write(path, "\n".join(new_lines))
    return files, broken_links, broken_imgs


def fix_assets():
    report = {"removed": [], "resized": [], "kept": 0}
    for slug, _n, _l in COMPANIES:
        adir = os.path.join(COMP, slug, "assets")
        if not os.path.isdir(adir):
            continue
        for f in sorted(os.listdir(adir)):
            path = os.path.join(adir, f)
            if f.startswith("."):
                continue
            mime = subprocess.run(["file", "--brief", "--mime-type", path], capture_output=True, text=True).stdout.strip()
            if f.endswith(".orig") or mime not in ("image/jpeg", "image/png", "image/webp", "image/gif"):
                os.remove(path)
                report["removed"].append("%s/%s (%s)" % (slug, f, mime))
                continue
            out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path], capture_output=True, text=True).stdout
            dims = [int(x) for x in re.findall(r"pixel(?:Width|Height):\s*(\d+)", out)]
            if dims and max(dims) > 1800:
                subprocess.run(["sips", "-Z", "1600", path], capture_output=True, text=True)
                report["resized"].append("%s/%s" % (slug, f))
            report["kept"] += 1
    return report


def sections2(text):
    """Ordered (heading, body) pairs of level-2 sections, ignoring fenced code."""
    out, cur, buf, in_code = [], None, [], False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
        if line.startswith("## ") and not in_code:
            if cur is not None:
                out.append((cur, "\n".join(buf).strip()))
            cur, buf = line[3:].strip(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out.append((cur, "\n".join(buf).strip()))
    return out


def find_section(text, *prefixes):
    for head, body in sections2(text):
        h = re.sub(r"[*_`]", "", head).lower()
        for pfx in prefixes:
            if h.startswith(pfx.lower()):
                return body
    return ""


def sub_section(body, prefix):
    """Body of a '### <prefix…>' block inside a level-2 section body."""
    out, on = [], False
    for line in body.split("\n"):
        if line.startswith("### "):
            if on:
                break
            if line[4:].strip().lower().startswith(prefix.lower()):
                on = True
                continue
        elif on:
            out.append(line)
    return "\n".join(out).strip()


def rebase_links(text, src_dir, dst_dir):
    def fix(m):
        bang, label, target = m.group(1), m.group(2), m.group(3).strip()
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#") or target.startswith("<"):
            return m.group(0)
        path, _sep, frag = target.partition("#")
        path = path.split(" ")[0]
        if not path:
            return m.group(0)
        full = os.path.normpath(os.path.join(src_dir, path.replace("%20", " ")))
        new = os.path.relpath(full, dst_dir).replace(os.sep, "/").replace(" ", "%20")
        return "%s[%s](%s%s)" % (bang, label, new, ("#" + frag) if frag else "")
    return LINK_RE.sub(fix, text)


def demote(body):
    out, in_code = [], False
    for line in body.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"^#{2,5} ", line):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def table_rows(body):
    rows = [l for l in body.split("\n") if l.strip().startswith("|")]
    rows = [l for l in rows if not re.match(r"^\s*\|[\s:|-]+\|\s*$", l)]
    return max(0, len(rows) - 1) if rows else 0


def md_tables(body):
    out, lines, i = [], body.split("\n"), 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header, rows, j = split_row(lines[i]), [], i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(lines[j])
                j += 1
            out.append((header, rows))
            i = j
        else:
            i += 1
    return out


def track_rows(body, code, src_dir, dst_dir):
    parts, n = [], 0
    for header, rows in md_tables(body):
        col = next((k for k, h in enumerate(header) if "track" in h.lower()), None)
        if col is None:
            continue
        keep = []
        for r in rows:
            cells = split_row(r)
            if col < len(cells) and code in cells[col]:
                keep.append(rebase_links(r, src_dir, dst_dir))
        if keep:
            n += len(keep)
            parts.append("\n".join(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + keep))
    return "\n\n".join(parts), n


def build_track_compilations(data):
    stats = {}
    for code, folder, title, emoji, tagline in TRACKS:
        base = os.path.join(CHAL, folder)
        nav = "%s · %s · %s" % (
            link("Start here", os.path.join(ROOT, "00-START-HERE.md"), base),
            exists_link("Track overview", os.path.join(base, code + "-0-Track-Overview.md"), base, "Track overview"),
            exists_link("Hardware shortlist", os.path.join(base, code + "-2-Hardware-Shortlist.md"), base, "Hardware shortlist"))
        A = ["---", "type: track-all-solutions", "challenge: " + code, 'challenge_title: "%s"' % title, "updated: " + TODAY,
             "tags: [leukerbad-hackathon, %s, solutions]" % code.lower(), "---",
             "# %s %s — All Solutions, Projects and Plans (every company)" % (code, title), "",
             "> %s %s" % (emoji, tagline),
             "> Compiled %s. Per company: every row of its solutions-and-projects register tagged %s (solutions, projects, future plans) and its quick index; second-pass direction coverage where that has run. Companies without a register show their first-pass findings for this track." % (NOW, code),
             "", nav, "", "## Index", "", "| Company | Fit | Solutions | Projects | Future plans | Source |", "|---|---|---|---|---|---|"]
        P = ["---", "type: track-research-library", "challenge: " + code, 'challenge_title: "%s"' % title, "updated: " + TODAY,
             "tags: [leukerbad-hackathon, %s, papers]" % code.lower(), "---",
             "# %s %s — Research Library" % (code, title), "",
             "> Compiled %s: papers relevant to this track, per company (company-authored and third-party work on their hardware)." % NOW, "", nav, ""]
        ranked = sorted(data, key=lambda d: (-(d["briefs"][code]["fit"] if d["briefs"][code]["fit"] is not None else -1), d["name"].lower()))
        idxA, bodyA, bodyP, nP, nreg, nfirst = [], [], [], 0, 0, 0
        for d in ranked:
            slug = d["slug"]
            cdir = os.path.join(COMP, slug, folder)
            cbase = os.path.join(COMP, slug)
            fit = d["briefs"][code]["fit"]
            spath = os.path.join(cbase, slug + "-Solutions-and-Projects.md")
            stext = read(spath) if size(spath) > 400 else ""
            rpath = os.path.join(cdir, "%s-%s-4-Solutions-Register-and-Papers.md" % (slug, code))
            rtext = read(rpath) if size(rpath) > 400 else ""
            p2 = os.path.join(cdir, "%s-%s-2-Products-and-Solutions.md" % (slug, code))
            links = [x for x in [
                exists_link("Brief", brief_path(slug, code, folder), base, ""),
                exists_link("Playbook", os.path.join(cdir, "%s-%s-3-Playbook.md" % (slug, code)), base, ""),
                exists_link("Products and solutions for " + code, p2, base, ""),
                exists_link("Company solutions register", spath, base, ""),
                exists_link("Second-pass track register", rpath, base, "")] if x]
            block = ["## %s — fit %s/5" % (d["name"], fit if fit is not None else "?"), "", " · ".join(links), ""]
            ns = npj = nf = 0
            if stext:
                nreg += 1
                sol, ns = track_rows(find_section(stext, "solutions catalogue"), code, cbase, base)
                proj, npj = track_rows(find_section(stext, "projects register"), code, cbase, base)
                fut, nf = track_rows(find_section(stext, "future projects"), code, cbase, base)
                quick = sub_section(find_section(stext, "solutions by track"), code)
                for label, body in (("Solutions", sol), ("Projects, deployments and pilots", proj), ("Future projects and plans", fut)):
                    if body:
                        block += ["### " + label, "", body, ""]
                if quick:
                    block += ["### Quick index (from the company register)", "", rebase_links(demote(demote(quick)), cbase, base), ""]
                src = "company register"
            else:
                nfirst += 1
                t2 = read(p2) if size(p2) > 400 else ""
                for head, body in sections2(t2):
                    h = head.lower()
                    if "already does" in h or "building next" in h:
                        block += ["### " + head, "", rebase_links(demote(body), cdir, base), ""]
                src = "first-pass track doc"
            if rtext:
                cov = find_section(rtext, "coverage of the official directions")
                if cov:
                    block += ["### Coverage of the official directions (second pass)", "", rebase_links(cov, cdir, base), ""]
                src += " + second pass"
            idxA.append("| %s | %s | %s | %s | %s | %s |" % (link(d["name"], profile_path(slug), base), fit if fit is not None else "…",
                                                          ns or "–", npj or "–", nf or "–", src))
            bodyA += block
            papers = find_section(rtext, "research papers") if rtext else ""
            ppath = os.path.join(cbase, slug + "-Papers-and-Research.md")
            ptext = read(ppath) if size(ppath) > 400 else ""
            reading = sub_section(find_section(ptext, "reading list"), code) if ptext else ""
            if papers or reading:
                nP += 1
                bodyP += ["## " + d["name"], ""]
                if papers:
                    bodyP += [rebase_links(demote(papers), cdir, base), ""]
                if reading:
                    bodyP += ["**Reading list from the company papers doc:**", "", rebase_links(demote(reading), cbase, base), ""]
                if ptext:
                    bodyP += ["→ " + link("All papers of " + d["name"], ppath, base), ""]
        write(os.path.join(base, code + "-5-All-Solutions-and-Projects.md"), "\n".join(A + idxA + [""] + bodyA))
        if nP:
            write(os.path.join(base, code + "-4-Research-Library.md"), "\n".join(P + bodyP))
        stats[code] = (nreg, nfirst, nP)
    return stats

def count_embeds(path):
    text, base, n = read(path), os.path.dirname(path), 0
    for m in LINK_RE.finditer(text):
        if m.group(1) == "!":
            t = m.group(3).strip().split(" ")[0].replace("%20", " ")
            if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", t) and os.path.exists(os.path.normpath(os.path.join(base, t))):
                n += 1
    return n


def build_audit(data):
    L = ["---", "type: coverage-audit", "updated: " + TODAY, "tags: [leukerbad-hackathon, audit]", "---",
         "# Coverage audit — is everything there for every company?", "",
         "> Generated %s by scanning the folders. ✅ = doc present (more than 1,000 bytes) · ⚠️ = stub · ❌ = missing." % NOW, "",
         link("Start here", os.path.join(ROOT, "00-START-HERE.md")), "",
         "## Company-level docs", "",
         "| Company | Profile | Products | Dev guide | Roadmap | Solutions and projects | Papers | Pictures saved | Solutions listed | Projects (past/current) | Future plans | Papers listed |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]

    def mark(path):
        sz = size(path)
        return "✅" if sz > 1000 else ("⚠️" if sz > 0 else "❌")

    totals = {"ok": 0, "all": 0}
    for d in data:
        slug = d["slug"]
        cd = os.path.join(COMP, slug)
        paths = [profile_path(slug)] + [os.path.join(cd, "%s-%s.md" % (slug, sfx)) for sfx in
                                        ("Products", "Developer-Guide", "Roadmap-and-Strategy", "Solutions-and-Projects", "Papers-and-Research")]
        marks = [mark(p) for p in paths]
        totals["all"] += len(marks)
        totals["ok"] += marks.count("✅")
        stext = read(paths[4])
        ptext = read(paths[5])
        n_sol = table_rows(find_section(stext, "solutions catalogue"))
        n_proj = table_rows(find_section(stext, "projects register"))
        n_fut = table_rows(find_section(stext, "future projects"))
        n_pap = table_rows(find_section(ptext, "company-authored")) + table_rows(find_section(ptext, "third-party"))
        L.append("| %s | %s | %d | %s | %s | %s | %s |" % (
            link(d["name"], profile_path(slug)) if d["profile"] else d["name"], " | ".join(marks), d["pics"],
            n_sol or "–", n_proj or "–", n_fut or "–", n_pap or "–"))
    L += ["", "## Track folders (4 docs each: Brief · Products and solutions · Playbook · Solutions register and papers)", "",
          "| Company | T01 Urban services | T02 Safe city | T03 Sustainable city | T04 Elderly care | Pictures shown in track docs |",
          "|---|---|---|---|---|---|"]
    for d in data:
        slug = d["slug"]
        cells, shown = [], 0
        for code, folder, _t, _e, _g in TRACKS:
            cd = os.path.join(COMP, slug, folder)
            ms = []
            for sfx in ("1-Brief", "2-Products-and-Solutions", "3-Playbook", "4-Solutions-Register-and-Papers"):
                pth = os.path.join(cd, "%s-%s-%s.md" % (slug, code, sfx))
                ms.append(mark(pth))
                shown += count_embeds(pth) if size(pth) else 0
            totals["all"] += 4
            totals["ok"] += ms.count("✅")
            cells.append(" ".join(ms))
        L.append("| %s | %s | %d |" % (d["name"], " | ".join(cells), shown))
    L += ["", "**Total: %d of %d expected docs present.**" % (totals["ok"], totals["all"]), ""]
    write(os.path.join(ROOT, "01-Coverage-Audit.md"), "\n".join(L))
    return totals


def wire_links(data):
    """Final step: make sure first-pass docs link to the second-pass docs."""
    changed = 0
    for d in data:
        slug = d["slug"]
        cd = os.path.join(COMP, slug)
        prof = profile_path(slug)
        text = read(prof)
        extra = []
        for sfx, label in (("Solutions-and-Projects", "Solutions and projects register"), ("Papers-and-Research", "Papers and research")):
            fn = "%s-%s.md" % (slug, sfx)
            if size(os.path.join(cd, fn)) > 400 and ("(" + fn + ")") not in text:
                extra.append("[%s](%s)" % (label, fn))
        if text and extra:
            line = "- " + " · ".join(extra)
            if "\n## Related docs" in text:
                head, sep, tail = text.partition("\n## Related docs")
                first_nl = tail.find("\n")
                tail = tail[: first_nl + 1] + line + "\n" + tail[first_nl + 1:]
                text = head + sep + tail
            else:
                text = text.rstrip("\n") + "\n\n## Related docs\n" + line + "\n"
            write(prof, text)
            changed += 1
        for code, folder, _t, _e, _g in TRACKS:
            td = os.path.join(cd, folder)
            reg = "%s-%s-4-Solutions-Register-and-Papers.md" % (slug, code)
            if size(os.path.join(td, reg)) <= 400:
                continue
            for sfx in ("1-Brief", "2-Products-and-Solutions", "3-Playbook"):
                pth = os.path.join(td, "%s-%s-%s.md" % (slug, code, sfx))
                t = read(pth)
                if not t or ("(" + reg + ")") in t:
                    continue
                lines = t.split("\n")
                for i, ln in enumerate(lines):
                    if ln.lstrip().startswith("⬆"):
                        lines[i] = ln.rstrip() + " · [Solutions register and papers](%s)" % reg
                        break
                else:
                    lines.append("")
                    lines.append("⬆ [Solutions register and papers](%s)" % reg)
                write(pth, "\n".join(lines))
                changed += 1
    return changed


DIRS = {
    "T01": ["Autonomous delivery & urban logistics", "Smart cleaning & facility maintenance", "Public-space service robots",
            "Autonomous urban inspection", "Smart guidance & information services", "Autonomous navigation & path planning",
            "Human-robot interaction in complex cities"],
    "T02": ["Emergency rescue robots", "Autonomous inspection in hazardous environments", "Infrastructure safety monitoring",
            "Disaster response & environment sensing", "Smart security monitoring", "Autonomous navigation in complex terrain",
            "Human-robot collaborative emergency response"],
    "T03": ["Smart waste sorting & collection", "Environmental monitoring robots", "Energy-efficient robotic systems",
            "Sustainable urban infrastructure", "Water & energy management", "Smart recycling & resource optimization",
            "Environmental data collection & analysis"],
    "T04": ["Daily living assistance for seniors", "Smart care robots", "Rehabilitation training robots",
            "Mobility assistance & support", "Human-robot interaction & companionship", "Automation in care scenarios",
            "Smart health monitoring & assistance"],
}


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]


def coverage_rows(rtext, code):
    body = find_section(rtext, "coverage of the official directions")
    rows = {}
    for line in body.split("\n"):
        if not line.strip().startswith("|"):
            continue
        cells = split_row(line)
        m = re.match(r"^(T0\d)\.(\d)\b", re.sub(r"[*_`\"“”]", "", cells[0]).strip())
        if not m or m.group(1) != code:
            continue
        strength = ""
        for c in reversed(cells[1:]):
            syms = [ch for ch in c if ch in "●◐○"]
            if syms:
                strength = syms[0]
                break
        rows[int(m.group(2))] = {
            "what": cells[1] if len(cells) > 1 else "", "evidence": cells[2] if len(cells) > 2 else "",
            "maturity": cells[3] if len(cells) > 3 else "", "strength": strength}
    return rows


def build_direction_pages(data):
    made = 0
    for code, folder, title, emoji, tagline in TRACKS:
        base = os.path.join(CHAL, folder)
        per_company = []
        for d in data:
            slug = d["slug"]
            cdir = os.path.join(COMP, slug, folder)
            rpath = os.path.join(cdir, "%s-%s-4-Solutions-Register-and-Papers.md" % (slug, code))
            if size(rpath) <= 400:
                continue
            rows = coverage_rows(read(rpath), code)
            if rows:
                per_company.append((d, cdir, rpath, rows))
        stale = os.path.join(base, code + "-6-Official-Directions-Who-Has-What.md")
        if len(per_company) < 8:
            if os.path.exists(stale):
                os.remove(stale)
            continue
        made += 1
        dirs = DIRS[code]
        L = ["---", "type: track-directions", "challenge: " + code, 'challenge_title: "%s"' % title, "updated: " + TODAY,
             "tags: [leukerbad-hackathon, %s, directions]" % code.lower(), "---",
             "# %s %s — Official directions: who has what" % (code, title), "",
             "> %s The organizers publish seven example directions for this track. This page pivots every company's second-pass register onto them." % emoji,
             "> Compiled %s from %d of 20 company registers. ● strong · ◐ partial · ○ nothing." % (NOW, len(per_company)), "",
             "%s · %s · %s · %s" % (
                 link("Start here", os.path.join(ROOT, "00-START-HERE.md"), base),
                 exists_link("Track overview", os.path.join(base, code + "-0-Track-Overview.md"), base, "Track overview"),
                 exists_link("Hardware shortlist", os.path.join(base, code + "-2-Hardware-Shortlist.md"), base, "Hardware shortlist"),
                 exists_link("All solutions and projects", os.path.join(base, code + "-5-All-Solutions-and-Projects.md"), base, "All solutions and projects")),
             "", "## Coverage matrix", ""]
        L += ["| # | Direction |", "|---|---|"] + ["| %s.%d | %s |" % (code, i, n) for i, n in enumerate(dirs, 1)] + [""]
        L += ["| Company | Fit | " + " | ".join(".%d" % i for i in range(1, 8)) + " | Strong in |",
              "|---|---|" + "---|" * 7 + "---|"]
        ordered = sorted(per_company, key=lambda t: (-(t[0]["briefs"][code]["fit"] or 0), t[0]["name"].lower()))
        for d, cdir, rpath, rows in ordered:
            syms = [rows.get(i, {}).get("strength") or "·" for i in range(1, 8)]
            L.append("| %s | %s | %s | %d of 7 |" % (
                link(d["name"], rpath, base), d["briefs"][code]["fit"] if d["briefs"][code]["fit"] is not None else "…",
                " | ".join(syms), syms.count("●")))
        for i, name in enumerate(dirs, 1):
            L += ["", "## %s.%d %s" % (code, i, name), ""]
            hits, none = [], []
            for d, cdir, rpath, rows in ordered:
                r = rows.get(i)
                if not r or r["strength"] in ("○", "") and re.sub(r"[^a-z]", "", r["what"].lower()) in ("", "nothing", "none"):
                    none.append(d["name"])
                    continue
                hits.append((0 if r["strength"] == "●" else (1 if r["strength"] == "◐" else 2), d, cdir, rpath, r))
            hits.sort(key=lambda t: (t[0], -(t[1]["briefs"][code]["fit"] or 0), t[1]["name"].lower()))
            if hits:
                L += ["| Company | Strength | What they have for it | Evidence | Maturity | Open |", "|---|---|---|---|---|---|"]
                for _o, d, cdir, rpath, r in hits:
                    L.append("| **%s** | %s | %s | %s | %s | %s |" % (
                        d["name"], r["strength"] or "·", rebase_links(r["what"], cdir, base) or "…",
                        rebase_links(r["evidence"], cdir, base) or "…", r["maturity"] or "…",
                        link("Register", rpath, base) + " · " + exists_link("Playbook", os.path.join(cdir, "%s-%s-3-Playbook.md" % (d["slug"], code)), base, "")))
            if none:
                L += ["", "*Nothing for this direction:* " + ", ".join(none) + "."]
        L.append("")
        write(os.path.join(base, code + "-6-Official-Directions-Who-Has-What.md"), "\n".join(L))
    return made


OFFICIAL_TAGLINE = {
    "T01": "Let robots become intelligent service partners of the future city.",
    "T02": "Use robots to build a safer, more resilient future city.",
    "T03": "Use robotics to drive a greener, more sustainable future.",
    "T04": "Let robots help people live healthier, more independent and dignified lives.",
}
COMPANY_DOC_LABELS = [("Products", "Products"), ("Developer-Guide", "Developer guide"), ("Roadmap-and-Strategy", "Roadmap"),
                      ("Solutions-and-Projects", "Solutions & projects"), ("Papers-and-Research", "Papers")]
TRACK_DOC_LABELS = [("1-Brief", "Brief"), ("2-Products-and-Solutions", "Products & solutions"), ("3-Playbook", "Playbook"),
                    ("4-Solutions-Register-and-Papers", "Register & papers")]
TRACK_LEVEL_LABELS = [("0-Track-Overview", "Overview"), ("6-Official-Directions-Who-Has-What", "Directions: who has what"),
                      ("2-Hardware-Shortlist", "Hardware shortlist"), ("1-Solution-Patterns", "Solution patterns"),
                      ("3-Cross-Vendor-Solutions", "Cross-vendor solutions"), ("4-Research-Library", "Research library"),
                      ("5-All-Solutions-and-Projects", "All solutions & projects")]
CORE_LABELS = [("Event-Intel", "Event intel — rules, judging, schedule"), ("02-Developer-Cheatsheet", "Developer cheat sheet"),
               ("01-Coverage-Audit", "Coverage audit"), ("00-START-HERE", "Hub page (vault version)"), ("README", "Read me — how to use this knowledge base"), ("-pipeline-README", "About the build pipeline")]


def doc_title(text, fallback):
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            body = text[end + 4:]
    for line in body.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def build_site(data):
    """Web viewer data: kb/core.js, kb/T0x.js, kb/<Company>.js (+ index.html for local use)."""
    docs, by_path, content = {}, {}, {}
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in ("kb", "assets", "vendor"))
        for n in sorted(names):
            if not n.endswith(".md"):
                continue
            path = os.path.join(base, n)
            relp = rel(path)
            parts = relp.split("/")
            did = re.sub(r"[^A-Za-z0-9-]", "-", n[:-3])
            if did in docs or did == "home":
                did = re.sub(r"[^A-Za-z0-9-]", "-", relp[:-3])
            comp = parts[1] if parts[0] == "Companies" and len(parts) > 2 else None
            trk = None
            for seg in parts[:-1]:
                mm = re.match(r"^(T0[1-4])-", seg)
                if mm:
                    trk = mm.group(1)
            part = comp or (trk if parts[0] == "Challenges" and trk else "core")
            text = read(path)
            docs[did] = {"id": did, "path": relp, "title": doc_title(text, did), "part": part, "company": comp, "track": trk}
            by_path[relp] = did
            content.setdefault(part, {})[did] = text

    def have(did):
        return did in docs

    tracks = []
    for code, folder, title, emoji, tagline in TRACKS:
        tdocs = [{"id": "%s-%s" % (code, sfx), "label": label} for sfx, label in TRACK_LEVEL_LABELS if have("%s-%s" % (code, sfx))]
        tracks.append({"code": code, "folder": folder, "title": title, "emoji": emoji, "tagline": tagline,
                       "official": OFFICIAL_TAGLINE.get(code, tagline), "dirs": DIRS[code], "docs": tdocs})
    companies = []
    for d in data:
        slug = d["slug"]
        cdocs = [{"id": slug, "label": "Profile"}] if have(slug) else []
        cdocs += [{"id": "%s-%s" % (slug, sfx), "label": label} for sfx, label in COMPANY_DOC_LABELS if have("%s-%s" % (slug, sfx))]
        ctracks, fits, verdicts = {}, {}, {}
        for code, folder, _t, _e, _g in TRACKS:
            ctracks[code] = [{"id": "%s-%s-%s" % (slug, code, sfx), "label": label} for sfx, label in TRACK_DOC_LABELS
                             if have("%s-%s-%s" % (slug, code, sfx))]
            fits[code] = d["briefs"][code]["fit"]
            verdicts[code] = cell(d["briefs"][code]["verdict"], 220)
        companies.append({"slug": slug, "name": d["name"], "oneLiner": cell(d["one_liner"], 240),
                          "onSite": cell(d["fm"].get("on_site_guess", ""), 200), "hq": d["fm"].get("hq", ""),
                          "website": d["fm"].get("website", ""), "categories": d["fm"].get("categories") or [],
                          "fits": fits, "verdicts": verdicts, "docs": cdocs, "tracks": ctracks})
    n_pics = sum(d["pics"] for d in data)
    meta = {"built": NOW, "counts": {"docs": len(docs), "pictures": n_pics, "companies": len(companies)},
            "tracks": tracks, "companies": companies, "docs": docs, "byPath": by_path,
            "core": [{"id": did, "label": label} for did, label in CORE_LABELS if have(did)]}
    kb = os.path.join(ROOT, "kb")
    os.makedirs(kb, exist_ok=True)

    def emit(name, obj):
        write(os.path.join(kb, name + ".js"), "__kbPart(" + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + ");\n")

    emit("core", {"name": "core", "meta": meta, "content": content.get("core", {})})
    sizes = {"core": size(os.path.join(kb, "core.js"))}
    for name in [t[0] for t in TRACKS] + [c[0] for c in COMPANIES]:
        emit(name, {"name": name, "content": content.get(name, {})})
        sizes[name] = size(os.path.join(kb, name + ".js"))
    frag_path = os.path.join(ROOT, "_pipeline", "viewer.fragment.html")
    if os.path.exists(frag_path):
        html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                '<style>:root{color-scheme:light}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>\n'
                + read(frag_path) + '\n</body>\n</html>\n')
        write(os.path.join(ROOT, "index.html"), html)
    return len(docs), sum(sizes.values()), max(sizes.values())


def build_canvas(data):
    """Obsidian canvas: one column per track, cards for every company with fit >= 3 (wikilinks by unique note name)."""
    nodes = []
    col_w, card_w, gap, head_h, card_h = 500, 440, 70, 230, 190
    for ci, (code, folder, title, emoji, tagline) in enumerate(TRACKS):
        x = ci * (col_w + gap)
        rows = []
        for d in data:
            b = d["briefs"][code]
            if b["fit"] is not None and b["fit"] >= 3:
                rows.append((b["fit"], d, b))
        rows.sort(key=lambda r: (-r[0], r[1]["name"].lower()))
        height = head_h + 40 + len(rows) * (card_h + 20) + 40
        nodes.append({"id": "g-" + code, "type": "group", "x": x, "y": 0, "width": col_w, "height": height,
                      "label": "%s %s" % (code, title)})
        nodes.append({"id": "h-" + code, "type": "text", "x": x + 30, "y": 30, "width": card_w, "height": head_h - 30,
                      "color": "6",
                      "text": "## %s %s %s\n%s\n\n[[%s-0-Track-Overview|Overview]] · [[%s-1-Solution-Patterns|Patterns]] · [[%s-2-Hardware-Shortlist|Shortlist]] · [[%s-3-Cross-Vendor-Solutions|Combos]]"
                              % (emoji, code, title, tagline, code, code, code, code)})
        y = head_h + 30
        for fit, d, b in rows:
            slug = d["slug"]
            color = "4" if fit >= 5 else ("5" if fit >= 4 else "3")
            head = "[[%s-%s-1-Brief|%s]]" % (slug, code, d["name"]) if b["exists"] else d["name"]
            text = "**%s — %s/5**\n%s\n\n[[%s-%s-3-Playbook|Playbook]] · [[%s-%s-2-Products-and-Solutions|Products]] · [[%s|Profile]]" % (
                head, fit, cell(b["verdict"], 170) or cell(d["one_liner"], 150), slug, code, slug, code, slug)
            nodes.append({"id": "c-%s-%s" % (code, slug), "type": "text", "x": x + 30, "y": y, "width": card_w,
                          "height": card_h, "color": color, "text": text})
            y += card_h + 20
    write(os.path.join(ROOT, "Hackathon-Map.canvas"), json.dumps({"nodes": nodes, "edges": []}, indent=1, ensure_ascii=False))


BASE_TEXT = """filters:
  and:
    - file.hasTag("leukerbad-hackathon")
properties:
  note.company:
    displayName: Company
  note.hq:
    displayName: HQ
  note.categories:
    displayName: Hardware class
  note.on_site_guess:
    displayName: Likely on site
  note.fit_t01:
    displayName: T01 Urban
  note.fit_t02:
    displayName: T02 Safe
  note.fit_t03:
    displayName: T03 Sustainable
  note.fit_t04:
    displayName: T04 Care
  note.fit:
    displayName: Fit
  note.challenge:
    displayName: Track
  note.identity_confidence:
    displayName: Identity confidence
views:
  - type: table
    name: "Companies - fit matrix"
    filters:
      and:
        - 'type == "company"'
    order:
      - file.name
      - hq
      - categories
      - on_site_guess
      - fit_t01
      - fit_t02
      - fit_t03
      - fit_t04
      - identity_confidence
    sort:
      - property: file.name
        direction: ASC
%s  - type: table
    name: "All track briefs"
    filters:
      and:
        - 'type == "challenge-brief"'
    groupBy:
      property: note.challenge
      direction: ASC
    order:
      - company
      - fit
      - file.name
    sort:
      - property: fit
        direction: DESC
"""

BASE_VIEW = """  - type: table
    name: "%s ranking"
    filters:
      and:
        - 'type == "challenge-brief"'
        - 'challenge == "%s"'
    order:
      - company
      - fit
      - file.name
    sort:
      - property: fit
        direction: DESC
"""


def build_base():
    views = "".join(BASE_VIEW % (code, code) for code, _f, _t, _e, _g in TRACKS)
    write(os.path.join(ROOT, "Companies.base"), BASE_TEXT % views)


def main():
    data = collect()
    if "--fix-images" in FLAGS:
        rep = fix_assets()
        print("assets: kept %d, resized %d, removed %d" % (rep["kept"], len(rep["resized"]), len(rep["removed"])))
        for r in rep["removed"]:
            print("  removed", r)
        data = collect()
    if "--final" in FLAGS:
        print("wired %d cross-links to second-pass docs" % wire_links(data))
        data = collect()
    build_shortlists(data)
    comp_stats = build_track_compilations(data)
    print("track compilations (company registers, first-pass fallbacks, research libraries):", comp_stats)
    n_dir = build_direction_pages(data)
    n_cheat = build_cheatsheet(data)
    build_canvas(data)
    build_base()
    totals = build_audit(data)
    build_hub(data)
    n_site, site_bytes, site_max = build_site(data)
    print("audit: %d/%d expected docs present" % (totals["ok"], totals["all"]))
    print("web viewer: %d docs packed, %.1f MB total, largest part %.1f MB" % (n_site, site_bytes / 1e6, site_max / 1e6))
    print("direction pages: %d" % n_dir)
    print("built hub + 4 shortlists + cheat sheet (%d guides) at %s" % (n_cheat, NOW))
    print("%-12s %-8s %-6s %-5s  %s" % ("company", "profile", "docs", "pics", "fit T01-T04 (b=brief, p=profile only)"))
    for d in data:
        fits = []
        for code, _f, _t, _e, _g in TRACKS:
            b = d["briefs"][code]
            fits.append("%s%s" % ("-" if b["fit"] is None else b["fit"], "b" if b["exists"] else ("p" if b["fit"] is not None else "")))
        print("%-12s %-8s %2d/%-3d %-5d  %s" % (d["slug"], "yes" if d["profile"] else "-", d["docs_have"], d["docs_total"], d["pics"], " ".join(fits)))
    if "--check" in FLAGS or "--fix-images" in FLAGS:
        files, bl, bi = check(data, fix_images="--fix-images" in FLAGS)
        print("checked %d md files: %d broken links, %d broken image embeds%s" % (
            files, len(bl), len(bi), " (image lines removed)" if "--fix-images" in FLAGS else ""))
        agg = {}
        for src, tgt in bl:
            agg.setdefault(tgt.split("/")[-1], []).append(src)
        for tgt, srcs in sorted(agg.items(), key=lambda kv: -len(kv[1]))[:40]:
            print("  missing link target %-55s x%d  e.g. %s" % (tgt, len(srcs), srcs[0]))
        if "--verbose" in FLAGS:
            for src, tgt in bi[:80]:
                print("  missing image %s  in %s" % (tgt, src))


if __name__ == "__main__":
    main()
