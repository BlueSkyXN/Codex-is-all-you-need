(() => {
  const SOURCE = "visual-brainstorming";
  const BRIDGE = "__VB_BRIDGE_TOKEN__";

  function send(event) {
    window.parent.postMessage({ source: SOURCE, bridge: BRIDGE, event }, "*");
  }

  function selectable(element) {
    return element && element.closest ? element.closest("[data-choice]") : null;
  }

  function choose(element) {
    document.querySelectorAll("[data-choice]").forEach(node => {
      node.classList.remove("vb-selected");
      node.setAttribute("aria-pressed", "false");
    });
    element.classList.add("vb-selected");
    element.setAttribute("aria-pressed", "true");
    send({
      type: "choice",
      choice: element.dataset.choice || "",
      label: element.dataset.label || element.getAttribute("aria-label") || element.textContent.trim().slice(0, 160),
      detail: element.dataset.detail || ""
    });
  }

  document.querySelectorAll("[data-choice]").forEach(element => {
    if (!element.hasAttribute("tabindex")) element.tabIndex = 0;
    if (!element.hasAttribute("role")) element.setAttribute("role", "button");
    if (!element.hasAttribute("aria-pressed")) element.setAttribute("aria-pressed", "false");
  });

  document.addEventListener("click", event => {
    const submit = event.target.closest ? event.target.closest("[data-vb-submit-note]") : null;
    if (submit) {
      const note = document.querySelector("[data-vb-note]");
      send({
        type: "note",
        label: submit.dataset.label || "提交备注",
        note: note ? note.value : ""
      });
      return;
    }
    const element = selectable(event.target);
    if (element) choose(element);
  });

  document.addEventListener("keydown", event => {
    if (event.key !== "Enter" && event.key !== " ") return;
    const element = selectable(event.target);
    if (!element) return;
    event.preventDefault();
    choose(element);
  });
})();
