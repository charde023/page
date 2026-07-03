#!/usr/bin/env python3
"""
generate.py — convert one 오늘의공부 Day0N_*.md file into study-anmok/dayNN/index.html.

Usage:
    python3 generate.py --md <path/to/DayNN_*.md> [--repo /Users/charde023/workspace/page]
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import markdown  # type: ignore[import]

from frontmatter import split_frontmatter
from blanks import transform_section4, transform_section5, preprocess_wikilinks
from template import CSS, AUTOSAVE_JS, PAGE_TEMPLATE, INDEX_TEMPLATE, CARD_TEMPLATE

H2_SPLIT = re.compile(r"^## ([①②③④⑤])[^\n]*\n", re.MULTILINE)
H2_HEADING_LINE = re.compile(r"^## ([①②③④⑤])([^\n]*)$", re.MULTILINE)
ONELINER_RE = re.compile(r"^>\s*오늘의 한 문장:\s*(.+)$", re.MULTILINE)
NUM_MAP = {"①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5}


def split_sections(body: str) -> dict[int, str]:
    marks = list(H2_SPLIT.finditer(body))
    sections: dict[int, str] = {}
    for i, m in enumerate(marks):
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        sections[NUM_MAP[m.group(1)]] = body[start:end]
    return sections


def section_headings(body: str) -> dict[int, str]:
    headings = {}
    for m in H2_HEADING_LINE.finditer(body):
        headings[NUM_MAP[m.group(1)]] = m.group(1) + m.group(2)
    return headings


def md_to_html(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code"])


def build_page(md_path: Path, all_days: list[int]) -> tuple[int, str]:
    raw = md_path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(raw)
    day_num = int(meta["Day"])

    oneliner_m = ONELINER_RE.search(body)
    oneliner = oneliner_m.group(1).strip() if oneliner_m else ""

    body = preprocess_wikilinks(body)
    headings = section_headings(body)
    sections = split_sections(body)

    sections[4] = transform_section4(sections[4], day_num)
    sections[5] = transform_section5(sections[5], day_num)

    parts = []
    for n in (1, 2, 3, 4, 5):
        heading_text = headings.get(n, str(n))
        parts.append(f"## {heading_text}\n\n{sections.get(n, '')}")
    full_md = "\n\n".join(parts)
    body_html = md_to_html(full_md)

    title = f"Day {day_num:02d} · {meta.get('주제', '')}"
    h1 = f"Day {day_num:02d} · {meta.get('주제', '')}"
    genre = meta.get("장르", "")
    anmok = meta.get("안목", "")

    idx = all_days.index(day_num)
    prev_link = (
        f'<a href="../day{all_days[idx-1]:02d}/">← Day {all_days[idx-1]:02d}</a>'
        if idx > 0 else "<span></span>"
    )
    next_link = (
        f'<a href="../day{all_days[idx+1]:02d}/">Day {all_days[idx+1]:02d} →</a>'
        if idx < len(all_days) - 1 else "<span></span>"
    )

    date_key = f"day{day_num:02d}_frontmatter_date"

    page = PAGE_TEMPLATE
    page = page.replace("__TITLE__", html.escape(title))
    page = page.replace("__DESCRIPTION__", html.escape(oneliner))
    page = page.replace("__H1__", html.escape(h1))
    page = page.replace("__GENRE__", html.escape(genre))
    page = page.replace("__ANMOK__", html.escape(anmok))
    page = page.replace("__ONELINER__", html.escape(oneliner))
    page = page.replace("__DATEKEY__", date_key)
    page = page.replace("__BODY__", body_html)
    page = page.replace("__PREV_LINK__", prev_link)
    page = page.replace("__NEXT_LINK__", next_link)
    page = page.replace("__CSS__", CSS)
    page = page.replace("__AUTOSAVE_JS__", AUTOSAVE_JS)

    return day_num, page


def build_index(md_paths: list[Path], repo: Path) -> str:
    cards = []
    for md_path in md_paths:
        raw = md_path.read_text(encoding="utf-8")
        meta, body = split_frontmatter(raw)
        day_num = int(meta["Day"])
        oneliner_m = ONELINER_RE.search(body)
        oneliner = oneliner_m.group(1).strip() if oneliner_m else ""
        card = CARD_TEMPLATE
        card = card.replace("__HREF__", f"day{day_num:02d}")
        card = card.replace("__TITLE__", html.escape(f"Day {day_num:02d} · {meta.get('주제', '')}"))
        card = card.replace("__GENRE__", html.escape(meta.get("장르", "")))
        card = card.replace("__ANMOK__", html.escape(meta.get("안목", "")))
        card = card.replace("__ONELINER__", html.escape(oneliner))
        cards.append((day_num, card))
    cards.sort(key=lambda x: x[0])

    idx = INDEX_TEMPLATE
    idx = idx.replace("__COUNT__", str(len(cards)))
    idx = idx.replace("__CARDS__", "\n".join(c for _, c in cards))
    idx = idx.replace("__CSS__", CSS)
    return idx


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", help="path to a single Day0N_*.md")
    ap.add_argument("--md-glob", help="glob pattern for multiple Day0N_*.md files")
    ap.add_argument("--repo", default="/Users/charde023/workspace/page")
    ap.add_argument("--all-days", default="1,2,3,4,5,6,7,8,9,10",
                     help="comma-separated day numbers, for prev/next nav")
    ap.add_argument("--build-index", action="store_true",
                     help="also (re)build study-anmok/index.html from --md-glob")
    args = ap.parse_args()

    all_days = [int(x) for x in args.all_days.split(",")]
    repo = Path(args.repo)

    md_paths: list[Path] = []
    if args.md:
        md_paths = [Path(args.md)]
    elif args.md_glob:
        import glob as globmod
        md_paths = [Path(p) for p in sorted(globmod.glob(args.md_glob))]
        # Only keep files whose frontmatter Day number is in --all-days (the
        # vault also contains Day11+ pages from other work; this pilot is
        # scoped to Day01~10 only).
        filtered = []
        for p in md_paths:
            meta, _ = split_frontmatter(p.read_text(encoding="utf-8"))
            if meta.get("Day", "").strip() and int(meta["Day"]) in all_days:
                filtered.append(p)
        md_paths = filtered

    for md_path in md_paths:
        day_num, page_html = build_page(md_path, all_days)
        out_dir = repo / "study-anmok" / f"day{day_num:02d}"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "index.html"
        out_path.write_text(page_html, encoding="utf-8")
        n_fields = len(re.findall(r'data-key="[^"]+"', page_html))
        print(f"generated {out_path} ({n_fields} input fields)")

    if args.build_index and md_paths:
        idx_html = build_index(md_paths, repo)
        idx_path = repo / "study-anmok" / "index.html"
        idx_path.write_text(idx_html, encoding="utf-8")
        print(f"generated {idx_path}")


if __name__ == "__main__":
    main()
