from __future__ import annotations

import re

MIN_CHUNK_WORDS = 90
TARGET_CHUNK_WORDS = 180
MAX_CHUNK_WORDS = 280


def normalize_text(value: str) -> str:
    return re.sub(r"[ \t]+", " ", value).strip()


def split_paragraphs(text: str) -> list[str]:
    raw_paragraphs = re.split(r"\n\s*\n+", text)
    return [normalize_text(paragraph.replace("\n", " ")) for paragraph in raw_paragraphs if normalize_text(paragraph)]


def count_words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def build_reading_chunks(
    paragraphs: list[str],
    min_words: int = MIN_CHUNK_WORDS,
    target_words: int = TARGET_CHUNK_WORDS,
    max_words: int = MAX_CHUNK_WORDS,
) -> list[str]:
    chunks: list[str] = []
    current: list[str] = []
    current_words = 0

    for paragraph in paragraphs:
        clean = normalize_text(paragraph)
        if not clean:
            continue
        parts = _split_large_paragraph(clean, max_words=max_words, target_words=target_words)
        for part in parts:
            part_words = count_words(part)
            if not current:
                current = [part]
                current_words = part_words
                if current_words >= max_words:
                    _push_chunk(chunks, current)
                    current = []
                    current_words = 0
                continue

            would_be = current_words + part_words
            should_close = current_words >= min_words and would_be > max_words
            target_reached = current_words >= target_words and part_words >= min_words
            if should_close or target_reached:
                _push_chunk(chunks, current)
                current = [part]
                current_words = part_words
            else:
                current.append(part)
                current_words = would_be

    if current:
        if chunks and current_words < min_words:
            chunks[-1] = chunks[-1] + "\n\n" + "\n\n".join(current)
        else:
            _push_chunk(chunks, current)

    return chunks


def first_sentence(text: str, max_chars: int = 220) -> str:
    match = re.search(r"(.+?[.!?])(\s|$)", text)
    sentence = match.group(1) if match else text
    sentence = normalize_text(sentence)
    if len(sentence) <= max_chars:
        return sentence
    return sentence[: max_chars - 1].rstrip() + "..."


def _split_large_paragraph(paragraph: str, max_words: int, target_words: int) -> list[str]:
    if count_words(paragraph) <= max_words:
        return [paragraph]

    sentences = _split_sentences(paragraph)
    parts: list[str] = []
    current: list[str] = []
    current_words = 0
    for sentence in sentences:
        sentence_words = count_words(sentence)
        if sentence_words > max_words:
            if current:
                parts.append(" ".join(current))
                current = []
                current_words = 0
            parts.extend(_split_words(sentence, target_words))
            continue
        if current and current_words + sentence_words > max_words:
            parts.append(" ".join(current))
            current = [sentence]
            current_words = sentence_words
        else:
            current.append(sentence)
            current_words += sentence_words
            if current_words >= target_words:
                parts.append(" ".join(current))
                current = []
                current_words = 0
    if current:
        parts.append(" ".join(current))
    return parts


def _split_sentences(text: str) -> list[str]:
    pieces = re.split(r"(?<=[.!?…])\s+", text)
    return [normalize_text(piece) for piece in pieces if normalize_text(piece)]


def _split_words(text: str, target_words: int) -> list[str]:
    words = text.split()
    return [" ".join(words[index : index + target_words]) for index in range(0, len(words), target_words)]


def _push_chunk(chunks: list[str], paragraphs: list[str]) -> None:
    value = "\n\n".join(paragraphs).strip()
    if value:
        chunks.append(value)
