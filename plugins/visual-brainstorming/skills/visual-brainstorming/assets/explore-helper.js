(() => {
  const SOURCE = "visual-brainstorming";
  const BRIDGE = "__VB_BRIDGE_TOKEN__";

  function send(event) {
    window.parent.postMessage({ source: SOURCE, bridge: BRIDGE, event }, "*");
  }

  // ---------------------------------------------------------------- paths
  // Elements may declare the logical paths they belong to:
  //   <g data-flows="message tool">...</g>
  // Filter buttons carry the matching path id:
  //   <button data-vb-path="message">消息路径</button>
  // A button with data-vb-path="all" (or no value) restores the full view.
  const flowNodes = Array.from(document.querySelectorAll("[data-flows]"));
  const pathButtons = Array.from(document.querySelectorAll("[data-vb-path]"));

  function nodeFlows(node) {
    return (node.dataset.flows || "").trim().split(/\s+/).filter(Boolean);
  }

  function applyPath(path) {
    const showAll = !path || path === "all";
    flowNodes.forEach(node => {
      const active = showAll || nodeFlows(node).includes(path);
      node.classList.toggle("vb-flow-dim", !active);
      node.classList.toggle("vb-flow-active", active && !showAll);
    });
    pathButtons.forEach(button => {
      const current = (button.dataset.vbPath || "all") === (showAll ? "all" : path);
      button.setAttribute("aria-pressed", current ? "true" : "false");
      button.classList.toggle("vb-path-on", current);
    });
    const panel = document.querySelector("[data-vb-path-panel]");
    if (panel) {
      const target = document.querySelector(`[data-vb-path-desc="${showAll ? "all" : path}"]`);
      if (target) panel.textContent = target.textContent;
    }
  }

  pathButtons.forEach(button => {
    if (!button.hasAttribute("aria-pressed")) button.setAttribute("aria-pressed", "false");
  });

  // ----------------------------------------------------------------- nodes
  // Clickable structural nodes report an exploration event instead of a
  // decision. Evidence state is read from data-evidence and surfaced on the
  // detail panel; the node element itself is styled via CSS classes.
  //   <g data-node="feishu-app" data-label="FeishuApp"
  //      data-evidence="verified" data-source="src/app.ts:40">...</g>
  const detailPanel = document.querySelector("[data-vb-node-detail]");

  function describeNode(node) {
    if (detailPanel) {
      const name = node.dataset.label || node.dataset.node || "";
      const source = node.dataset.source || "";
      const evidence = node.dataset.evidence || "";
      const evidenceLabel = { claimed: "文档声称", verified: "代码坐实", contradicted: "存在冲突" }[evidence] || "";
      const detail = node.dataset.detail || "";
      detailPanel.innerHTML = "";
      const title = document.createElement("strong");
      title.textContent = name;
      detailPanel.appendChild(title);
      if (evidenceLabel) {
        const tag = document.createElement("span");
        tag.className = `vb-ev vb-ev-${evidence}`;
        tag.textContent = evidenceLabel;
        detailPanel.appendChild(tag);
      }
      if (detail) {
        const p = document.createElement("p");
        p.textContent = detail;
        detailPanel.appendChild(p);
      }
      if (source) {
        const ref = document.createElement("code");
        ref.textContent = source;
        detailPanel.appendChild(ref);
      }
    }
    send({
      type: "action",
      choice: node.dataset.node || "",
      label: node.dataset.label || node.dataset.node || "",
      detail: node.dataset.source || "",
      payload: {
        kind: "explore-node",
        evidence: node.dataset.evidence || "",
        source: node.dataset.source || "",
        flows: nodeFlows(node)
      }
    });
  }

  document.querySelectorAll("[data-node]").forEach(node => {
    if (!node.hasAttribute("tabindex")) node.tabIndex = 0;
    if (!node.hasAttribute("role")) node.setAttribute("role", "button");
  });

  // ---------------------------------------------------------------- events
  document.addEventListener("click", event => {
    const pathButton = event.target.closest ? event.target.closest("[data-vb-path]") : null;
    if (pathButton) {
      applyPath(pathButton.dataset.vbPath || "all");
      return;
    }
    const node = event.target.closest ? event.target.closest("[data-node]") : null;
    if (node) describeNode(node);
  });

  document.addEventListener("keydown", event => {
    if (event.key !== "Enter" && event.key !== " ") return;
    const node = event.target.closest ? event.target.closest("[data-node]") : null;
    if (!node) return;
    event.preventDefault();
    describeNode(node);
  });
})();
