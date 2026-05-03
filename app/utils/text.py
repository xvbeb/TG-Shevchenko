from __future__ import annotations

import re


def normalize_text(value: str) -> str:
    return re.sub(r"[ \t]+", " ", value).strip()


def split_paragraphs(text: str) -> list[str]:
    raw_paragraphs = re.split(r"\n\s*\n+", text)
    return [normalize_text(paragraph.replace("\n", " ")) for paragraph in raw_paragraphs if normalize_text(paragraph)]


def count_words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def first_sentence(text: str, max_chars: int = 220) -> str:
    match = re.search(r"(.+?[.!?])(\s|$)", text)
    sentence = match.group(1) if match else text
    sentence = normalize_text(sentence)
    if len(sentence) <= max_chars:
        return sentence
    return sentence[: max_chars - 1].rstrip() + "..."
