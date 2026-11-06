// PyTrace content pages: theme toggle (shared with the visualizer) + editor-like code highlighting.
(() => {
  const STORE = "viz.state.v1"; // same key the visualizer uses, so the theme choice is shared
  const cmTheme = () => (document.documentElement.dataset.theme === "light" ? "cm-s-idea" : "cm-s-material-darker");
  const paintCode = () => document.querySelectorAll(".code .src").forEach((el) => {
    el.classList.remove("cm-s-idea", "cm-s-material-darker");
    el.classList.add(cmTheme());
  });

  function applyTheme(t, persist) {
    document.documentElement.dataset.theme = t;
    const btn = document.getElementById("themeBtn");
    if (btn) btn.title = t === "light" ? "Switch to dark mode" : "Switch to light mode";
    paintCode();
    if (!persist) return;
    try {
      const s = JSON.parse(localStorage.getItem(STORE) || "{}");
      s.theme = t;
      localStorage.setItem(STORE, JSON.stringify(s));
    } catch (e) {}
  }

  document.getElementById("themeBtn")?.addEventListener("click", () =>
    applyTheme(document.documentElement.dataset.theme === "light" ? "dark" : "light", true));
  matchMedia("(prefers-color-scheme: light)").addEventListener("change", (e) => {
    let saved = null;
    try { saved = JSON.parse(localStorage.getItem(STORE) || "{}").theme; } catch (err) {}
    if (!saved) applyTheme(e.matches ? "light" : "dark", false);
  });

  // syntax highlighting with the same CodeMirror mode/themes as the editor (plain text if it fails to load)
  if (window.CodeMirror && CodeMirror.runMode) {
    document.querySelectorAll(".code .src").forEach((el) => {
      const text = el.textContent;
      el.textContent = "";
      CodeMirror.runMode(text, "python", el);
    });
  }
  applyTheme(document.documentElement.dataset.theme, false);
})();
