"""Tests for enforced invariants (FR-011, Constitution III)."""

from __future__ import annotations

from uaicp.api.main import app
from uaicp.db.models import Capability
from uaicp.domain.enums import CapabilityStatus


def test_capability_defaults_to_discovered(session):
    cap = Capability(tenant_id="t", capability_id="image.upscale", name="upscale")
    session.add(cap)
    session.flush()
    # discovered != executable: default is DISCOVERED, never ACTIVE.
    assert cap.status == CapabilityStatus.DISCOVERED
    assert cap.status is not CapabilityStatus.ACTIVE


def test_no_browser_route_exposes_secrets():
    for route in app.routes:
        path = getattr(route, "path", "").lower()
        assert "secret" not in path, path
        assert "credential" not in path, path