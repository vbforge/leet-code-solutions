#!/usr/bin/env python3
"""
generate_pages.py
Generates docs/index.html — a polished GitHub Pages site listing all solved problems.
"""

import os
import re
import sys
from generate_readme import parse_packages, PROBLEM_META  # reuse parsing logic

BASE_SRC = os.path.join("src", "main", "java", "com", "vbforge")
DOCS_DIR = "docs"
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "your-username/your-repo")
GITHUB_PAGES_BASE = f"https://github.com/{GITHUB_REPO}/blob/main"

DIFFICULTY_COLOR = {
    "Easy":   ("#00b8a3", "#e0f8f5"),
    "Medium": ("#f0a500", "#fff8e1"),
    "Hard":   ("#ef4743", "#fdecea"),
}

TAG_COLORS = [
    "#4f8ef7", "#a259f7", "#f75990", "#f7a259",
    "#59f7a2", "#59d4f7", "#f7f759", "#7ef759",
]

def tag_color(tag: str) -> str:
    return TAG_COLORS[hash(tag) % len(TAG_COLORS)]


def build_html(problems: list[dict]) -> str:
    solved = sum(1 for p in problems if p["solved"])
    total  = len(problems)

    tags = sorted(set(p["tag"] for p in problems))

    # Build tag filter buttons
    tag_buttons = '\n'.join(
        f'<button class="tag-btn" data-tag="{t}" style="--tc:{tag_color(t)}" onclick="filterTag(this)">{t}</button>'
        for t in tags
    )

    # Build problem cards
    cards = []
    for p in problems:
        dc, bg = DIFFICULTY_COLOR.get(p["difficulty"], ("#888", "#f0f0f0"))
        status_cls = "solved" if p["solved"] else "pending"
        status_txt = "✅ Solved" if p["solved"] else "⏳ In Progress"
        sol_btn = (
            f'<a class="sol-btn" href="{GITHUB_PAGES_BASE}/{p["solution"]}" target="_blank">View Solution →</a>'
            if p["solution"] else '<span class="sol-btn disabled">No solution yet</span>'
        )
        cards.append(f"""
        <div class="card {status_cls}" data-tag="{p['tag']}" data-difficulty="{p['difficulty']}">
          <div class="card-header" style="background:{bg}">
            <span class="num">#{p['num']}</span>
            <span class="diff-badge" style="background:{dc}">{p['difficulty']}</span>
          </div>
          <div class="card-body">
            <a class="problem-title" href="{p['url']}" target="_blank">{p['title']}</a>
            <span class="tag-pill" style="background:{tag_color(p['tag'])}22;color:{tag_color(p['tag'])}">{p['tag']}</span>
            <div class="card-footer">
              <span class="status {status_cls}-txt">{status_txt}</span>
              {sol_btn}
            </div>
          </div>
        </div>""")

    cards_html = "\n".join(cards)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>LeetCode Solutions — vbforge</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0d1117; color: #e6edf3; min-height: 100vh; }}

    header {{ background: linear-gradient(135deg, #161b22 0%, #1f2937 100%); padding: 48px 24px 32px; text-align: center; border-bottom: 1px solid #30363d; }}
    header h1 {{ font-size: 2.4rem; font-weight: 800; letter-spacing: -1px; }}
    header h1 span {{ color: #58a6ff; }}
    header p {{ color: #8b949e; margin-top: 8px; font-size: 1rem; }}

    .stats {{ display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; padding: 28px 24px 0; }}
    .stat {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 16px 28px; text-align: center; }}
    .stat .val {{ font-size: 2rem; font-weight: 700; color: #58a6ff; }}
    .stat .lbl {{ font-size: 0.78rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }}

    .controls {{ max-width: 1200px; margin: 32px auto 0; padding: 0 24px; }}
    .search-row {{ display: flex; gap: 12px; flex-wrap: wrap; align-items: center; margin-bottom: 16px; }}
    input[type=search] {{ flex: 1; min-width: 200px; background: #161b22; border: 1px solid #30363d; border-radius: 8px;
      color: #e6edf3; padding: 10px 16px; font-size: 0.95rem; outline: none; }}
    input[type=search]:focus {{ border-color: #58a6ff; }}
    .diff-filters {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .diff-btn {{ cursor: pointer; border: 2px solid transparent; border-radius: 20px; padding: 5px 16px;
      font-size: 0.82rem; font-weight: 600; background: #161b22; color: #8b949e; transition: all .2s; }}
    .diff-btn:hover, .diff-btn.active {{ border-color: currentColor; color: #e6edf3; }}
    .diff-btn[data-d=Easy]  {{ --c: #00b8a3; }} .diff-btn[data-d=Easy].active  {{ background: #00b8a322; color:#00b8a3; border-color:#00b8a3; }}
    .diff-btn[data-d=Medium]{{ --c: #f0a500; }} .diff-btn[data-d=Medium].active{{ background: #f0a50022; color:#f0a500; border-color:#f0a500; }}
    .diff-btn[data-d=Hard]  {{ --c: #ef4743; }} .diff-btn[data-d=Hard].active  {{ background: #ef474322; color:#ef4743; border-color:#ef4743; }}

    .tag-filters {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; }}
    .tag-btn {{ cursor: pointer; border: 1.5px solid var(--tc); border-radius: 20px; padding: 4px 14px;
      font-size: 0.78rem; font-weight: 600; background: transparent; color: var(--tc); transition: all .2s; }}
    .tag-btn:hover, .tag-btn.active {{ background: var(--tc); color: #0d1117; }}

    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px;
      max-width: 1200px; margin: 0 auto; padding: 0 24px 48px; }}

    .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; overflow: hidden;
      transition: transform .2s, box-shadow .2s; }}
    .card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 24px #00000060; }}
    .card.hidden {{ display: none; }}

    .card-header {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; }}
    .num {{ font-weight: 700; font-size: 0.9rem; color: #6e7681; }}
    .diff-badge {{ font-size: 0.72rem; font-weight: 700; color: #fff; padding: 3px 10px; border-radius: 20px; }}

    .card-body {{ padding: 12px 16px 16px; }}
    .problem-title {{ display: block; font-weight: 600; font-size: 1rem; color: #e6edf3; text-decoration: none;
      margin-bottom: 8px; line-height: 1.4; }}
    .problem-title:hover {{ color: #58a6ff; }}
    .tag-pill {{ display: inline-block; font-size: 0.72rem; font-weight: 600; padding: 3px 10px;
      border-radius: 20px; margin-bottom: 12px; }}

    .card-footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 4px; }}
    .status {{ font-size: 0.8rem; font-weight: 600; }}
    .solved-txt {{ color: #3fb950; }}
    .pending-txt {{ color: #8b949e; }}
    .sol-btn {{ font-size: 0.8rem; font-weight: 600; color: #58a6ff; text-decoration: none; padding: 4px 10px;
      border: 1px solid #58a6ff33; border-radius: 6px; transition: background .2s; }}
    .sol-btn:hover {{ background: #58a6ff22; }}
    .sol-btn.disabled {{ color: #484f58; border-color: transparent; cursor: default; }}

    footer {{ text-align: center; padding: 24px; color: #484f58; font-size: 0.82rem; border-top: 1px solid #21262d; }}
    footer a {{ color: #58a6ff; text-decoration: none; }}
  </style>
</head>
<body>

<header>
  <h1>Leet<span>Code</span> Solutions</h1>
  <p>vbforge · Auto-generated on every push · Java 21 + JUnit 5</p>
</header>

<div class="stats">
  <div class="stat"><div class="val">{solved}</div><div class="lbl">Solved</div></div>
  <div class="stat"><div class="val">{total}</div><div class="lbl">Total</div></div>
  <div class="stat"><div class="val">{sum(1 for p in problems if p['difficulty']=='Easy' and p['solved'])}</div><div class="lbl">Easy ✓</div></div>
  <div class="stat"><div class="val">{sum(1 for p in problems if p['difficulty']=='Medium' and p['solved'])}</div><div class="lbl">Medium ✓</div></div>
  <div class="stat"><div class="val">{sum(1 for p in problems if p['difficulty']=='Hard' and p['solved'])}</div><div class="lbl">Hard ✓</div></div>
</div>

<div class="controls">
  <div class="search-row">
    <input type="search" id="searchInput" placeholder="Search problems…" oninput="applyFilters()"/>
    <div class="diff-filters">
      <button class="diff-btn" data-d="Easy"   onclick="toggleDiff(this)">🟢 Easy</button>
      <button class="diff-btn" data-d="Medium" onclick="toggleDiff(this)">🟡 Medium</button>
      <button class="diff-btn" data-d="Hard"   onclick="toggleDiff(this)">🔴 Hard</button>
    </div>
  </div>
  <div class="tag-filters">
    {tag_buttons}
  </div>
</div>

<div class="grid" id="grid">
  {cards_html}
</div>

<footer>
  Auto-generated by GitHub Actions ·
  <a href="https://github.com/{GITHUB_REPO}" target="_blank">View on GitHub →</a>
</footer>

<script>
  let activeTags = new Set();
  let activeDiffs = new Set();

  function filterTag(btn) {{
    const tag = btn.dataset.tag;
    btn.classList.toggle('active');
    activeTags.has(tag) ? activeTags.delete(tag) : activeTags.add(tag);
    applyFilters();
  }}

  function toggleDiff(btn) {{
    const d = btn.dataset.d;
    btn.classList.toggle('active');
    activeDiffs.has(d) ? activeDiffs.delete(d) : activeDiffs.add(d);
    applyFilters();
  }}

  function applyFilters() {{
    const q = document.getElementById('searchInput').value.toLowerCase();
    document.querySelectorAll('.card').forEach(card => {{
      const title = card.querySelector('.problem-title').textContent.toLowerCase();
      const tag   = card.dataset.tag;
      const diff  = card.dataset.difficulty;
      const matchSearch = !q || title.includes(q);
      const matchTag    = activeTags.size === 0 || activeTags.has(tag);
      const matchDiff   = activeDiffs.size === 0 || activeDiffs.has(diff);
      card.classList.toggle('hidden', !(matchSearch && matchTag && matchDiff));
    }});
  }}
</script>
</body>
</html>
"""


def main():
    problems = parse_packages(BASE_SRC)
    os.makedirs(DOCS_DIR, exist_ok=True)
    html = build_html(problems)
    out = os.path.join(DOCS_DIR, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] {out} generated — {len(problems)} problems.")


if __name__ == "__main__":
    main()
