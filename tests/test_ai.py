from __future__ import annotations

from app.services.ai import looks_like_json_fragment, parse_json_payload


def test_parse_json_payload_accepts_plain_object() -> None:
    assert parse_json_payload('{"type":"quick","recap":"Previously"}') == {
        "type": "quick",
        "recap": "Previously",
    }


def test_parse_json_payload_extracts_markdown_fence() -> None:
    raw = 'Result:\n```json\n{"type":"fiction","events":["One"]}\n```'

    assert parse_json_payload(raw) == {"type": "fiction", "events": ["One"]}


def test_incomplete_json_is_rejected_as_fragment() -> None:
    raw = '{"type":"quick","recap":"unfinished"'

    assert parse_json_payload(raw) is None
    assert looks_like_json_fragment(raw) is True

