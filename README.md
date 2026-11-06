# PyTrace

**Step-by-step visualizer for Python solutions to LeetCode-style problems.**

👉 Try it at **[pytrace.app](https://pytrace.app)** — free, no sign-up.

PyTrace runs your Python code line by line and shows you what happens at each step: variables, the call stack, the comparisons on the current line, and an animated view of your data structures (arrays with their index pointers, matrices, dicts, linked lists, trees, graphs…). You can play, pause and scrub back and forth through the execution.

## Why

I built PyTrace to help myself study LeetCode-style problems. Seeing how pointers move, how a tree gets traversed, or why a loop never ends is much easier than tracing it in your head or filling your code with `print`s. I hope it helps someone else too.

## How it works

- Everything runs **in your browser**. Python (CPython) is compiled to WebAssembly via [Pyodide](https://pyodide.org); there is no server and your code never leaves your machine.
- The tracer uses `sys.settrace` to record every step, and the page renders the recorded steps.
- Your code, test cases, layout and theme are saved in your browser's `localStorage`.

### Ways to write code

- **`class Solution`**: the usual LeetCode format. PyTrace detects the methods and their parameters and generates input fields for them.
- **Plain functions** defined at the top level.
- **Scripts**: loose code with no functions.
- **Design problems** (e.g. `LRUCache`, `MinStack`): LeetCode-style operation lists, like `["LRUCache","put","get"]` + `[[2],[1,1],[1]]`.

You can have several test cases, each with an optional **expected** value, and PyTrace tells you whether the result matches.

`ListNode`, `TreeNode` and common imports (`collections`, `heapq`, `bisect`, `itertools`, `functools`, `math`, `typing`, …) are already available, just like on LeetCode. `ListNode` and `TreeNode` inputs are written in LeetCode notation: `[1,2,3]`, `[3,9,20,null,null,15,7]`.

## Supported data structures

| Structure | Visualization |
| --- | --- |
| Lists, tuples, `deque`, strings | Array of cells, with index variables (`i`, `j`, `left`, `right`…) drawn as pointers |
| Lists of lists | 2D grid / matrix |
| `dict`, `defaultdict`, `Counter` | Key → value table |
| `set` | Chips, highlighting added elements |
| Linked lists (`ListNode` or any object with `next`; also `prev`, `random`) | Nodes and arrows |
| Binary trees (`TreeNode` or any object with `left` / `right`) | Tree |
| N-ary trees and graphs (objects with `children` / `neighbors`) | Node graph |

It also shows local variables, the call stack (recursion included), the comparisons evaluated on the current line, and the program output (`print`).

## Known limitations

- **5,000 step limit** per run: infinite loops or very large inputs are cut off and only the first 5,000 steps are shown.
- **Size limits** on visualizations: arrays up to 80 cells, matrices up to 40×40, up to 150 nodes per step (long linked lists are drawn up to 40 nodes).
- Heaps (`heapq`) are shown as plain arrays, not as trees.
- Python only. Pyodide supports most of the standard library, but **not** threads, subprocesses or sockets, and not every third-party package.
- The first load downloads the runtime (~10 MB) from a CDN, so it needs an internet connection; after that the browser caches it.
- Tracing every line adds overhead, so it is meant for small inputs, not for measuring performance.

## Run it locally

PyTrace is open source and free to use: fork it, modify it, and run it on your own machine.

The whole app is a single `index.html` file with no build step. Serve it with any static server:

```bash
git clone https://github.com/arvazvi/pytrace.git
cd pytrace
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

> Dependencies (Pyodide, CodeMirror, Gridstack, Ruff) are loaded from public CDNs, so you need an internet connection.

## Found a bug?

If something doesn't work, a structure isn't drawn properly, or you have an idea, please [open an issue](https://github.com/arvazvi/pytrace/issues). If you can, include the code and inputs that reproduce the problem. It helps a lot.
