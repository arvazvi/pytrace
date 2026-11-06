#!/usr/bin/env python3
"""Generate PyTrace's static content pages (examples, about) and sitemap.xml.

    python3 tools/build_pages.py          # validate every example with the real tracer, then write the pages
    python3 tools/build_pages.py --no-check

Every example is run through the tracer embedded in index.html (plain CPython is enough),
and the build fails if it errors, exceeds the step limit or doesn't match its expected value.
Each page links to the app with a share link (#s=<base64url JSON>) that loads and runs it.
"""
import base64
import datetime
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://pytrace.app"
TODAY = datetime.date.today().isoformat()

# --------------------------------------------------------------------------------------------
# Examples
# --------------------------------------------------------------------------------------------
EXAMPLES = [
    {
        "slug": "two-pointers",
        "title": "Two Pointers Visualization in Python",
        "nav": "Two pointers",
        "description": "See the two pointers technique step by step: watch left and right close in on a sorted array in an animated Python visualization (Two Sum II, LeetCode 167).",
        "problem": ("Two Sum II – Input Array Is Sorted", 167, "two-sum-ii-input-array-is-sorted"),
        "intro": """<p>The <strong>two pointers</strong> technique keeps two indexes into the same array and moves them toward each other (or in the same direction) based on a comparison. On a sorted array it turns an O(n²) pair search into a single O(n) pass.</p>
<p>In this example, <code>left</code> starts at the smallest number and <code>right</code> at the largest. If their sum is too small, the only way to grow it is to move <code>left</code> forward; if it is too big, move <code>right</code> back.</p>""",
        "watch": [
            "<code>left</code> and <code>right</code> drawn as colored pointers under the <code>numbers</code> array",
            "The comparison <code>total &lt; target</code> evaluated on every step, which decides which pointer moves",
            "The search space shrinking by one cell per iteration",
        ],
        "complexity": "O(n) time, O(1) extra space.",
        "code": """class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left, right = 0, len(numbers) - 1
        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                return [left + 1, right + 1]
            if total < target:
                left += 1
            else:
                right -= 1
        return []
""",
        "method": "twoSum",
        "args": {"numbers": "[1,2,3,4,6,8,11,15]", "target": "14"},
        "expected": "[3,7]",
    },
    {
        "slug": "sliding-window",
        "title": "Sliding Window Visualization in Python",
        "nav": "Sliding window",
        "description": "Watch a sliding window grow and shrink over a string, step by step, in an animated Python visualization (Longest Substring Without Repeating Characters).",
        "problem": ("Longest Substring Without Repeating Characters", 3, "longest-substring-without-repeating-characters"),
        "intro": """<p>A <strong>sliding window</strong> is a range <code>[left, right]</code> over an array or string that you extend on one side and shrink on the other, so that each element enters and leaves the window at most once.</p>
<p>Here the window must never contain a repeated character. <code>right</code> moves forward on every iteration; whenever the new character is already in the window, <code>left</code> advances and removes characters from the <code>seen</code> set until the duplicate is gone.</p>""",
        "watch": [
            "<code>left</code> and <code>right</code> as pointers over the string, marking the current window",
            "The <code>seen</code> set gaining and losing characters as the window moves",
            "<code>best</code> updating only when the window reaches a new maximum length",
        ],
        "complexity": "O(n) time: each character is added and removed at most once.",
        "code": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        left = best = 0
        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            best = max(best, right - left + 1)
        return best
""",
        "method": "lengthOfLongestSubstring",
        "args": {"s": '"abcabcbb"'},
        "expected": "3",
    },
    {
        "slug": "binary-search",
        "title": "Binary Search Visualization in Python",
        "nav": "Binary search",
        "description": "Visualize binary search step by step: see lo, mid and hi move over a sorted array and the search space halve on every comparison (LeetCode 704).",
        "problem": ("Binary Search", 704, "binary-search"),
        "intro": """<p><strong>Binary search</strong> finds a value in a sorted array by comparing it with the middle element and discarding the half where it cannot be. Each step halves the search space, so even a million elements need only about 20 comparisons.</p>
<p>The classic bugs are off-by-one errors: <code>lo &lt;= hi</code> versus <code>lo &lt; hi</code>, and <code>mid + 1</code> versus <code>mid</code>. Stepping through the loop and watching the three pointers makes it obvious when the range stops shrinking.</p>""",
        "watch": [
            "<code>lo</code>, <code>mid</code> and <code>hi</code> as pointers over <code>nums</code>",
            "The comparison <code>nums[mid] &lt; target</code> that decides which half to keep",
            "How few iterations it takes to reach the target",
        ],
        "complexity": "O(log n) time, O(1) extra space.",
        "code": """class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
""",
        "method": "search",
        "args": {"nums": "[-1,0,3,5,9,12,17,21,30,42]", "target": "21"},
        "expected": "7",
    },
    {
        "slug": "reverse-linked-list",
        "title": "Reverse a Linked List – Python Visualization",
        "nav": "Reverse a linked list",
        "description": "See how reversing a linked list works: watch prev, curr and next move and each arrow flip, step by step, in an animated Python visualization (LeetCode 206).",
        "problem": ("Reverse Linked List", 206, "reverse-linked-list"),
        "intro": """<p>Reversing a <strong>singly linked list</strong> in place means walking it once and turning every <code>next</code> arrow around. You need three references: <code>prev</code> (the already reversed part), <code>curr</code> (the node being processed) and <code>nxt</code> (so you don't lose the rest of the list when you overwrite <code>curr.next</code>).</p>
<p>It is a short function, but the order of the four assignments matters. PyTrace draws the nodes and arrows, so you can see the list split in two and the reversed half grow node by node.</p>""",
        "watch": [
            "The nodes and <code>next</code> arrows of the list, redrawn after each assignment",
            "<code>prev</code>, <code>curr</code> and <code>nxt</code> pointing at nodes",
            "The moment <code>curr.next = prev</code> flips an arrow",
        ],
        "complexity": "O(n) time, O(1) extra space.",
        "code": """class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev
""",
        "method": "reverseList",
        "args": {"head": "[1,2,3,4,5]"},
        "expected": "[5,4,3,2,1]",
    },
    {
        "slug": "binary-tree-level-order-traversal",
        "title": "Level Order Traversal Visualization (Python BFS)",
        "nav": "Binary tree BFS",
        "description": "Visualize breadth-first search on a binary tree: watch the queue and the tree level by level in an animated Python step-by-step trace (LeetCode 102).",
        "problem": ("Binary Tree Level Order Traversal", 102, "binary-tree-level-order-traversal"),
        "intro": """<p><strong>Level order traversal</strong> is breadth-first search (BFS) on a tree: visit the root, then all nodes at depth 1, then depth 2, and so on. A queue keeps the nodes waiting to be visited, and processing exactly <code>len(queue)</code> nodes per round separates the levels.</p>
<p>PyTrace draws the binary tree from LeetCode notation (<code>[3,9,20,null,null,15,7]</code>), so you can follow which node is being dequeued while the <code>deque</code> and the <code>result</code> list fill up.</p>""",
        "watch": [
            "The binary tree, with the current <code>node</code> highlighted",
            "The <code>queue</code> (<code>deque</code>) as an array: nodes join at the back and leave from the front",
            "<code>result</code> getting one new list per level",
        ],
        "complexity": "O(n) time, O(w) extra space where w is the maximum width of the tree.",
        "code": """class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        result = []
        queue = deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result
""",
        "method": "levelOrder",
        "args": {"root": "[3,9,20,null,null,15,7]"},
        "expected": "[[3],[9,20],[15,7]]",
    },
    {
        "slug": "number-of-islands",
        "title": "Number of Islands: Grid BFS Visualization",
        "nav": "Grid BFS (islands)",
        "description": "Watch breadth-first search flood-fill a 2D grid step by step. An animated Python visualization of Number of Islands (LeetCode 200) with the matrix and queue.",
        "problem": ("Number of Islands", 200, "number-of-islands"),
        "intro": """<p>Many interview problems hide a graph inside a <strong>2D grid</strong>: every cell is a node connected to its four neighbors. To count islands you scan the grid, and every time you find unvisited land you start a <strong>BFS</strong> that sinks the whole island by turning its cells into water.</p>
<p>PyTrace renders the grid as a matrix with <code>r</code>/<code>c</code> and <code>i</code>/<code>j</code> as row and column pointers, so you can watch the flood fill spread from cell to cell.</p>""",
        "watch": [
            "The <code>grid</code> matrix, with cells flipping from <code>\"1\"</code> to <code>\"0\"</code>",
            "The <code>queue</code> of coordinates waiting to be explored",
            "<code>islands</code> increasing only when the scan finds new land",
        ],
        "complexity": "O(rows × cols) time; O(min(rows, cols)) queue space for BFS.",
        "code": """class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        islands = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != "1":
                    continue
                islands += 1
                grid[r][c] = "0"
                queue = deque([(r, c)])
                while queue:
                    i, j = queue.popleft()
                    for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == "1":
                            grid[ni][nj] = "0"
                            queue.append((ni, nj))
        return islands
""",
        "method": "numIslands",
        "args": {"grid": '[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]'},
        "expected": "3",
    },
    {
        "slug": "backtracking-subsets",
        "title": "Recursion and Backtracking Visualization in Python",
        "nav": "Recursion & backtracking",
        "description": "Visualize recursion and backtracking with the call stack: watch every recursive call push and pop while generating all subsets, step by step (LeetCode 78).",
        "problem": ("Subsets", 78, "subsets"),
        "intro": """<p><strong>Backtracking</strong> explores choices recursively: make a choice, recurse, then undo the choice and try the next one. It is how you generate subsets, permutations and combinations, and how you solve problems like N-Queens or Sudoku.</p>
<p>Recursion is hard to trace in your head because each call has its own variables. PyTrace shows the <strong>call stack</strong>: every <code>backtrack(start)</code> frame with its own <code>start</code> and <code>i</code>, while the shared <code>path</code> grows with <code>append</code> and shrinks with <code>pop</code>.</p>""",
        "watch": [
            "The call stack growing with each <code>backtrack(i + 1)</code> and unwinding on return",
            "<code>path</code> being extended and undone: the essence of backtracking",
            "<code>result</code> collecting a copy of <code>path</code> at every node of the recursion tree",
        ],
        "complexity": "O(n · 2ⁿ) time: there are 2ⁿ subsets and copying each costs up to n.",
        "code": """class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []

        def backtrack(start):
            result.append(path[:])
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return result
""",
        "method": "subsets",
        "args": {"nums": "[1,2,3]"},
        "expected": "[[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]",
    },
    {
        "slug": "dynamic-programming-coin-change",
        "title": "Dynamic Programming Visualization in Python",
        "nav": "Dynamic programming",
        "description": "See a bottom-up dynamic programming table fill in, step by step. Animated Python visualization of Coin Change (LeetCode 322) with the dp array.",
        "problem": ("Coin Change", 322, "coin-change"),
        "intro": """<p><strong>Dynamic programming</strong> solves a problem by combining the answers to smaller subproblems. In bottom-up DP you store those answers in a table, here <code>dp[a]</code> = the fewest coins that add up to <code>a</code>, and fill it from the smallest amount up.</p>
<p>For every amount <code>a</code> and every <code>coin</code>, if using that coin on top of the best answer for <code>a - coin</code> is better than what we have, we update <code>dp[a]</code>. Watching the array fill in makes the recurrence concrete.</p>""",
        "watch": [
            "The <code>dp</code> array, with <code>a</code> and <code>a - coin</code> as pointers into it",
            "Cells going from <code>inf</code> (unreachable) to their final value",
            "The comparison that decides whether a coin improves the answer",
        ],
        "complexity": "O(amount × len(coins)) time, O(amount) space.",
        "code": """class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [0] + [inf] * amount
        for a in range(1, amount + 1):
            for coin in coins:
                if coin <= a and dp[a - coin] + 1 < dp[a]:
                    dp[a] = dp[a - coin] + 1
        return dp[amount] if dp[amount] != inf else -1
""",
        "method": "coinChange",
        "args": {"coins": "[1,2,5]", "amount": "11"},
        "expected": "3",
    },
]


# --------------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------------
def share_hash(ex):
    """Same format the app reads: #s=<base64url(JSON)> with { code, method, cases }."""
    payload = {
        "code": ex["code"],
        "method": ex["method"],
        "cases": [{"args": ex["args"], "expected": {ex["method"]: ex["expected"]}, "ops": "", "opargs": ""}],
    }
    raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
    return "#s=" + base64.urlsafe_b64encode(raw).decode().rstrip("=")


def check_examples():
    src = (ROOT / "index.html").read_text()
    py = re.search(r'<script type="text/x-python" id="tracer-src">(.*?)</script>', src, re.S).group(1)
    g = {}
    exec(py, g)
    ok = True
    for ex in EXAMPLES:
        a = json.loads(g["analyze_json"](ex["code"]))
        params = [p["name"] for m in a.get("methods", []) if m["name"] == ex["method"] for p in m["params"]]
        if not a.get("ok") or sorted(params) != sorted(ex["args"]):
            print(f"✗ {ex['slug']}: analysis {a.get('error') or params}")
            ok = False
            continue
        cfg = {"method": ex["method"], "args": ex["args"], "expected": ex["expected"], "ops": "", "opargs": ""}
        t = json.loads(g["run"](ex["code"], json.dumps(cfg)))
        steps = len(t["steps"])
        if t.get("error") or not (t.get("check") or {}).get("ok") or steps >= 5000:
            print(f"✗ {ex['slug']}: error={t.get('error')} result={t.get('result')} check={t.get('check')} steps={steps}")
            ok = False
        else:
            print(f"✓ {ex['slug']}: {steps} steps, result {t.get('result')}")
    return ok


E = html.escape
CM = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16"
GITHUB_SVG = '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
THEME_SVG = (
    '<svg class="sun" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>'
    '<svg class="moon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
)


def app_version():
    m = re.search(r'class="ver"[^>]*>(v[\d.]+)<', (ROOT / "index.html").read_text())
    return m.group(1) if m else ""


def page(*, path, title, description, body, jsonld, og_type="article", current=None, code=False):
    url = SITE + path
    nav = "".join(
        f'<a class="navlink" href="{href}"{" aria-current=\"page\"" if current == key else ""}>{label}</a>'
        for key, href, label in (("app", "/", "Visualizer"), ("examples", "/examples/", "Examples"), ("about", "/about/", "About"))
    )
    cm_css = (
        f'<link rel="stylesheet" href="{CM}/theme/material-darker.min.css">\n<link rel="stylesheet" href="{CM}/theme/idea.min.css">\n'
        if code else ""
    )
    cm_js = f'<script src="{CM}/addon/runmode/runmode-standalone.min.js"></script>\n<script src="{CM}/mode/python/python.min.js"></script>\n' if code else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="PyTrace">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script>
  // same theme logic as the visualizer: saved choice, else the OS preference (before first paint)
  (() => {{
    let t = null;
    try {{ t = JSON.parse(localStorage.getItem("viz.state.v1") || "{{}}").theme; }} catch (e) {{}}
    if (t !== "light" && t !== "dark") t = matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
    document.documentElement.dataset.theme = t;
  }})();
</script>
{cm_css}<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">
{json.dumps(jsonld, indent=1, ensure_ascii=False)}
</script>
</head>
<body>
<header>
  <div class="logo"><a href="/">PyTrace</a><span class="tagline"> · Python algorithm visualizer</span></div>
  <span class="ver">{app_version()}</span>
  <nav>
    {nav}
    <a class="gh-link" href="https://github.com/arvazvi/pytrace" rel="noopener" title="Source code on GitHub" aria-label="PyTrace on GitHub">{GITHUB_SVG}</a>
    <button id="themeBtn" class="icon" aria-label="Toggle light/dark mode">{THEME_SVG}</button>
  </nav>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <a href="/examples/">Examples</a>
  <a href="/about/">About</a>
  <a href="https://github.com/arvazvi/pytrace" rel="noopener">GitHub</a>
</footer>
{cm_js}<script src="/assets/site.js"></script>
</body>
</html>
"""


def breadcrumbs(*items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)
        ],
    }


def run_pill(href, label):
    return f'<a class="run" href="{href}"><span class="ico">▶</span>{label}</a>'


def card(title, body, *, head_extra="", cls="", flush=False, label=False):
    """A card like the visualizer's: uppercase muted head (h2, or a plain label when the page h1 lives inside) + body."""
    head = f'<span class="label">{title}</span>' if label else f"<h2>{title}</h2>"
    inner = body if flush else f'<div class="card-body">{body}</div>'
    return (f'<section class="card {cls}"><div class="card-head">{head}<span class="spacer"></span>{head_extra}</div>'
            f"{inner}</section>")


def code_block(src):
    lines = src.rstrip("\n").split("\n")
    gutter = "\n".join(str(i + 1) for i in range(len(lines)))
    return f'<div class="code"><pre class="gutter" aria-hidden="true">{gutter}</pre><pre class="src"><code>{E(src.rstrip())}</code></pre></div>'


def example_page(ex, i):
    path = f"/examples/{ex['slug']}/"
    name, num, lc = ex["problem"]
    app_url = "/" + share_hash(ex)
    rows = "".join(
        f'<div class="row"><span class="k">{E(k)}</span><span class="v">{E(v)}</span></div>'
        for k, v in [*ex["args"].items(), ("expected", ex["expected"])]
    )
    others = "".join(f'<li><a href="/examples/{o["slug"]}/">{E(o["nav"])}</a></li>' for o in EXAMPLES if o is not ex)

    hero = card(
        f'<a href="/examples/">Examples</a> / {E(ex["nav"])}',
        f'<h1>{E(ex["title"])}</h1>{ex["intro"]}'
        f'<p class="cx"><span class="cx-k">Complexity</span>{ex["complexity"]}</p>',
        head_extra=run_pill(app_url, "Run in PyTrace"), cls="hero", label=True,
    )
    code_card = card(
        "Code",
        code_block(ex["code"]),
        head_extra=f'<a class="meta" href="https://leetcode.com/problems/{lc}/" rel="noopener nofollow">LeetCode {num}: {E(name)} ↗</a>',
        flush=True,
    )
    side = '<div class="stack">' + "".join([
        card("Inputs", f'<div class="inputs">{rows}</div>', head_extra='<span class="meta">LeetCode notation</span>'),
        card("What to watch", "<ul>" + "".join(f"<li>{w}</li>" for w in ex["watch"]) + "</ul>"),
    ]) + "</div>"
    body = "\n".join([
        hero,
        f'<div class="cols-2">{code_card}{side}</div>',
        card("More algorithm visualizations", f'<ul class="chips">{others}</ul>'),
    ])
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "headline": ex["title"],
                "description": ex["description"],
                "url": SITE + path,
                "image": SITE + "/assets/og.png",
                "dateModified": TODAY,
                "author": {"@type": "Person", "name": "Aldo V", "url": "https://github.com/arvazvi"},
                "publisher": {"@type": "Organization", "name": "PyTrace", "url": SITE + "/"},
                "proficiencyLevel": "Beginner",
                "programmingLanguage": "Python",
                "about": ex["nav"],
                "isPartOf": {"@id": SITE + "/#app"},
            },
            breadcrumbs(("PyTrace", "/"), ("Examples", "/examples/"), (ex["nav"], path)),
        ],
    }
    return path, page(path=path, title=f"{ex['title']} | PyTrace", description=ex["description"], body=body,
                      jsonld=jsonld, current="examples", code=True)


def examples_index():
    path = "/examples/"
    title = "Algorithm Visualization Examples in Python"
    description = "Step-by-step Python visualizations of common algorithm patterns: two pointers, sliding window, binary search, linked lists, BFS, backtracking and DP."
    hero = card(
        "Examples",
        f"<h1>{title}</h1>"
        "<p>The algorithm patterns that come up again and again in LeetCode problems and coding interviews. "
        "Each example explains the idea, shows a short Python solution and opens it in the visualizer, where you can "
        "watch it run line by line: pointers moving over arrays, trees and grids being explored, the call stack growing and shrinking.</p>",
        head_extra=run_pill("/", "Open the visualizer"), cls="hero", label=True,
    )
    cards = "".join(
        f"""<article class="card ex-card"><div class="card-head"><h2><a href="/examples/{ex['slug']}/">{E(ex['nav'])}</a></h2><span class="spacer"></span><span class="meta">LC {ex['problem'][1]}</span></div>
<div class="card-body"><p>{E(ex['description'])}</p></div>
<div class="foot">{run_pill('/' + share_hash(ex), 'Run')}<a class="more" href="/examples/{ex['slug']}/">How it works →</a></div></article>"""
        for ex in EXAMPLES
    )
    body = f'{hero}\n<div class="grid-cards">{cards}</div>'
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "name": title,
                "description": description,
                "url": SITE + path,
                "hasPart": [{"@type": "TechArticle", "name": ex["title"], "url": f"{SITE}/examples/{ex['slug']}/"} for ex in EXAMPLES],
            },
            breadcrumbs(("PyTrace", "/"), ("Examples", path)),
        ],
    }
    return path, page(path=path, title=f"{title} | PyTrace", description=description, body=body, jsonld=jsonld,
                      og_type="website", current="examples")


FAQ = [
    ("Does my code leave my computer?",
     "No. PyTrace runs CPython compiled to WebAssembly (Pyodide) inside your browser tab. There is no server, and your code, test cases and layout are only saved in your browser's localStorage."),
    ("Can I paste my LeetCode solution as-is?",
     "Yes. Write it in the usual class Solution format (plain functions and scripts work too). PyTrace detects the method parameters and creates input fields. ListNode and TreeNode inputs use LeetCode notation such as [1,2,3] or [3,9,20,null,null,15,7], and common imports like collections, heapq and bisect are preloaded."),
    ("Are there limits?",
     "Each run records up to 5,000 steps, and visualizations are capped (arrays up to 80 cells, matrices up to 40×40). It is meant for small inputs, not for measuring performance. Threads, subprocesses and sockets are not available."),
    ("Is PyTrace free?",
     "Yes. PyTrace is free, open source and needs no sign-up."),
]


def about_page():
    path = "/about/"
    title = "About PyTrace – Step-by-Step Python Algorithm Visualizer"
    description = "PyTrace runs your Python code line by line and animates arrays with pointers, matrices, linked lists, trees, graphs and the call stack. Free, in your browser."
    hero = card(
        "About",
        "<h1>Visualize Python algorithms step by step</h1>"
        "<p>PyTrace is a free <strong>algorithm visualizer for Python</strong>. Paste your solution to a LeetCode-style problem, "
        "fill in the inputs and press <b>Run</b>: PyTrace executes your code line by line and animates what happens at every step. "
        "You see <strong>arrays with their index pointers</strong> (<code>i</code>, <code>j</code>, <code>left</code>, <code>right</code>…), "
        "<strong>matrices and grids</strong>, <strong>hash maps</strong>, <strong>linked lists</strong>, <strong>binary trees</strong>, "
        "<strong>graphs</strong>, local variables and the <strong>call stack</strong>, and you can play, pause and scrub back and forth through the execution.</p>"
        "<p>It is the tool I wanted while studying for coding interviews: seeing how two pointers close in, how a sliding window grows and shrinks, "
        "how a tree gets traversed or why a recursive function never stops is much easier than tracing it in your head or filling your code with <code>print</code>s.</p>",
        head_extra=run_pill("/", "Open the visualizer"), cls="hero", label=True,
    )
    visualizes = card("What it visualizes", """<ul>
<li><b>Lists, tuples, strings and <code>deque</code></b> as arrays of cells, with index variables drawn as pointers</li>
<li><b>Lists of lists</b> as 2D grids and matrices</li>
<li><b><code>dict</code>, <code>defaultdict</code>, <code>Counter</code></b> as key → value tables, and <b><code>set</code></b> as chips</li>
<li><b>Linked lists</b> (<code>ListNode</code> or anything with <code>next</code>, <code>prev</code>, <code>random</code>)</li>
<li><b>Binary trees</b> (<code>TreeNode</code> or anything with <code>left</code> / <code>right</code>)</li>
<li><b>N-ary trees and graphs</b> (objects with <code>children</code> / <code>neighbors</code>)</li>
<li>The <b>call stack</b>, recursion included, and the <b>comparisons</b> evaluated on the current line</li>
</ul>""")
    leetcode = card("Made for LeetCode practice", """<ul>
<li>Paste a <code>class Solution</code> as-is: PyTrace detects the method and its parameters and creates input fields</li>
<li>Inputs in LeetCode notation: <code>[1,2,3]</code>, <code>[3,9,20,null,null,15,7]</code></li>
<li>Design problems such as <code>LRUCache</code> or <code>MinStack</code> with operation lists</li>
<li>Several test cases, each with an optional expected value</li>
<li><code>ListNode</code>, <code>TreeNode</code>, <code>collections</code>, <code>heapq</code>, <code>bisect</code>… preloaded</li>
<li>Share your solution with a link (🔗 Share)</li>
</ul>""")
    browser = card("Runs entirely in your browser",
                   '<p>PyTrace uses <a href="https://pyodide.org" rel="noopener">Pyodide</a>, CPython compiled to WebAssembly. '
                   "There is no server: your code runs on your own machine and never leaves it. It is free and "
                   '<a href="https://github.com/arvazvi/pytrace" rel="noopener">open source</a>.</p>')
    examples = card("Examples", '<ul class="chips">' + "".join(
        f'<li><a href="/examples/{ex["slug"]}/">{E(ex["nav"])}</a></li>' for ex in EXAMPLES) + "</ul>")
    faq = card("FAQ", "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ)
               + '<p class="muted" style="margin-top:12px">Found a bug or have an idea? '
                 '<a href="https://github.com/arvazvi/pytrace/issues" rel="noopener">Open an issue on GitHub</a>.</p>')
    body = "\n".join([
        hero,
        f'<div class="cols-2"><div class="stack">{visualizes}{browser}</div><div class="stack">{leetcode}{examples}</div></div>',
        faq,
    ])
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "AboutPage",
                "name": title,
                "description": description,
                "url": SITE + path,
                "about": {"@id": SITE + "/#app"},
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ
                ],
            },
            breadcrumbs(("PyTrace", "/"), ("About", path)),
        ],
    }
    return path, page(path=path, title=title, description=description, body=body, jsonld=jsonld,
                      og_type="website", current="about")


def write(path, content):
    out = ROOT / path.lstrip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content)
    print("  wrote", out.relative_to(ROOT))


def main():
    if "--no-check" not in sys.argv and not check_examples():
        sys.exit("Some examples failed; nothing written.")
    pages = [example_page(ex, i) for i, ex in enumerate(EXAMPLES)] + [examples_index(), about_page()]
    for path, content in pages:
        write(path, content)
    urls = [("/", "1.0")] + [(p, "0.8" if p in ("/examples/", "/about/") else "0.7") for p, _ in pages]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in urls)
    sitemap += "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap)
    print("  wrote sitemap.xml")


if __name__ == "__main__":
    main()
