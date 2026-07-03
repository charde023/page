"""
blanks.py — detect fill-in-the-blank patterns in "오늘의공부" Day pages (sections ④⑤)
and replace them with HTML input/textarea elements carrying a unique data-key
for the client-side autosave script.

Observed blank shapes (verified against Day01~10 source verbatim):
  T1  Table cell blank         | ... | ______ |                (Day10 only)
  T2  Standalone blank line    ________________________________  (Day10 extra)
  M   Multi inline blank       - 라벨 — 서브라벨: ___ / 서브라벨: ___ / ...   (Day08 only)
  D   Em-dash + "답:" (same line, no blank run)   N. 라벨 — 답:   (Day03,06,07)
  J   Two-line "적어보기:"      - 질문...\n  적어보기: ___          (Day01)
  G   Generic single-line blank  (-|N.) 라벨[: 설명 →]? ______ (부가설명)?  (Day02,04,05,09)
  QA  ⑤ two-line 답:/결정:      N. 질문...(어떤 문장으로 끝나든)\n   답|결정:  (all days)

All patterns are tried in the order below; each consumed line is replaced with
an HTML block before the next pattern runs, so there is no double-matching.
"""

from __future__ import annotations

import html
import re

BULLET_OR_NUM = r"(?:-|\d+\.)"


def _field_html(day_num: int, section: int, slot: str, label: str, kind: str = "textarea",
                 hint: str = "") -> str:
    key = f"day{day_num:02d}_s{section}_{slot}"
    label_html = html.escape(label.strip())
    hint_html = f'<div class="field-hint">{html.escape(hint.strip())}</div>' if hint.strip() else ""
    if kind == "input":
        input_html = f'<input type="text" class="field-input" data-key="{key}">'
    else:
        input_html = f'<textarea class="field-input" data-key="{key}" rows="2"></textarea>'
    return (
        f'<div class="field">'
        f'<div class="field-label">{label_html}</div>'
        f'{hint_html}'
        f'{input_html}'
        f'<span class="save-status" data-for="{key}"></span>'
        f'</div>'
    )


# ---------------------------------------------------------------------------
# ⑤ section — universal two-line "답:"/"결정:" pattern (all 10 Days confirmed)
# ---------------------------------------------------------------------------

QA_TWOLINE = re.compile(
    r"^(?P<num>\d+)\.\s(?P<question>[^\n]+)\n[ \t]*(?P<label>답|결정)[:：]\s*$",
    re.MULTILINE,
)


def transform_section5(text: str, day_num: int) -> str:
    counter = {"a": 0}

    def repl(m: re.Match) -> str:
        label = m.group("label")
        question = html.escape(m.group("question").strip())
        num = m.group("num")
        if label == "결정":
            slot = "decision"
        else:
            counter["a"] += 1
            slot = f"a{counter['a']}"
        field = _field_html(day_num, 5, slot, label, kind="textarea")
        # Rendered as a self-contained HTML block (not markdown list syntax) so
        # each question keeps its own number instead of every fragment resetting
        # to "1." (markdown would otherwise treat each isolated "N. ..." line as
        # the start of a brand-new single-item <ol>).
        return (
            f'<div class="qa-block">'
            f'<div class="qa-question"><strong>{num}.</strong> {question}</div>'
            f'{field}'
            f'</div>'
        )

    return QA_TWOLINE.sub(repl, text)


# ---------------------------------------------------------------------------
# ④ section — table blanks (Day10)
# ---------------------------------------------------------------------------

TABLE_ROW = re.compile(r"^\|(?P<cells>.+)\|\s*$", re.MULTILINE)
SEP_ROW = re.compile(r"^\|[\s:|-]+\|\s*$")
BLANK_CELL = re.compile(r"^_{3,}$")


def _transform_table_blanks(text: str, day_num: int) -> str:
    lines = text.split("\n")
    out_lines = []
    row_idx = 0
    for line in lines:
        m = TABLE_ROW.match(line)
        if not m or SEP_ROW.match(line):
            out_lines.append(line)
            continue
        cells = m.group("cells").split("|")
        changed = False
        new_cells = []
        # Row label for the export feature: prefer the 2nd column (개념 name),
        # since table rows aren't wrapped in a .field-label div like other blanks.
        row_label = cells[1].strip() if len(cells) > 1 else f"행 {row_idx + 1}"
        for cell in cells:
            stripped = cell.strip()
            if BLANK_CELL.match(stripped):
                row_idx += 1
                key = f"day{day_num:02d}_s4_row{row_idx}"
                label_attr = html.escape(row_label, quote=True)
                new_cells.append(
                    f' <input type="text" class="field-input field-input-cell" '
                    f'data-key="{key}" data-label="{label_attr}">'
                    f'<span class="save-status" data-for="{key}"></span> '
                )
                changed = True
            else:
                new_cells.append(cell)
        if changed:
            out_lines.append("|" + "|".join(new_cells) + "|")
        else:
            out_lines.append(line)
    return "\n".join(out_lines)


# ---------------------------------------------------------------------------
# ④ section — standalone underscore-only line (Day10 extra blank)
# ---------------------------------------------------------------------------

STANDALONE_BLANK_LINE = re.compile(r"^_{6,}\s*$", re.MULTILINE)


def _transform_standalone_blank(text: str, day_num: int, counter: dict) -> str:
    def repl(m: re.Match) -> str:
        counter["extra"] = counter.get("extra", 0) + 1
        slot = "extra" if counter["extra"] == 1 else f"extra{counter['extra']}"
        return _field_html(day_num, 4, slot, "직접 적어보기", kind="textarea")

    return STANDALONE_BLANK_LINE.sub(repl, text)


# ---------------------------------------------------------------------------
# ④ section — Day08-only: bullet line with 2+ "/"-separated inline blanks
#   - 광고 증액 — 돈: ______ / 지속성: ______ / 브랜드: ______
# ---------------------------------------------------------------------------

MULTI_INLINE_LINE = re.compile(
    r"^-\s*(?P<mainlabel>[^\n]+?)\s*[—–-]\s*(?P<rest>[^\n]+_{3,}[^\n]*)\s*$",
    re.MULTILINE,
)
SUBFIELD = re.compile(r"(?P<sublabel>[^/]+?)[:：]\s*_{3,}")


def _transform_multi_inline(text: str, day_num: int, counter: dict) -> str:
    def repl(m: re.Match) -> str:
        rest = m.group("rest")
        subs = SUBFIELD.findall(rest)
        if len(subs) < 2:
            return m.group(0)  # not a multi-inline row; leave untouched
        mainlabel = m.group("mainlabel").strip()
        parts = []
        for sub in subs:
            counter["q"] = counter.get("q", 0) + 1
            key = f"day{day_num:02d}_s4_q{counter['q']}"
            sublabel = html.escape(sub.strip())
            parts.append(
                f'<label class="inline-field">'
                f'<span class="inline-field-label">{sublabel}</span>'
                f'<input type="text" class="field-input" data-key="{key}">'
                f'<span class="save-status" data-for="{key}"></span>'
                f'</label>'
            )
        inline_html = f'<div class="field-label">{html.escape(mainlabel)}</div><div class="inline-group">' + "".join(parts) + "</div>"
        return inline_html

    return MULTI_INLINE_LINE.sub(repl, text)


# ---------------------------------------------------------------------------
# ④ section — em-dash + "답:" on the same line, no blank run (Day03,06,07)
# ---------------------------------------------------------------------------

EMDASH_DAP_LINE = re.compile(
    rf"^{BULLET_OR_NUM}\s*(?P<label>[^\n]+?)\s*[—–-]\s*답[:：]\s*$",
    re.MULTILINE,
)


def _transform_emdash_dap(text: str, day_num: int, counter: dict) -> str:
    def repl(m: re.Match) -> str:
        counter["q"] = counter.get("q", 0) + 1
        slot = f"q{counter['q']}"
        return _field_html(day_num, 4, slot, m.group("label"), kind="textarea")

    return EMDASH_DAP_LINE.sub(repl, text)


# ---------------------------------------------------------------------------
# ④ section — two-line "적어보기:" pattern (Day01)
# ---------------------------------------------------------------------------

JEOKEOBOGI_TWOLINE = re.compile(
    r"^-\s*(?P<question>[^\n]+?)\n[ \t]*적어보기[:：]\s*_*\s*$",
    re.MULTILINE,
)


def _transform_jeokeobogi(text: str, day_num: int, counter: dict) -> str:
    def repl(m: re.Match) -> str:
        counter["q"] = counter.get("q", 0) + 1
        slot = f"q{counter['q']}"
        # Whole "- 질문...\n  적어보기: ___" block becomes one self-contained
        # field div (question as its label) — no leftover "- " bullet text, so
        # markdown won't wrap it in a spurious single-item <ul>.
        return _field_html(day_num, 4, slot, m.group("question"), kind="textarea")

    return JEOKEOBOGI_TWOLINE.sub(repl, text)


# ---------------------------------------------------------------------------
# ④ section — generic single-line "label ... _____ (trailing note)?" (Day02,04,05,09)
# ---------------------------------------------------------------------------

GENERIC_BLANK_LINE = re.compile(
    rf"^{BULLET_OR_NUM}\s*(?P<label>[^\n]+?)\s*_{{3,}}\s*(?P<trailing>\([^\n]*\))?\s*$",
    re.MULTILINE,
)


def _transform_generic_blank(text: str, day_num: int, counter: dict) -> str:
    def repl(m: re.Match) -> str:
        counter["q"] = counter.get("q", 0) + 1
        slot = f"q{counter['q']}"
        hint = m.group("trailing") or ""
        return _field_html(day_num, 4, slot, m.group("label"), kind="textarea", hint=hint)

    return GENERIC_BLANK_LINE.sub(repl, text)


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------

def transform_section4(text: str, day_num: int) -> str:
    counter: dict = {}
    text = _transform_table_blanks(text, day_num)
    text = _transform_multi_inline(text, day_num, counter)
    text = _transform_emdash_dap(text, day_num, counter)
    text = _transform_jeokeobogi(text, day_num, counter)
    text = _transform_generic_blank(text, day_num, counter)
    text = _transform_standalone_blank(text, day_num, counter)
    return text


WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def preprocess_wikilinks(text: str) -> str:
    def repl(m: re.Match) -> str:
        target = m.group(1).strip()
        display = (m.group(2) or target).strip()
        return (
            f'<span class="wikiterm" title="옵시디언 원노트: {html.escape(target)}">'
            f'{html.escape(display)}</span>'
        )

    return WIKILINK.sub(repl, text)
