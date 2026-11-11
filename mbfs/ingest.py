"""Load the corpus into chunks. Every line keeps its exact character span in the source file."""

import csv
import io
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path


@dataclass
class Line:
    text: str  # cleaned text used for search and answers
    quote: str  # exact source text: source[start:end] == quote
    start: int
    end: int
    line_no: int


@dataclass
class Chunk:
    id: str
    source: str
    title: str
    lines: list[Line] = field(default_factory=list)

    @property
    def text(self):
        return "\n".join(line.text for line in self.lines)


def make_line(src, start, end, text=None):
    raw = src[start:end]
    start += len(raw) - len(raw.lstrip())
    end -= len(raw) - len(raw.rstrip())
    quote = src[start:end]
    return Line(text or " ".join(quote.split()), quote, start, end, src.count("\n", 0, start) + 1)


def table_row(headers, values):
    # "£15.00" on its own is useless to search, so each value keeps its column name
    return " | ".join(f"{h}: {v}" for h, v in zip(headers, values) if v)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_markdown(src, path):
    """Policies: one chunk per '## ' section, one line per paragraph, list item or table row."""
    meta = dict(re.findall(r"^(\w+): (.+)$", src.split("\n---", 1)[0], re.MULTILINE))
    chunks = []
    for m in re.finditer(r"^.*$", src, re.MULTILINE):
        text = m.group()
        if text.startswith("## "):
            heading = text[3:].strip()
            chunks.append(
                Chunk(f"{meta['document_id']}#{slug(heading)}", path, f"{meta['title']} › {heading}")
            )
        elif chunks and text.strip() and not text.startswith("#") and not set(text) <= set("|-: "):
            chunks[-1].lines.append(make_line(src, m.start(), m.end()))
    return chunks


def load_notice(src, path):
    """Plain-text notices: section headings sit between ==== or ---- rules, and text is
    hard-wrapped, so a citable line is a whole paragraph."""
    doc_id = re.search(r"Document ID: (\S+)", src).group(1)
    title_field = re.search(r"^Title: (.+)$", src, re.MULTILINE)
    title = title_field.group(1) if title_field else src.split("\n")[1].strip()
    rule = re.compile(r"^[=-]{10,}$")
    lines = src.split("\n")
    chunks = [Chunk(f"{doc_id}#details", path, f"{title} › Details")]
    offset, para_start = 0, None
    for i, line in enumerate(lines):
        heading = 0 < i < len(lines) - 1 and rule.match(lines[i - 1]) and rule.match(lines[i + 1])
        if para_start is not None and (not line.strip() or rule.match(line)):
            para = make_line(src, para_start, offset)
            if not para.text.startswith("[Synthetic"):
                chunks[-1].lines.append(para)
            para_start = None
        if heading:
            chunks.append(Chunk(f"{doc_id}#{slug(line)}", path, f"{title} › {line.strip().capitalize()}"))
        elif line.strip() and not rule.match(line) and para_start is None:
            para_start = offset
        offset += len(line) + 1
    if para_start is not None:
        chunks[-1].lines.append(make_line(src, para_start, len(src)))
    return [c for c in chunks if c.lines]


class FaqParser(HTMLParser):
    """Keeps <p>, <li> and table rows inside <main>, grouped under the preceding <h3> question.
    The page header, footer, scripts and styles are outside <main> and ignored."""

    def __init__(self, src):
        super().__init__()
        self.src = src
        self.line_offsets = [0] + [m.end() for m in re.finditer("\n", src)]
        self.in_main, self.title, self.heading = False, "", ""
        self.blocks = []  # (heading, Line)
        self.text, self.cells, self.headers, self.block_start = [], [], [], 0

    def position(self):
        line, col = self.getpos()
        return self.line_offsets[line - 1] + col

    def handle_starttag(self, tag, attrs):
        self.in_main |= tag == "main"
        if tag in ("title", "h3", "p", "li", "td", "th"):
            self.text = []
        if tag in ("p", "li", "tr"):
            self.block_start, self.cells = self.position(), []

    def handle_data(self, data):
        self.text.append(data)

    def handle_endtag(self, tag):
        text = " ".join("".join(self.text).split())
        end = self.src.index(">", self.position()) + 1
        if tag == "title":
            self.title = text.split(" | ")[0]
        elif tag == "main":
            self.in_main = False
        elif not self.in_main:
            return
        elif tag == "h3":
            self.heading = text
        elif tag in ("td", "th"):
            self.cells.append((tag, text))
        elif tag == "tr" and all(t == "th" for t, _ in self.cells):
            self.headers = [v for _, v in self.cells]
        elif tag == "tr":
            row = table_row(self.headers, [v for _, v in self.cells])
            self.blocks.append((self.heading, make_line(self.src, self.block_start, end, row)))
        elif tag in ("p", "li") and text:
            self.blocks.append((self.heading, make_line(self.src, self.block_start, end, text)))


def load_html(src, path):
    parser = FaqParser(src)
    parser.feed(src)
    sections = {}
    for heading, line in parser.blocks:
        sections.setdefault(heading, []).append(line)
    doc = Path(path).stem
    return [Chunk(f"{doc}#{slug(h)}", path, f"{parser.title} › {h}", lines) for h, lines in sections.items()]


def load_csv(src, path):
    """Fee schedule: one chunk per row, so a citation points at the exact fee. Assumes no
    multi-line cells."""
    reader = csv.DictReader(io.StringIO(src))
    headers = [h.replace("_", " ") for h in reader.fieldnames]
    line_offsets = [0] + [m.end() for m in re.finditer("\n", src)]
    chunks = []
    for row in reader:
        start = line_offsets[reader.line_num - 1]
        end = src.find("\n", start)
        if end == -1:
            end = len(src)
        line = make_line(src, start, end, table_row(headers, list(row.values())))
        title = f"Fee and rate schedule › {row['item']} ({row['plan']})"
        chunks.append(Chunk(f"{Path(path).stem}#{row['fee_id']}", path, title, [line]))
    return chunks


LOADERS = {".md": load_markdown, ".html": load_html, ".csv": load_csv, ".txt": load_notice}


def load_corpus(root):
    chunks = []
    for path in sorted(Path(root).rglob("*")):
        if path.suffix in LOADERS:
            chunks += LOADERS[path.suffix](
                path.read_text(encoding="utf-8"), path.relative_to(root).as_posix()
            )
    return chunks
