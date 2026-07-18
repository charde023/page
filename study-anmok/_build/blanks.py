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

# Any non-empty line immediately followed by a line that is just "답:" or
# "결정:". Covers numbered questions ("1. ...\n답:"), bold decision prompts
# ("**오늘 내릴 작은 결정**: ...\n결정:"), and essay M16 questions — the format
# varies across Day11~72.
GENERIC_QA = re.compile(
    r"^(?P<qline>[^\n]+)\n[ \t]*(?P<label>답|결정)[:：]\s*$",
    re.MULTILINE,
)


def _qa_block(day_num: int, section: int, slot: str, label: str, qline: str) -> str:
    qtext = html.escape(qline.strip().replace("**", ""))
    field = _field_html(day_num, section, slot, label, kind="textarea")
    return f'<div class="qa-block"><div class="qa-question">{qtext}</div>{field}</div>'


def transform_section5(text: str, day_num: int) -> str:
    counter = {"a": 0}

    def repl(m: re.Match) -> str:
        label = m.group("label")
        if label == "결정":
            slot = "decision"
        else:
            counter["a"] += 1
            slot = f"a{counter['a']}"
        return _qa_block(day_num, 5, slot, label, m.group("qline"))

    return GENERIC_QA.sub(repl, text)


# ---------------------------------------------------------------------------
# ④ section — table blanks (Day10)
# ---------------------------------------------------------------------------

TABLE_ROW = re.compile(r"^\|(?P<cells>.+)\|\s*$", re.MULTILINE)
SEP_ROW = re.compile(r"^\|[\s:|-]+\|\s*$")
BLANK_RUN = re.compile(r"_{3,}")


def _transform_table_blanks(text: str, day_num: int) -> str:
    lines = text.split("\n")
    out_lines = []
    counter = {"row": 0}
    headers: list[str] = []
    saw_header = False
    for line in lines:
        m = TABLE_ROW.match(line)
        if not m:
            out_lines.append(line)
            headers, saw_header = [], False  # table ended
            continue
        if SEP_ROW.match(line):
            out_lines.append(line)
            saw_header = True
            continue
        cells = m.group("cells").split("|")
        if not saw_header and not headers:
            # First row of a table is the header — capture column names for
            # the export labels (rows aren't wrapped in a .field-label div).
            headers = [c.strip() for c in cells]
            out_lines.append(line)
            continue
        new_cells = []
        changed = False
        for ci, cell in enumerate(cells):
            if BLANK_RUN.search(cell):
                col_label = headers[ci].strip() if ci < len(headers) and headers[ci].strip() else "표 입력"

                def sub_run(_m: re.Match) -> str:
                    counter["row"] += 1
                    key = f"day{day_num:02d}_s4_row{counter['row']}"
                    return (
                        f'<input type="text" class="field-input field-input-cell" '
                        f'data-key="{key}" data-label="{html.escape(col_label, quote=True)}">'
                        f'<span class="save-status" data-for="{key}"></span>'
                    )

                new_cells.append(BLANK_RUN.sub(sub_run, cell))
                changed = True
            else:
                new_cells.append(cell)
        out_lines.append(("|" + "|".join(new_cells) + "|") if changed else line)
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
DAYNUM_RE = re.compile(r"^Day(\d+)_")


def preprocess_wikilinks(text: str) -> str:
    def repl(m: re.Match) -> str:
        target = m.group(1).strip()
        display = (m.group(2) or target).strip()
        dm = DAYNUM_RE.match(target)
        if dm:
            # Links to other Day pages are internal to study-anmok → clickable.
            n = int(dm.group(1))
            return f'<a class="daylink" href="../day{n:02d}/">{html.escape(display)}</a>'
        # Links to 학습노트 (not published here) → non-clickable styled term.
        return (
            f'<span class="wikiterm" title="옵시디언 원노트: {html.escape(target)}">'
            f'{html.escape(display)}</span>'
        )

    return WIKILINK.sub(repl, text)


# ---------------------------------------------------------------------------
# Essay pages (Day17/24/31/38/43/50/57/61/67/72) — different structure:
#   ① 복습(Day링크) ② 주제후보/총복기표 ③ 캐묻기 ④ 쓰는 곳 + 체크박스/M16.
# Interactive elements are spread across sections, so essays are transformed as
# a whole-section pass rather than the ④/⑤-specific passes.
# ---------------------------------------------------------------------------

CHECKBOX_LINE = re.compile(r"^-\s*\[ ?\]\s*(?P<label>.+?)\s*$", re.MULTILINE)
ESSAY_WRITE_LINE = re.compile(
    r"^\*{0,2}(?P<label>오늘의 논제|논제|본문|주제|논증)[:：]\*{0,2}\s*$",
    re.MULTILINE,
)


def _essay_field(day_num: int, slot: str, label: str, kind: str) -> str:
    key = f"day{day_num:02d}_essay_{slot}"
    label_html = html.escape(label.strip())
    if kind == "input":
        inp = f'<input type="text" class="field-input" data-key="{key}">'
    elif kind == "big":
        inp = f'<textarea class="field-input field-input-big" data-key="{key}" rows="10"></textarea>'
    else:
        inp = f'<textarea class="field-input" data-key="{key}" rows="2"></textarea>'
    return (
        f'<div class="field"><div class="field-label">{label_html}</div>{inp}'
        f'<span class="save-status" data-for="{key}"></span></div>'
    )


def transform_essay(text: str, day_num: int) -> str:
    counter = {"q": 0, "w": 0, "c": 0}

    # 1. 총복기 표 빈칸 (일부 에세이의 ②)
    text = _transform_table_blanks(text, day_num)

    # 2. 쓰는 곳 프롬프트: 오늘의 논제/주제 → 한 줄, 본문/논증 → 큰 칸
    def wrepl(m: re.Match) -> str:
        label = m.group("label")
        counter["w"] += 1
        if label in ("본문", "논증"):
            return _essay_field(day_num, f"body{counter['w']}", label, "big")
        return _essay_field(day_num, f"topic{counter['w']}", label, "input")

    text = ESSAY_WRITE_LINE.sub(wrepl, text)

    # 3. M16/후속 질문 (질문\n   답:)
    def qrepl(m: re.Match) -> str:
        counter["q"] += 1
        qtext = html.escape(m.group("qline").strip().replace("**", ""))
        field = _essay_field(day_num, f"q{counter['q']}", m.group("label"), "textarea")
        return f'<div class="qa-block"><div class="qa-question">{qtext}</div>{field}</div>'

    text = GENERIC_QA.sub(qrepl, text)

    # 4. M23/M16 체크박스
    def crepl(m: re.Match) -> str:
        counter["c"] += 1
        key = f"day{day_num:02d}_essay_chk{counter['c']}"
        label = html.escape(m.group("label"))
        return (
            f'<label class="checkfield"><input type="checkbox" data-key="{key}">'
            f'<span>{label}</span></label>'
        )

    text = CHECKBOX_LINE.sub(crepl, text)
    return text


# ---------------------------------------------------------------------------
# ⑥ section — 생각의 꼬리 (차드 ↔ 시그마) persistent dialogue.
#
# Unlike ④⑤, this is NOT a localStorage input field. It is committed text
# mirrored from the vault note, so it reads identically on phone and PC and
# survives cache-clears. Turns are delimited by a bold-ONLY marker line whose
# first word is 차드 or 시그마:
#     **차드 · 2026-07-06 — 오늘 내 답**
#     **시그마 — 코치 노트**
#     **차드 — 이어서 (여기 적기)**
# Everything up to the next marker (or the end) is that turn's body, rendered
# as ordinary markdown. A marker mentioning "이어서" becomes a dashed "your turn"
# block. Any preamble before the first marker is kept as-is.
# ---------------------------------------------------------------------------

DIALOGUE_MARKER = re.compile(
    r"^\*\*\s*(?P<label>(?P<who>차드|시그마|스미스)[^*\n]*)\*\*\s*$",
    re.MULTILINE,
)


def transform_dialogue(text: str, day_num: int) -> str:
    import markdown  # local import; markdown is a generate.py dependency

    def render(md: str) -> str:
        return markdown.markdown(md.strip(), extensions=["tables", "fenced_code"])

    markers = list(DIALOGUE_MARKER.finditer(text))
    if not markers:
        return text  # nothing to structure — leave the section untouched

    preamble = text[: markers[0].start()].strip()
    turns = []
    for i, m in enumerate(markers):
        label = m.group("label").strip()
        who = m.group("who")
        body_end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
        body = text[m.end():body_end].strip()
        role = "next" if "이어서" in label else ("sigma" if who in ("시그마", "스미스") else "chad")
        body_html = render(body) if body else ""
        # "이어서" 턴은 정적 안내문 아래에 실제 입력란(textarea)을 단다. 자동저장
        # (data-key)이 걸려 있어 하단 "답변 내보내기" 버튼에 자동 포함된다. 웹에서
        # 바로 이어 쓰고 export로 복사해 시그마에게 주면 볼트 ⑥에 영구 기록된다.
        # key 접미사에 마커 개수를 써서 대화가 길어지면 새 입력칸이 신선해진다
        # (이전 라운드 초안이 새 칸에 되살아나지 않도록).
        extra = ""
        if role == "next":
            key = f"day{day_num:02d}_tail{len(markers)}"
            extra = (
                f'<textarea class="field-input" data-key="{key}" rows="4" '
                f'data-label="⑥ 생각의 꼬리 — 차드 이어서" '
                f"placeholder=\"여기에 이어서 써 — 이 기기에 자동 저장돼. 영구 기록은 아래 '답변 내보내기'로 복사해 시그마에게 주면 볼트에 박아줄게.\"></textarea>"
                f'<span class="save-status" data-for="{key}"></span>'
            )
        turns.append(
            f'<div class="turn turn-{role}">'
            f'<div class="turn-who">{html.escape(label)}</div>'
            f'{body_html}'
            f'{extra}'
            f'</div>'
        )
    block = '<div class="dialogue">' + "".join(turns) + "</div>"
    return (preamble + "\n\n" + block) if preamble else block
