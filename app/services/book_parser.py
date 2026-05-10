from __future__ import annotations

import base64
import re
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional
from zipfile import ZipFile

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, epub

from app.utils.text import build_reading_chunks, count_words, normalize_text, split_paragraphs


@dataclass
class ParsedBook:
    title: str
    author: Optional[str]
    source_type: str
    chunks: list[str]
    total_words: int
    cover_image_data_url: Optional[str] = None


def parse_book_upload(filename: str, content: bytes, title: Optional[str] = None, author: Optional[str] = None) -> ParsedBook:
    extension = Path(filename).suffix.lower().lstrip(".")
    if extension == "txt":
        return _parse_txt(filename, content, title, author)
    if extension == "epub":
        return _parse_epub(filename, content, title, author)
    if extension == "fb2" or filename.lower().endswith(".fb2.zip"):
        return _parse_fb2(filename, content, title, author)
    raise ValueError("Only TXT, EPUB and FB2 files are supported in the MVP")


def _parse_txt(filename: str, content: bytes, title: Optional[str], author: Optional[str]) -> ParsedBook:
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    chunks = build_reading_chunks(split_paragraphs(text))
    return ParsedBook(
        title=clean_book_title(title or Path(filename).stem, filename),
        author=author,
        source_type="txt",
        chunks=chunks,
        total_words=sum(count_words(chunk) for chunk in chunks),
    )


def _parse_epub(filename: str, content: bytes, title: Optional[str], author: Optional[str]) -> ParsedBook:
    # ebooklib expects a path-like source, so the uploaded bytes briefly live in /tmp.
    with NamedTemporaryFile(suffix=".epub") as tmp:
        tmp.write(content)
        tmp.flush()
        book = epub.read_epub(tmp.name)

    metadata_title = _first_metadata(book, "DC", "title")
    metadata_author = _first_metadata(book, "DC", "creator")
    cover_image_data_url = _extract_epub_cover(book)
    paragraphs: list[str] = []

    for item in book.get_items_of_type(ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")
        for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "blockquote", "li"]):
            text = normalize_text(tag.get_text(" "))
            if text:
                paragraphs.append(text)

    chunks = build_reading_chunks(paragraphs)
    return ParsedBook(
        title=clean_book_title(title or metadata_title or Path(filename).stem, filename),
        author=author or metadata_author,
        source_type="epub",
        chunks=chunks,
        total_words=sum(count_words(chunk) for chunk in chunks),
        cover_image_data_url=cover_image_data_url,
    )


def _parse_fb2(filename: str, content: bytes, title: Optional[str], author: Optional[str]) -> ParsedBook:
    raw_content = _unpack_fb2_if_needed(filename, content)
    text = _decode_text(raw_content)
    soup = BeautifulSoup(text, "xml")

    metadata_title = _tag_text(soup, "book-title")
    metadata_author = _fb2_author(soup)
    cover_image_data_url = _extract_fb2_cover(soup)
    paragraphs: list[str] = []

    for tag in soup.find_all(["title", "subtitle", "p", "v"]):
        value = normalize_text(tag.get_text(" "))
        if value:
            paragraphs.append(value)

    chunks = build_reading_chunks(paragraphs)
    return ParsedBook(
        title=clean_book_title(title or metadata_title or _strip_known_extensions(filename), filename),
        author=author or metadata_author,
        source_type="fb2",
        chunks=chunks,
        total_words=sum(count_words(chunk) for chunk in chunks),
        cover_image_data_url=cover_image_data_url,
    )


def clean_book_title(raw_title: str, filename: str) -> str:
    value = normalize_text(raw_title or _strip_known_extensions(filename))
    value = _strip_known_extensions(value)
    value = re.sub(r"(?i)^microsoft\s+word\s*[-–—:]*\s*", "", value)
    value = re.sub(r"[_]+", " ", value)
    value = re.sub(r"(?i)^r[\s.-]+", "", value)
    value = re.sub(r"(?i)\bfull\s*text\b", "", value)
    value = re.sub(r"\s+\d+\s*$", "", value)
    value = normalize_text(value).strip(" -–—_.")
    if not value:
        value = _strip_known_extensions(filename)
    if _is_latin_uppercase_noise(value):
        value = value.title()
    return value or "Без названия"


def _strip_known_extensions(value: str) -> str:
    path = Path(value)
    name = path.name
    known_suffixes = {".txt", ".epub", ".fb2", ".zip", ".doc", ".docx", ".rtf"}
    changed = True
    while changed:
        changed = False
        suffix = Path(name).suffix.lower()
        if suffix in known_suffixes:
            name = name[: -len(suffix)]
            changed = True
    return name


def _is_latin_uppercase_noise(value: str) -> bool:
    letters = [char for char in value if char.isalpha()]
    latin_letters = [char for char in letters if char.lower() in "abcdefghijklmnopqrstuvwxyz"]
    if not latin_letters or len(latin_letters) < max(3, len(letters) // 2):
        return False
    return all(not char.islower() for char in latin_letters)


def _image_data_url(content: bytes, media_type: Optional[str]) -> Optional[str]:
    if not content:
        return None
    if len(content) > 1_500_000:
        return None
    mime = media_type or "image/jpeg"
    encoded = base64.b64encode(content).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _extract_epub_cover(book: epub.EpubBook) -> Optional[str]:
    cover_ids: list[str] = []
    for _, attrs in book.get_metadata("OPF", "cover"):
        content = attrs.get("content") if isinstance(attrs, dict) else None
        if content:
            cover_ids.append(content)

    for cover_id in cover_ids:
        item = book.get_item_with_id(cover_id)
        if item:
            return _image_data_url(item.get_content(), getattr(item, "media_type", None))

    image_items = list(book.get_items_of_type(ITEM_IMAGE))
    for item in image_items:
        name = (getattr(item, "file_name", "") or "").lower()
        if "cover" in name:
            return _image_data_url(item.get_content(), getattr(item, "media_type", None))
    if image_items:
        item = image_items[0]
        return _image_data_url(item.get_content(), getattr(item, "media_type", None))
    return None


def _extract_fb2_cover(soup: BeautifulSoup) -> Optional[str]:
    cover_id = _fb2_cover_id(soup)
    binaries = soup.find_all("binary")
    for binary in binaries:
        binary_id = binary.get("id")
        if cover_id and binary_id != cover_id:
            continue
        media_type = binary.get("content-type") or "image/jpeg"
        try:
            content = base64.b64decode("".join(binary.get_text().split()), validate=False)
        except ValueError:
            continue
        return _image_data_url(content, media_type)

    for binary in binaries:
        media_type = binary.get("content-type") or ""
        if not media_type.startswith("image/"):
            continue
        try:
            content = base64.b64decode("".join(binary.get_text().split()), validate=False)
        except ValueError:
            continue
        return _image_data_url(content, media_type)
    return None


def _fb2_cover_id(soup: BeautifulSoup) -> Optional[str]:
    coverpage = soup.find("coverpage")
    if not coverpage:
        return None
    image = coverpage.find("image")
    if not image:
        return None
    for value in image.attrs.values():
        if isinstance(value, str) and value.startswith("#"):
            return value[1:]
    return None


def _first_metadata(book: epub.EpubBook, namespace: str, name: str) -> Optional[str]:
    values = book.get_metadata(namespace, name)
    if not values:
        return None
    value = values[0][0]
    return str(value) if value else None


def _unpack_fb2_if_needed(filename: str, content: bytes) -> bytes:
    if not filename.lower().endswith(".fb2.zip"):
        return content

    with NamedTemporaryFile(suffix=".zip") as tmp:
        tmp.write(content)
        tmp.flush()
        with ZipFile(tmp.name) as archive:
            fb2_names = [name for name in archive.namelist() if name.lower().endswith(".fb2")]
            if not fb2_names:
                raise ValueError("FB2 zip archive does not contain an .fb2 file")
            return archive.read(fb2_names[0])


def _decode_text(content: bytes) -> str:
    for encoding in ["utf-8-sig", "utf-16", "windows-1251", "latin-1"]:
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="ignore")


def _tag_text(soup: BeautifulSoup, name: str) -> Optional[str]:
    tag = soup.find(name)
    if not tag:
        return None
    value = normalize_text(tag.get_text(" "))
    return value or None


def _fb2_author(soup: BeautifulSoup) -> Optional[str]:
    author_tag = soup.find("author")
    if not author_tag:
        return None
    first_name = _tag_text(author_tag, "first-name")
    middle_name = _tag_text(author_tag, "middle-name")
    last_name = _tag_text(author_tag, "last-name")
    nickname = _tag_text(author_tag, "nickname")
    parts = [part for part in [first_name, middle_name, last_name] if part]
    if parts:
        return " ".join(parts)
    return nickname
