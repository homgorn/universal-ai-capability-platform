"""Embeddability classification tests."""

from __future__ import annotations

from uaicp.catalog.embed import embed_info


def test_public_gradio_is_embeddable():
    info = embed_info({"id": "demo/app", "sdk": "gradio", "subdomain": "demo-app", "private": False})
    assert info.status == "EMBEDDABLE"
    assert info.web_component is True
    assert info.embed_url == "https://demo-app.hf.space"


def test_private_is_not_embeddable():
    info = embed_info({"id": "x/y", "sdk": "gradio", "private": True})
    assert info.status == "NOT_EMBEDDABLE"


def test_missing_subdomain_derives_slug():
    info = embed_info({"id": "owner/my-space", "sdk": "static", "private": False})
    assert info.status == "EMBEDDABLE"
    assert info.embed_url == "https://owner-my-space.hf.space"


def test_unknown_runtime_is_verify():
    info = embed_info({"id": "x/y", "sdk": "gradio", "private": False, "runtime": {"stage": "BUILDING"}})
    assert info.status == "VERIFY"