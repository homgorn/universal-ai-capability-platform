"""Integration tests for tenant isolation (FR-003, SC-003)."""

from __future__ import annotations

from uaicp.db.models import Capability
from uaicp.db.repository import TenantRepository
from uaicp.domain.enums import CapabilityStatus


def test_cross_tenant_read_is_blocked(session):
    session.add(
        Capability(
            tenant_id="A",
            capability_id="image.upscale",
            name="upscale",
            status=CapabilityStatus.ACTIVE,
        )
    )
    session.flush()

    repo_b = TenantRepository(session, "B")
    assert repo_b.get(Capability, 1) is None
    assert repo_b.list(Capability) == []


def test_cross_tenant_write_is_forbidden(session):
    repo_a = TenantRepository(session, "A")
    cap = Capability(
        tenant_id="B",
        capability_id="image.upscale",
        name="upscale",
        status=CapabilityStatus.ACTIVE,
    )
    try:
        repo_a.add(cap)
    except PermissionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("cross-tenant write should be forbidden")


def test_same_tenant_read_ok(session):
    session.add(
        Capability(
            tenant_id="A",
            capability_id="image.upscale",
            name="upscale",
            status=CapabilityStatus.ACTIVE,
        )
    )
    session.flush()
    repo_a = TenantRepository(session, "A")
    assert len(repo_a.list(Capability)) == 1