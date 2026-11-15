"""Web UI stream, confidence overlay, and status tests (ROS-free)."""

from types import SimpleNamespace

import numpy as np
import pytest

from web_ui.app import PAGE, DashboardApp
from web_ui.types import Detection


def test_page_contains_three_camera_streams():
    assert 'src="/stream"' in PAGE
    assert 'src="/front_stream"' in PAGE
    assert 'src="/wrist_stream"' in PAGE


def test_render_cache_tracks_mask_and_box_changes():
    frame = np.zeros((120, 120, 3), dtype=np.uint8)
    stream = SimpleNamespace(frames_received=1, latest=lambda max_age_s=5.0: frame)
    app = SimpleNamespace(
        _bboxes_enabled=True,
        _jpeg_cache={},
        _stream_for=lambda _name: stream,
        _encode=lambda image: image.tobytes(),
    )
    first = Detection("can", 0.8, (20, 30, 100, 100), ((20, 30), (100, 30), (100, 100)))
    second = Detection("can", 0.8, (30, 40, 90, 90), ((30, 40), (90, 40), (90, 90)))
    original = DashboardApp._camera_jpeg(app, "front", [first])
    changed = DashboardApp._camera_jpeg(app, "front", [second])
    assert original != changed


@pytest.mark.parametrize("camera", ["table", "front", "wrist"])
@pytest.mark.parametrize("confidence, visible", [(0.49, False), (0.5, True), (0.51, True)])
def test_display_confidence_threshold(camera, confidence, visible):
    frame = np.zeros((120, 120, 3), dtype=np.uint8)
    stream = SimpleNamespace(frames_received=1, latest=lambda max_age_s=5.0: frame)
    app = SimpleNamespace(
        _bboxes_enabled=True,
        _jpeg_cache={},
        _stream_for=lambda _name: stream,
        _encode=lambda image: image.tobytes(),
    )
    detection = Detection("can", confidence, (20, 30, 100, 100), ((20, 30), (100, 30), (100, 100)))
    rendered = DashboardApp._camera_jpeg(app, camera, [detection])
    assert (rendered != frame.tobytes()) is visible


def _make_model_app(provider="mock", model="mock", api_key="", base_url=None):
    import threading

    app = SimpleNamespace(
        _config=SimpleNamespace(
            api_key=lambda: api_key,
            vlm=SimpleNamespace(base_url=base_url),
        ),
        _provider=provider,
        _model=model,
        _lock=threading.Lock(),
        _worker=None,
        _events=SimpleNamespace(emit=lambda *a, **kw: None),
    )
    app.available_models = lambda: DashboardApp.available_models(app)
    app._cached_provider_models = lambda *a, **kw: DashboardApp._cached_provider_models(app, *a, **kw)
    return app


def test_available_models_credential_gating(monkeypatch):
    monkeypatch.setattr("web_ui.vlm.registry._fetch_json", lambda *a, **kw: (_ for _ in ()).throw(OSError("offline")))
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("CLAUDE_API_KEY", raising=False)

    app = _make_model_app()
    assert app.available_models() == [{"provider": "mock", "model": "mock"}]

    monkeypatch.setenv("GEMINI_API_KEY", "test-gem-key")
    providers = {m["provider"] for m in app.available_models()}
    assert providers == {"gemini", "mock"}

    monkeypatch.setenv("OPENAI_API_KEY", "test-oai-key")
    providers = {m["provider"] for m in app.available_models()}
    assert providers == {"gemini", "openai", "mock"}

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-ant-key")
    providers = {m["provider"] for m in app.available_models()}
    assert providers == {"gemini", "openai", "anthropic", "mock"}


def test_set_model_accepts_available_and_rejects_uncredentialed(monkeypatch):
    monkeypatch.setattr("web_ui.vlm.registry._fetch_json", lambda *a, **kw: (_ for _ in ()).throw(OSError("offline")))
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("CLAUDE_API_KEY", raising=False)

    app = _make_model_app()
    with pytest.raises(ValueError):
        DashboardApp.set_model(app, "openai", "gpt-4o")
    with pytest.raises(ValueError):
        DashboardApp.set_model(app, "anthropic", "claude-sonnet-4-20250514")

    monkeypatch.setenv("OPENAI_API_KEY", "test-oai-key")
    assert DashboardApp.set_model(app, "openai", "gpt-4o-mini") is True
    assert (app._provider, app._model) == ("openai", "gpt-4o-mini")

    monkeypatch.setenv("CLAUDE_API_KEY", "test-claude-key")
    assert DashboardApp.set_model(app, "anthropic", "claude-sonnet-4-20250514") is True
    assert (app._provider, app._model) == ("anthropic", "claude-sonnet-4-20250514")


def test_make_session_anthropic_accepts_claude_api_key(monkeypatch):
    from web_ui.config import VLMSettings
    from web_ui.vlm.registry import make_session

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("CLAUDE_API_KEY", "test-claude-key")
    session = make_session(VLMSettings(provider="anthropic", model="claude-sonnet-4-20250514"), "sys", [])
    assert session.name == "anthropic"
    assert session.model == "claude-sonnet-4-20250514"


def test_list_provider_models_queries_live_api(monkeypatch):
    from web_ui.vlm.registry import list_provider_models

    def fake_fetch(url, headers=None, timeout_s=3.0):
        if "generativelanguage.googleapis.com" in url:
            return {
                "models": [
                    {"name": "models/gemini-2.5-pro", "supportedGenerationMethods": ["generateContent"]},
                    {"name": "models/embedding-001", "supportedGenerationMethods": ["embedContent"]},
                ]
            }
        if "api.openai.com" in url:
            return {"data": [{"id": "gpt-4o"}, {"id": "gpt-4.1"}, {"id": "text-embedding-3-small"}]}
        if "api.anthropic.com" in url:
            return {"data": [{"id": "claude-sonnet-4-20250514"}, {"id": "claude-opus-4-1-20250805"}]}
        raise AssertionError(f"unexpected url: {url}")

    monkeypatch.setattr("web_ui.vlm.registry._fetch_json", fake_fetch)
    assert list_provider_models("gemini", api_key="k") == ["gemini-2.5-pro"]
    assert list_provider_models("openai", api_key="k") == ["gpt-4.1", "gpt-4o"]
    assert list_provider_models("anthropic", api_key="k") == ["claude-sonnet-4-20250514", "claude-opus-4-1-20250805"]
