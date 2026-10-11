#!/usr/bin/env python3
"""Convert EPUB books to clean Markdown with ebooklib + BeautifulSoup.

  python3 scripts/epub_to_md.py cache/book/book.epub
  python3 scripts/epub_to_md.py cache/book/book.epub --split
  python3 scripts/epub_to_md.py cache/book --out outputs/books
  python3 scripts/epub_to_md.py cache/book/book.epub --no-images
  python3 scripts/epub_to_md.py cache/book/book.epub --code-class class_s45V

A book is written to <epub folder>/markdown/<title>/: one <title>.md by
default, or index.md plus one NN_<chapter>.md per TOC entry with --split.
Images go to images/ beside the Markdown. The book's own contents page is
dropped. A directory converts every .epub in it. DRM-encrypted books are
skipped with an error.

Monospace paragraphs become code blocks automatically. Books that mark
prompts or code with a plain CSS class need --code-class <class>.
"""
from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
import warnings
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

try:
    import ebooklib
    from bs4 import BeautifulSoup, Comment, NavigableString, Tag
    from ebooklib import epub
except ImportError as exc:
    raise SystemExit(
        f"epub_to_md: {exc}. Run: python3 -m pip install ebooklib beautifulsoup4"
    )

HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCK_TAGS = HEADINGS | {
    "p", "div", "section", "article", "aside", "header", "footer", "main",
    "nav", "figure", "blockquote", "pre", "ul", "ol", "dl", "table", "hr", "body",
}
SKIP_TAGS = {"script", "style", "head", "title", "meta", "link"}
LINK_RE = re.compile(r"^(https?|mailto|ftp):", re.I)
BULLET_RE = re.compile(r"^\s*[●○◦•▪▫■□‣⁃∙◆◇➢➤►▶·]\s*")
BOLD_RE = re.compile(r"font-weight\s*:\s*(bold|bolder|[6-9]00)", re.I)
ITALIC_RE = re.compile(r"font-style\s*:\s*(italic|oblique)", re.I)
MONO_RE = re.compile(r"font-family\s*:[^;]*(mono|courier|consolas|menlo)", re.I)
MARGIN_RE = re.compile(r"margin-left\s*:\s*(-?[\d.]+)", re.I)
ZLIB_RE = re.compile(r"\s*\((?:z-library|z-lib|1lib)[^)]*\)", re.I)
HARD_BREAK = "\\\n"


class ConversionError(Exception):
    pass


def die(msg: str, code: int = 2) -> None:
    print(f"epub_to_md: {msg}", file=sys.stderr)
    raise SystemExit(code)


def escape(text: str) -> str:
    for ch in ("\\", "*", "`", "<"):
        text = text.replace(ch, "\\" + ch)
    return re.sub(r"(?<![0-9A-Za-z])_|_(?![0-9A-Za-z])", r"\\_", text)


def tidy(text: str) -> str:
    for ch in ("\u00ad", "\u200b", "\ufeff"):
        text = text.replace(ch, "")
    text = text.replace("****", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" ?\\\n ?", HARD_BREAK, text)
    text = re.sub(r"(?:\\\n)+", HARD_BREAK, text)
    return re.sub(r"^(?:\s|\\\n)+|(?:\s|\\\n)+$", "", text)


def guard(text: str) -> str:
    """Escape line starts that Markdown would read as headings, quotes or lists."""
    text = re.sub(r"^([#>+]|[-=]+$|- )", r"\\\1", text, flags=re.M)
    return re.sub(r"^(\d+)([.)]) ", r"\1\\\2 ", text, flags=re.M)


def wrap(text: str, mark: str) -> str:
    m = re.match(r"^((?:\s|\\\n)*)(.*?)((?:\s|\\\n)*)$", text, re.S)
    lead, core, trail = m.groups()
    if not core:
        return text
    return f"{lead}{mark}{core}{mark}{trail}"


def safe_name(text: str) -> str:
    text = re.sub(r'[\\/:*?"<>|\r\n\t]+', " ", text)
    return re.sub(r"\s+", " ", text).strip(" .")[:80].strip(" .")


def slug(text: str) -> str:
    return re.sub(r"[^\w]+", "-", text.lower()).strip("-_")[:60].strip("-_") or "section"


@dataclass
class Styles:
    rules: dict[str, str]
    code_classes: frozenset[str] = frozenset()

    def is_code(self, tag: Tag) -> bool:
        return bool(self.code_classes & set(tag.get("class") or [])) or self.has(tag, MONO_RE)

    def css(self, tag: Tag) -> str:
        parts = [self.rules.get(c, "") for c in tag.get("class") or []]
        parts.append(tag.get("style") or "")
        return ";".join(parts)

    def has(self, tag: Tag, pattern: re.Pattern) -> bool:
        return bool(pattern.search(self.css(tag)))

    def margin(self, tag: Tag) -> float:
        values = MARGIN_RE.findall(self.css(tag))
        return float(values[-1]) if values else 0.0


def load_styles(book: epub.EpubBook, code_classes: frozenset[str]) -> Styles:
    rules: dict[str, str] = {}
    for item in book.get_items_of_type(ebooklib.ITEM_STYLE):
        css = re.sub(r"/\*.*?\*/", "", item.get_content().decode("utf-8", "ignore"), flags=re.S)
        for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
            for selector in selectors.split(","):
                classes = re.findall(r"\.([\w-]+)", selector)
                if classes:
                    rules[classes[-1]] = rules.get(classes[-1], "") + ";" + body
    return Styles(rules, code_classes)


@dataclass
class Section:
    title: str
    blocks: list[tuple[str, str, int]] = field(default_factory=list)


class Converter:
    def __init__(self, book: epub.EpubBook, styles: Styles, images_dir: Path | None):
        self.book = book
        self.styles = styles
        self.images_dir = images_dir
        self.saved: dict[str, str] = {}
        self.doc_href = ""
        self.levels: dict[float, int] = {}

    def set_bullet_levels(self, soups) -> None:
        margins = {
            self.styles.margin(p)
            for soup in soups
            for p in soup.find_all("p")
            if BULLET_RE.match(p.get_text())
        }
        self.levels = {m: i for i, m in enumerate(sorted(margins))}

    def image(self, src: str, alt: str) -> str:
        if self.images_dir is None or not src or src.startswith("data:"):
            return ""
        href = posixpath.normpath(
            posixpath.join(posixpath.dirname(self.doc_href), unquote(src.split("#")[0]))
        )
        if href not in self.saved:
            item = self.book.get_item_with_href(href)
            if item is None:
                return ""
            name = posixpath.basename(href)
            stem, ext = posixpath.splitext(name)
            taken = set(self.saved.values())
            n = 1
            while f"images/{name}" in taken:
                n += 1
                name = f"{stem}_{n}{ext}"
            self.images_dir.mkdir(parents=True, exist_ok=True)
            (self.images_dir / name).write_bytes(item.get_content())
            self.saved[href] = f"images/{name}"
        return f"![{alt}]({self.saved[href]})"

    def inline(self, node) -> str:
        if isinstance(node, Comment):
            return ""
        if isinstance(node, NavigableString):
            return escape(re.sub(r"\s+", " ", str(node)))
        name = node.name
        if name in SKIP_TAGS:
            return ""
        if name == "br":
            return HARD_BREAK
        if name == "img":
            return self.image(node.get("src", ""), node.get("alt", "").strip())
        if name == "image":
            return self.image(node.get("xlink:href") or node.get("href", ""), "")
        if name in ("code", "kbd", "tt", "samp") or self.styles.is_code(node):
            code = re.sub(r"\s+", " ", node.get_text()).strip()
            return f"`{code}`" if code else ""
        inner = "".join(self.inline(c) for c in node.children)
        if name == "a":
            href = node.get("href", "")
            if LINK_RE.match(href) and inner.strip():
                return f"[{inner.strip()}]({href})"
            return inner
        if name in BLOCK_TAGS or name in ("li", "dt", "dd"):
            return f" {inner} "
        if name in ("b", "strong") or self.styles.has(node, BOLD_RE):
            inner = wrap(inner.replace("**", ""), "**")
        if name in ("i", "em", "cite", "dfn") or self.styles.has(node, ITALIC_RE):
            inner = wrap(inner, "*")
        return inner

    def blocks(self, node, out: list) -> None:
        for child in node.children:
            if isinstance(child, Comment):
                continue
            if isinstance(child, NavigableString):
                text = tidy(self.inline(child))
                if text:
                    out.append(("p", guard(text), 0))
                continue
            name = child.name
            if name in SKIP_TAGS:
                continue
            if name in HEADINGS:
                text = tidy(self.inline(child).replace("**", "").replace(HARD_BREAK, " "))
                if text:
                    out.append(("h", "#" * int(name[1]) + " " + text, 0))
            elif name == "p":
                self.paragraph(child, out)
            elif name in ("ul", "ol"):
                self.list(child, 0, out)
            elif name == "hr":
                out.append(("hr", "---", 0))
            elif name == "pre":
                code = child.get_text().strip("\n")
                if code.strip():
                    out.append(("code", code, 0))
            elif name == "blockquote":
                sub: list = []
                self.blocks(child, sub)
                body = assemble(sub)
                if body:
                    quoted = "\n".join(("> " + line).rstrip() for line in body.split("\n"))
                    out.append(("quote", quoted, 0))
            elif name == "table":
                table = self.table(child)
                if table:
                    out.append(("table", table, 0))
            elif name in ("img", "image", "svg"):
                images = child.find_all("image") if name == "svg" else [child]
                for img in images:
                    md = self.inline(img)
                    if md:
                        out.append(("p", md, 0))
            elif any(
                isinstance(c, Tag) and (c.name in BLOCK_TAGS or c.name in ("img", "svg"))
                for c in child.children
            ):
                self.blocks(child, out)
            else:
                self.paragraph(child, out)

    def paragraph(self, p: Tag, out: list) -> None:
        if self.styles.is_code(p):
            code = p.get_text().rstrip()
            if code.strip():
                out.append(("code", code, 0))
            return
        text = tidy(self.inline(p))
        if not text:
            return
        bullet = BULLET_RE.match(text)
        if bullet:
            prev = out[-1] if out else None
            deepest = prev[2] + 1 if prev and prev[0] == "li" else 0
            level = min(self.levels.get(self.styles.margin(p), 0), deepest)
            out.append(("li", "    " * level + "- " + guard(text[bullet.end():]), level))
            return
        if p.name == "p" and self.styles.has(p, BOLD_RE):
            text = wrap(text.replace("**", ""), "**")
        if p.name == "p" and self.styles.has(p, ITALIC_RE):
            text = wrap(text, "*")
        out.append(("p", guard(text), 0))

    def list(self, lst: Tag, depth: int, out: list) -> None:
        ordered = lst.name == "ol"
        try:
            n = int(lst.get("start", 1))
        except ValueError:
            n = 1
        for li in lst.find_all("li", recursive=False):
            nested = [c for c in li.children if isinstance(c, Tag) and c.name in ("ul", "ol")]
            nested_ids = {id(c) for c in nested}
            text = tidy("".join(self.inline(c) for c in li.children if id(c) not in nested_ids))
            text = guard(BULLET_RE.sub("", text))
            marker = f"{n}." if ordered else "-"
            n += 1
            out.append(("li", "    " * depth + f"{marker} {text}", depth))
            for sub in nested:
                self.list(sub, depth + 1, out)

    def table(self, table: Tag) -> str:
        rows = []
        for tr in table.find_all("tr"):
            cells = [
                tidy(self.inline(td)).replace(HARD_BREAK, "<br>").replace("|", "\\|")
                for td in tr.find_all(["td", "th"], recursive=False)
            ]
            if cells:
                rows.append(cells)
        if not rows:
            return ""
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
        lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
        return "\n".join(lines)


def assemble(blocks: list) -> str:
    merged: list = []
    for kind, text, level in blocks:
        if kind == "hr" and (not merged or merged[-1][0] in ("hr", "h")):
            continue
        if kind == "h" and merged and merged[-1][0] == "hr":
            merged.pop()
        if kind == "code" and merged and merged[-1][0] == "code":
            merged[-1] = ("code", merged[-1][1] + "\n" + text, 0)
            continue
        merged.append((kind, text, level))
    while merged and merged[-1][0] == "hr":
        merged.pop()

    parts: list[str] = []
    prev = None
    for kind, text, _ in merged:
        if kind == "code":
            fence = "```"
            while fence in text:
                fence += "`"
            text = f"{fence}\n{text}\n{fence}"
        if parts:
            parts.append("\n" if kind == "li" and prev == "li" else "\n\n")
        parts.append(text)
        prev = kind
    return "".join(parts)


def check_drm(path: Path) -> None:
    try:
        with zipfile.ZipFile(path) as zf:
            if "META-INF/encryption.xml" not in zf.namelist():
                return
            xml = zf.read("META-INF/encryption.xml").decode("utf-8", "ignore")
    except zipfile.BadZipFile:
        raise ConversionError("not a valid EPUB (zip) file")
    if re.search(r'Algorithm="[^"]*xmlenc#aes', xml):
        raise ConversionError("encrypted with DRM; remove DRM before converting")


def read_book(path: Path) -> epub.EpubBook:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            return epub.read_epub(str(path), options={"ignore_ncx": True})
        except Exception as exc:
            raise ConversionError(f"could not read EPUB: {exc}")


def meta(book: epub.EpubBook, name: str) -> str:
    values = book.get_metadata("DC", name)
    return values[0][0].strip() if values else ""


def spine_docs(book: epub.EpubBook) -> list:
    docs = []
    for idref, _linear in book.spine:
        item = book.get_item_with_id(idref)
        if item is not None and item.get_type() == ebooklib.ITEM_DOCUMENT:
            docs.append(item)
    return docs


def toc_starts(book: epub.EpubBook) -> dict[str, str]:
    """Map each document's file name to the first TOC title pointing at it."""
    starts: dict[str, str] = {}

    def walk(entries) -> None:
        for entry in entries:
            link, children = entry if isinstance(entry, tuple) else (entry, [])
            href = getattr(link, "href", "") or ""
            title = (getattr(link, "title", "") or "").strip()
            if href and title:
                starts.setdefault(posixpath.basename(unquote(href.split("#")[0])), title)
            walk(children)

    walk(book.toc)
    return starts


def is_contents_page(soup) -> bool:
    """A page whose lines are mostly in-book links is the book's own TOC."""
    lines = [p for p in soup.find_all(["p", "li"]) if p.get_text(strip=True)]
    linked = [
        p
        for p in lines
        if (a := p.find("a", href=True))
        and not LINK_RE.match(a["href"])
        and a.get_text(strip=True) == p.get_text(strip=True)
    ]
    return len(linked) >= 5 and len(linked) >= 0.8 * len(lines)


def first_heading(soup) -> str:
    tag = soup.find(list(HEADINGS))
    return re.sub(r"\s+", " ", tag.get_text()).strip() if tag else ""


def front_matter(title: str, author: str, source: str) -> str:
    lines = ["---", f"title: {json.dumps(title, ensure_ascii=False)}"]
    if author:
        lines.append(f"author: {json.dumps(author, ensure_ascii=False)}")
    lines += [f"source: {json.dumps(source, ensure_ascii=False)}", "---", "", ""]
    return "\n".join(lines)


def convert(
    path: Path, out_root: Path, *, split: bool, images: bool, code_classes: frozenset[str]
) -> None:
    check_drm(path)
    book = read_book(path)
    title = meta(book, "title") or ZLIB_RE.sub("", path.stem)
    author = meta(book, "creator")
    name = safe_name(title.split(":")[0]) or safe_name(ZLIB_RE.sub("", path.stem)) or "book"
    book_dir = out_root / name

    styles = load_styles(book, code_classes)
    conv = Converter(book, styles, book_dir / "images" if images else None)
    soups = [(item, BeautifulSoup(item.get_content(), "html.parser")) for item in spine_docs(book)]
    if not soups:
        raise ConversionError("no readable chapters in spine")
    conv.set_bullet_levels(soup for _, soup in soups)

    starts = toc_starts(book)
    sections: list[Section] = []
    for item, soup in soups:
        key = posixpath.basename(item.get_name())
        if is_contents_page(soup):
            continue
        if not starts:
            sections.append(Section(first_heading(soup) or posixpath.splitext(key)[0]))
        elif key in starts:
            sections.append(Section(starts[key]))
        elif not sections:
            sections.append(Section("Front matter"))
        conv.doc_href = item.get_name()
        conv.blocks(soup.body or soup, sections[-1].blocks)

    book_dir.mkdir(parents=True, exist_ok=True)
    header = front_matter(title, author, path.name)
    bodies = [(s.title, assemble(s.blocks)) for s in sections]
    bodies = [(t, b) for t, b in bodies if b.strip()]

    if split:
        for old in book_dir.glob("[0-9][0-9]_*.md"):
            old.unlink()
        index = [f"# {title}", ""]
        if author:
            index += [f"*{author}*", ""]
        for i, (sec_title, body) in enumerate(bodies):
            fname = f"{i:02d}_{slug(sec_title)}.md"
            (book_dir / fname).write_text(body + "\n", encoding="utf-8")
            index.append(f"- [{sec_title}]({fname})")
        target = book_dir / "index.md"
        target.write_text(header + "\n".join(index) + "\n", encoding="utf-8")
    else:
        target = book_dir / f"{name}.md"
        target.write_text(header + "\n\n".join(b for _, b in bodies) + "\n", encoding="utf-8")

    size_kb = sum(len(b.encode("utf-8")) for _, b in bodies) / 1024
    print(
        f"{path.name}\n  -> {target}\n  sections={len(bodies)}  "
        f"images={len(conv.saved)}  text={size_kb:.0f} KB",
        flush=True,
    )


def collect(src: Path) -> list[Path]:
    if src.is_file():
        if src.suffix.lower() != ".epub":
            die(f"not an .epub file: {src}")
        return [src]
    if not src.is_dir():
        die(f"not found: {src}")
    books = sorted(p for p in src.iterdir() if p.is_file() and p.suffix.lower() == ".epub")
    if not books:
        die(f"no .epub files in {src}")
    return books


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="把 EPUB 转成干净的 Markdown（单个文件，或一个目录里的全部 .epub）。"
    )
    parser.add_argument("input", type=Path, help="EPUB 路径，或 EPUB 所在目录")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="输出根目录（默认：EPUB 旁边的 markdown/），每本书一个子目录",
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help="按目录章节拆成多个 .md，并生成 index.md（默认合并成一个文件）",
    )
    parser.add_argument(
        "--no-images",
        dest="images",
        action="store_false",
        help="不导出图片，Markdown 里也不插入图片",
    )
    parser.add_argument(
        "--code-class",
        dest="code_classes",
        action="append",
        default=[],
        metavar="CLASS",
        help="把带这个 CSS 类的段落当作代码块（可重复；等宽字体段落自动识别）",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    src = args.input.expanduser().resolve()
    books = collect(src)
    out_root = (
        args.out.expanduser().resolve()
        if args.out
        else (src.parent if src.is_file() else src) / "markdown"
    )
    failed = 0
    for path in books:
        try:
            convert(
                path,
                out_root,
                split=args.split,
                images=args.images,
                code_classes=frozenset(args.code_classes),
            )
        except ConversionError as exc:
            print(f"epub_to_md: {path.name}: {exc}", file=sys.stderr)
            failed += 1
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
