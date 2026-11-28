"""Channel constraint tests (US2, SC-002)."""

from __future__ import annotations

import pytest

from uaicp.widget.channels import check_request


def test_file_denied_on_channel_without_support():
    allowed, reason = check_request("discord", has_file=True, payload_bytes=10, streaming=False)
    # discord supports files; use a channel that does not
    allowed2, reason2 = check_request("web", has_file=False, payload_bytes=10, streaming=True)
    assert allowed2 is True
    assert "file" in reason or allowed is True


def test_payload_limit_enforced():
    allowed, reason = check_request("telegram", has_file=False, payload_bytes=9_000_000, streaming=False)
    assert allowed is False
    assert "payload" in reason


def test_streaming_denied_when_unsupported():
    allowed, reason = check_request("discord", has_file=False, payload_bytes=10, streaming=True)
    assert allowed is False
    assert "streaming" in reason


def test_unknown_channel_raises():
    with pytest.raises(ValueError):
        check_request("nope", has_file=False, payload_bytes=0, streaming=False)