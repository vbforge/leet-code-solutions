#!/usr/bin/env bash
# generate_pages.sh

BASE_SRC="src/main/java/com/vbforge"
REPO="${GITHUB_REPOSITORY:-your-username/leet-code-solutions}"
GITHUB_RAW_BASE="https://github.com/${REPO}/blob/main"

get_meta() {
  case "$1" in
    1)   echo "two-sum|Easy|Arrays & Hashing Basics" ;;
    9)   echo "palindrome-number|Easy|Math, Bits & Misc" ;;
    66)  echo "plus-one|Easy|Arrays & Hashing Basics" ;;
    121) echo "best-time-to-buy-and-sell-stock|Easy|Arrays & Hashing Basics" ;;
    217) echo "contains-duplicate|Easy|Arrays & Hashing Basics" ;;
    242) echo "valid-anagram|Easy|Arrays & Hashing Basics" ;;
    283) echo "move-zeroes|Easy|Arrays & Hashing Basics" ;;
    350) echo "intersection-of-two-arrays-ii|Easy|Arrays & Hashing Basics" ;;
    14)  echo "longest-common-prefix|Easy|Strings & Basic Logic" ;;
    125) echo "valid-palindrome|Easy|Strings & Basic Logic" ;;
    205) echo "isomorphic-strings|Easy|Strings & Basic Logic" ;;
    344) echo "reverse-string|Easy|Strings & Basic Logic" ;;
    383) echo "ransom-note|Easy|Strings & Basic Logic" ;;
    387) echo "first-unique-character-in-a-string|Easy|Strings & Basic Logic" ;;
    541) echo "reverse-string-ii|Easy|Strings & Basic Logic" ;;
    20)  echo "valid-parentheses|Easy|Stack, Queue & Linked Lists" ;;
    21)  echo "merge-two-sorted-lists|Easy|Stack, Queue & Linked Lists" ;;
    83)  echo "remove-duplicates-from-sorted-list|Easy|Stack, Queue & Linked Lists" ;;
    141) echo "linked-list-cycle|Easy|Stack, Queue & Linked Lists" ;;
    155) echo "min-stack|Medium|Stack, Queue & Linked Lists" ;;
    160) echo "intersection-of-two-linked-lists|Easy|Stack, Queue & Linked Lists" ;;
    234) echo "palindrome-linked-list|Easy|Stack, Queue & Linked Lists" ;;
    171) echo "excel-sheet-column-number|Easy|Math, Bits & Misc" ;;
    202) echo "happy-number|Easy|Math, Bits & Misc" ;;
    204) echo "count-primes|Medium|Math, Bits & Misc" ;;
    268) echo "missing-number|Easy|Math, Bits & Misc" ;;
    326) echo "power-of-three|Easy|Math, Bits & Misc" ;;
    412) echo "fizz-buzz|Easy|Math, Bits & Misc" ;;
    136) echo "single-number|Easy|Math, Bits & Misc" ;;
    169) echo "majority-element|Easy|Math, Bits & Misc" ;;
    461) echo "hamming-distance|Easy|Math, Bits & Misc" ;;
    *)   echo "$(echo "$2" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')|Easy|Uncategorized" ;;
  esac
}

PACKAGES=$(find "$BASE_SRC" -maxdepth 1 -type d -name 'p_*' \
  | sed 's|.*/||' \
  | sort -t_ -k2 -n)

total=0; solved=0
CARDS=""
SEEN_TAGS=""

while IFS= read -r pkg; do
  [ -z "$pkg" ] && continue
  total=$((total + 1))
  num=$(echo "$pkg" | cut -d_ -f2)
  raw=$(echo "$pkg" | cut -d_ -f3-)
  title="${raw//_/ }"
  meta=$(get_meta "$num" "$title")
  slug=$(echo "$meta" | cut -d'|' -f1)
  diff=$(echo "$meta" | cut -d'|' -f2)
  tag=$(echo "$meta" | cut -d'|' -f3)

  lc_url="https://leetcode.com/problems/${slug}/"
  sol_path="src/main/java/com/vbforge/${pkg}/Solution.java"

  case "$diff" in
    Easy)   dc="#00b8a3"; bg="#e0f8f5" ;;
    Medium) dc="#f0a500"; bg="#fff8e1" ;;
    Hard)   dc="#ef4743"; bg="#fdecea" ;;
    *)      dc="#888";    bg="#f0f0f0" ;;
  esac

  if [ -f "$BASE_SRC/$pkg/Solution.java" ]; then
    solved=$((solved + 1))
    status_txt="✅ Solved"; status_cls="solved"
    sol_btn="<a class=\"sol-btn\" href=\"${GITHUB_RAW_BASE}/${sol_path}\" target=\"_blank\">View Solution →</a>"
  else
    status_txt="⏳ In Progress"; status_cls="pending"
    sol_btn="<span class=\"sol-btn disabled\">No solution yet</span>"
  fi

  CARDS="${CARDS}
    <div class=\"card ${status_cls}\" data-tag=\"${tag}\" data-difficulty=\"${diff}\">
      <div class=\"card-header\" style=\"background:${bg}\">
        <span class=\"num\">#${num}</span>
        <span class=\"diff-badge\" style=\"background:${dc}\">${diff}</span>
      </div>
      <div class=\"card-body\">
        <a class=\"problem-title\" href=\"${lc_url}\" target=\"_blank\">${num}. ${title}</a>
        <span class=\"tag-pill\">${tag}</span>
        <div class=\"card-footer\">
          <span class=\"status ${status_cls}-txt\">${status_txt}</span>
          ${sol_btn}
        </div>
      </div>
    </div>"

  # Collect unique tags
  if ! echo "$SEEN_TAGS" | grep -qF "|${tag}|"; then
    SEEN_TAGS="${SEEN_TAGS}|${tag}|"
    TAG_BUTTONS="${TAG_BUTTONS:-}<button class=\"tag-btn\" data-tag=\"${tag}\" onclick=\"filterTag(this)\">${tag}</button>"
  fi
done <<< "$PACKAGES"

mkdir -p docs

cat > docs/index.html << HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>LeetCode Solutions — vbforge</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0d1117; color: #e6edf3; min-height: 100vh; }
    header { background: linear-gradient(135deg, #161b22 0%, #1f2937 100%); padding: 48px 24px 32px; text-align: center; border-bottom: 1px solid #30363d; }
    header h1 { font-size: 2.4rem; font-weight: 800; letter-spacing: -1px; }
    header h1 span { color: #58a6ff; }
    header p { color: #8b949e; margin-top: 8px; }
    .stats { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; padding: 28px 24px 0; }
    .stat { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 16px 28px; text-align: center; }
    .stat .val { font-size: 2rem; font-weight: 700; color: #58a6ff; }
    .stat .lbl { font-size: 0.78rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }
    .controls { max-width: 1200px; margin: 32px auto 0; padding: 0 24px; }
    input[type=search] { width: 100%; background: #161b22; border: 1px solid #30363d; border-radius: 8px; color: #e6edf3; padding: 10px 16px; font-size: 0.95rem; outline: none; margin-bottom: 16px; }
    input[type=search]:focus { border-color: #58a6ff; }
    .diff-filters, .tag-filters { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
    .diff-btn { cursor: pointer; border: 2px solid #30363d; border-radius: 20px; padding: 5px 16px; font-size: 0.82rem; font-weight: 600; background: #161b22; color: #8b949e; transition: all .2s; }
    .diff-btn[data-d=Easy].active   { background: #00b8a322; color:#00b8a3; border-color:#00b8a3; }
    .diff-btn[data-d=Medium].active { background: #f0a50022; color:#f0a500; border-color:#f0a500; }
    .diff-btn[data-d=Hard].active   { background: #ef474322; color:#ef4743; border-color:#ef4743; }
    .tag-btn { cursor: pointer; border: 1.5px solid #58a6ff; border-radius: 20px; padding: 4px 14px; font-size: 0.78rem; font-weight: 600; background: transparent; color: #58a6ff; transition: all .2s; }
    .tag-btn.active { background: #58a6ff; color: #0d1117; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; max-width: 1200px; margin: 24px auto 0; padding: 0 24px 48px; }
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; overflow: hidden; transition: transform .2s, box-shadow .2s; }
    .card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px #00000060; }
    .card.hidden { display: none; }
    .card-header { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; }
    .num { font-weight: 700; font-size: 0.9rem; color: #6e7681; }
    .diff-badge { font-size: 0.72rem; font-weight: 700; color: #fff; padding: 3px 10px; border-radius: 20px; }
    .card-body { padding: 12px 16px 16px; }
    .problem-title { display: block; font-weight: 600; font-size: 1rem; color: #e6edf3; text-decoration: none; margin-bottom: 8px; line-height: 1.4; }
    .problem-title:hover { color: #58a6ff; }
    .tag-pill { display: inline-block; font-size: 0.72rem; font-weight: 600; padding: 3px 10px; border-radius: 20px; margin-bottom: 12px; background: #58a6ff22; color: #58a6ff; }
    .card-footer { display: flex; justify-content: space-between; align-items: center; }
    .solved-txt { color: #3fb950; font-size: 0.8rem; font-weight: 600; }
    .pending-txt { color: #8b949e; font-size: 0.8rem; font-weight: 600; }
    .sol-btn { font-size: 0.8rem; font-weight: 600; color: #58a6ff; text-decoration: none; padding: 4px 10px; border: 1px solid #58a6ff33; border-radius: 6px; transition: background .2s; }
    .sol-btn:hover { background: #58a6ff22; }
    .sol-btn.disabled { color: #484f58; border-color: transparent; cursor: default; }
    footer { text-align: center; padding: 24px; color: #484f58; font-size: 0.82rem; border-top: 1px solid #21262d; }
    footer a { color: #58a6ff; text-decoration: none; }
  </style>
</head>
<body>
<header>
  <h1>Leet<span>Code</span> Solutions</h1>
  <p>vbforge · Auto-generated on every push · Java 21 + JUnit 5</p>
</header>
<div class="stats">
  <div class="stat"><div class="val">${solved}</div><div class="lbl">Solved</div></div>
  <div class="stat"><div class="val">${total}</div><div class="lbl">Total</div></div>
</div>
<div class="controls">
  <input type="search" id="searchInput" placeholder="Search problems…" oninput="applyFilters()"/>
  <div class="diff-filters">
    <button class="diff-btn" data-d="Easy" onclick="toggleDiff(this)">🟢 Easy</button>
    <button class="diff-btn" data-d="Medium" onclick="toggleDiff(this)">🟡 Medium</button>
    <button class="diff-btn" data-d="Hard" onclick="toggleDiff(this)">🔴 Hard</button>
  </div>
  <div class="tag-filters">${TAG_BUTTONS}</div>
</div>
<div class="grid" id="grid">${CARDS}</div>
<footer>
  Auto-generated by GitHub Actions ·
  <a href="https://github.com/${REPO}" target="_blank">View on GitHub →</a>
</footer>
<script>
  let activeTags = new Set(), activeDiffs = new Set();
  function filterTag(btn) {
    const tag = btn.dataset.tag; btn.classList.toggle('active');
    activeTags.has(tag) ? activeTags.delete(tag) : activeTags.add(tag); applyFilters();
  }
  function toggleDiff(btn) {
    const d = btn.dataset.d; btn.classList.toggle('active');
    activeDiffs.has(d) ? activeDiffs.delete(d) : activeDiffs.add(d); applyFilters();
  }
  function applyFilters() {
    const q = document.getElementById('searchInput').value.toLowerCase();
    document.querySelectorAll('.card').forEach(card => {
      const title = card.querySelector('.problem-title').textContent.toLowerCase();
      const ok = (!q || title.includes(q))
        && (activeTags.size === 0  || activeTags.has(card.dataset.tag))
        && (activeDiffs.size === 0 || activeDiffs.has(card.dataset.difficulty));
      card.classList.toggle('hidden', !ok);
    });
  }
</script>
</body>
</html>
HTML

echo "[OK] docs/index.html generated — ${total} problems, ${solved} solved."
