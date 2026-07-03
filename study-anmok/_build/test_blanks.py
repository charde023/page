"""Scratch test: run blanks.py transforms against real Day01~10 files and report field counts."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from frontmatter import split_frontmatter
from blanks import transform_section4, transform_section5, preprocess_wikilinks

VAULT_DAYS = Path("/Users/charde023/workspace/obsidian/charde_n/.claude/worktrees/magical-golick-6c950a/오늘의공부")

EXPECTED = {
    1: (3, 3), 2: (4, 3), 3: (3, 3), 4: (4, 3), 5: (4, 3),
    6: (3, 3), 7: (3, 3), 8: (10, 3), 9: (4, 3), 10: (11, 3),
}

H2_SPLIT = re.compile(r"^## ([①②③④⑤])[^\n]*\n", re.MULTILINE)


def split_sections(body: str) -> dict:
    marks = list(H2_SPLIT.finditer(body))
    sections = {}
    nummap = {"①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5}
    for i, m in enumerate(marks):
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        sections[nummap[m.group(1)]] = body[start:end]
    return sections


ok = True
for md_path in sorted(VAULT_DAYS.glob("Day*.md")):
    m = re.match(r"Day(\d+)_", md_path.name)
    if not m:
        continue
    day_num = int(m.group(1))
    if day_num not in EXPECTED:
        continue
    text = md_path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)
    body = preprocess_wikilinks(body)
    sections = split_sections(body)
    s4 = transform_section4(sections[4], day_num)
    s5 = transform_section5(sections[5], day_num)
    got4 = len(re.findall(r'data-key="[^"]+"', s4))
    got5 = len(re.findall(r'data-key="[^"]+"', s5))
    exp4, exp5 = EXPECTED[day_num]
    status = "OK" if (got4, got5) == (exp4, exp5) else "MISMATCH"
    if status == "MISMATCH":
        ok = False
    print(f"Day{day_num:02d}: s4 got={got4} exp={exp4} | s5 got={got5} exp={exp5}  [{status}]")
    if status == "MISMATCH":
        print("--- s4 leftover blanks-looking lines ---")
        for line in sections[4].split("\n"):
            if "___" in line or "적어보기" in line or re.search(r"—\s*답[:：]\s*$", line):
                print("   SRC:", line)
        print("--- s4 rendered (first 2000 chars) ---")
        print(s4[:2000])

print("\nALL OK" if ok else "\nSOME MISMATCHES ABOVE")
