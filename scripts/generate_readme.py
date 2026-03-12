#!/usr/bin/env python3
"""
generate_readme.py
Scans src/main/java/com/vbforge for problem packages and auto-generates README.md.

Package naming convention: p_{number}_{Problem_Name_With_Underscores}
e.g. p_1_Two_Sum, p_121_Best_Time_to_Buy_and_Sell_Stock
"""

import os
import re
import sys

# ── LeetCode metadata ────────────────────────────────────────────────────────
# Maps problem number → (url_slug, difficulty, tag)
# Extend this dict whenever you add a new category of problems.
PROBLEM_META = {
    1:   ("two-sum",                              "Easy",   "Arrays & Hashing Basics"),
    121: ("best-time-to-buy-and-sell-stock",       "Easy",   "Arrays & Hashing Basics"),
    242: ("valid-anagram",                         "Easy",   "Arrays & Hashing Basics"),
    217: ("contains-duplicate",                    "Easy",   "Arrays & Hashing Basics"),
    350: ("intersection-of-two-arrays-ii",         "Easy",   "Arrays & Hashing Basics"),
    283: ("move-zeroes",                           "Easy",   "Arrays & Hashing Basics"),
    66:  ("plus-one",                              "Easy",   "Arrays & Hashing Basics"),
    125: ("valid-palindrome",                      "Easy",   "Strings & Basic Logic"),
    344: ("reverse-string",                        "Easy",   "Strings & Basic Logic"),
    541: ("reverse-string-ii",                     "Easy",   "Strings & Basic Logic"),
    14:  ("longest-common-prefix",                 "Easy",   "Strings & Basic Logic"),
    387: ("first-unique-character-in-a-string",    "Easy",   "Strings & Basic Logic"),
    383: ("ransom-note",                           "Easy",   "Strings & Basic Logic"),
    205: ("isomorphic-strings",                    "Easy",   "Strings & Basic Logic"),
    20:  ("valid-parentheses",                     "Easy",   "Stack, Queue & Linked Lists"),
    155: ("min-stack",                             "Medium", "Stack, Queue & Linked Lists"),
    83:  ("remove-duplicates-from-sorted-list",    "Easy",   "Stack, Queue & Linked Lists"),
    21:  ("merge-two-sorted-lists",                "Easy",   "Stack, Queue & Linked Lists"),
    234: ("palindrome-linked-list",                "Easy",   "Stack, Queue & Linked Lists"),
    141: ("linked-list-cycle",                     "Easy",   "Stack, Queue & Linked Lists"),
    160: ("intersection-of-two-linked-lists",      "Easy",   "Stack, Queue & Linked Lists"),
    171: ("excel-sheet-column-number",             "Easy",   "Math, Bits & Misc"),
    412: ("fizz-buzz",                             "Easy",   "Math, Bits & Misc"),
    136: ("single-number",                         "Easy",   "Math, Bits & Misc"),
    169: ("majority-element",                      "Easy",   "Math, Bits & Misc"),
    326: ("power-of-three",                        "Easy",   "Math, Bits & Misc"),
    461: ("hamming-distance",                      "Easy",   "Math, Bits & Misc"),
    268: ("missing-number",                        "Easy",   "Math, Bits & Misc"),
    204: ("count-primes",                          "Medium", "Math, Bits & Misc"),
    202: ("happy-number",                          "Easy",   "Math, Bits & Misc"),
}

DIFFICULTY_EMOJI = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
BASE_SRC = os.path.join("src", "main", "java", "com", "vbforge")
LEETCODE_BASE = "https://leetcode.com/problems"
GITHUB_BASE = "src/main/java/com/vbforge"


def parse_packages(base_path: str) -> list[dict]:
    """Walk base_path and return sorted list of problem dicts."""
    problems = []
    if not os.path.isdir(base_path):
        print(f"[WARN] Source directory not found: {base_path}", file=sys.stderr)
        return problems

    pattern = re.compile(r"^p_(\d+)_(.+)$")
    for entry in os.scandir(base_path):
        if not entry.is_dir():
            continue
        m = pattern.match(entry.name)
        if not m:
            continue

        num = int(m.group(1))
        raw_name = m.group(2)           # e.g. "Two_Sum"
        title = raw_name.replace("_", " ")  # e.g. "Two Sum"

        solution_rel = f"{GITHUB_BASE}/{entry.name}/Solution.java"
        solution_exists = os.path.isfile(os.path.join(base_path, entry.name, "Solution.java"))

        meta = PROBLEM_META.get(num, {})
        url_slug = meta.get(0) if isinstance(meta, tuple) else None

        # Unpack tuple if present
        if isinstance(meta, tuple) and len(meta) == 3:
            url_slug, difficulty, tag = meta
        else:
            url_slug   = title.lower().replace(" ", "-")
            difficulty = "Easy"
            tag        = "Uncategorized"

        problems.append({
            "num":       num,
            "title":     title,
            "url":       f"{LEETCODE_BASE}/{url_slug}/",
            "difficulty": difficulty,
            "tag":       tag,
            "solution":  solution_rel if solution_exists else None,
            "solved":    solution_exists,
        })

    problems.sort(key=lambda p: p["num"])
    return problems


def build_readme(problems: list[dict]) -> str:
    solved   = sum(1 for p in problems if p["solved"])
    total    = len(problems)
    easy     = sum(1 for p in problems if p["difficulty"] == "Easy")
    medium   = sum(1 for p in problems if p["difficulty"] == "Medium")
    hard     = sum(1 for p in problems if p["difficulty"] == "Hard")

    lines = [
        "# LeetCode Solutions — vbforge\n",
        "> 🤖 *This file is auto-generated by GitHub Actions. Do not edit manually.*\n",
        "## 📊 Progress\n",
        f"![Solved](https://img.shields.io/badge/Solved-{solved}-brightgreen)",
        f"![Total](https://img.shields.io/badge/Total-{total}-blue)",
        f"![Easy](https://img.shields.io/badge/Easy-{easy}-green)",
        f"![Medium](https://img.shields.io/badge/Medium-{medium}-yellow)",
        f"![Hard](https://img.shields.io/badge/Hard-{hard}-red)\n",
        "## 📋 Problem List\n",
        "#### Legend: ✅ solved · ⏳ in-progress\n",
        "| # | Problem | Difficulty | Status | Tag | Solution |",
        "|---|---------|------------|--------|-----|----------|",
    ]

    for i, p in enumerate(problems, 1):
        diff_icon = DIFFICULTY_EMOJI.get(p["difficulty"], "")
        status    = "✅" if p["solved"] else "⏳"
        sol_link  = f"[Solution.java]({p['solution']})" if p["solution"] else "—"
        prob_link = f"[{p['num']}. {p['title']}]({p['url']})"
        lines.append(
            f"| {i} | {prob_link} | {diff_icon} {p['difficulty']} | {status} | {p['tag']} | {sol_link} |"
        )

    lines += [
        "",
        "---",
        f"*Auto-generated. {solved}/{total} problems solved.*",
    ]
    return "\n".join(lines) + "\n"


def main():
    problems = parse_packages(BASE_SRC)
    if not problems:
        print("[INFO] No problem packages found. Writing empty README.")

    readme = build_readme(problems)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"[OK] README.md generated — {len(problems)} problems found.")


if __name__ == "__main__":
    main()
