from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional
from zipfile import ZipFile

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub

from app.utils.text import count_words, normalize_text, split_paragraphs


@dataclass
class ParsedBook:
    title: str
    author: Optional[str]
    source_type: str
    chunks: list[str]
    total_words: int


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

    chunks = split_paragraphs(text)
    return ParsedBook(
        title=title or Path(filename).stem,
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
    paragraphs: list[str] = []

    for item in book.get_items_of_type(ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")
        for tag in soup.find_all(["p", "blockquote", "li"]):
            text = normalize_text(tag.get_text(" "))
            if text:
                paragraphs.append(text)

    return ParsedBook(
        title=title or metadata_title or Path(filename).stem,
        author=author or metadata_author,
        source_type="epub",
        chunks=paragraphs,
        total_words=sum(count_words(chunk) for chunk in paragraphs),
    )


def _parse_fb2(filename: str, content: bytes, title: Optional[str], author: Optional[str]) -> ParsedBook:
    raw_content = _unpack_fb2_if_needed(filename, content)
    text = _decode_text(raw_content)
    soup = BeautifulSoup(text, "xml")

    metadata_title = _tag_text(soup, "book-title")
    metadata_author = _fb2_author(soup)
    paragraphs: list[str] = []

    for tag in soup.find_all(["p", "subtitle", "v"]):
        value = normalize_text(tag.get_text(" "))
        if value:
            paragraphs.append(value)

    return ParsedBook(
        title=title or metadata_title or Path(filename).stem.replace(".fb2", ""),
        author=author or metadata_author,
        source_type="fb2",
        chunks=paragraphs,
        total_words=sum(count_words(chunk) for chunk in paragraphs),
    )


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
