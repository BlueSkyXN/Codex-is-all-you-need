(() => {
  const frame = document.getElementById("screen");
  const waiting = document.getElementById("waiting");
  const dot = document.getElementById("dot");
  const statusText = document.getElementById("statusText");
  const toast = document.getElementById("toast");
  const storageKey = "visual-brainstorming-session-key";
  let currentVersion = "";
  let currentName = "";
  let currentBridge = "";
  let toastTimer;
  let pollFailures = 0;

  const fragmentParams = new URLSearchParams(location.hash.slice(1));
  const queryParams = new URLSearchParams(location.search);
  const fragmentKeys = fragmentParams.getAll("key");
  const queryKeys = queryParams.getAll("key");
  const fragmentKey = fragmentKeys.length === 1 ? fragmentKeys[0] : "";
  const queryKey = queryKeys.length === 1 ? queryKeys[0] : "";
  const invalidLocationKey =
    fragmentKeys.length > 1 ||
    queryKeys.length > 1 ||
    (fragmentKey && queryKey && fragmentKey !== queryKey);
  let sessionKey = invalidLocationKey ? "" : (fragmentKey || queryKey);
  try {
    if (!invalidLocationKey) {
      sessionKey = sessionKey || sessionStorage.getItem(storageKey) || "";
    }
    if (sessionKey) sessionStorage.setItem(storageKey, sessionKey);
  } catch (_error) {
    // A fragment/query key still works when sessionStorage is unavailable.
  }
  history.replaceState(null, "", location.pathname);
  const authBase = sessionKey ? `/_vb/${encodeURIComponent(sessionKey)}` : "";
  const authenticated = path => `${authBase}${path}`;

  function showToast(message) {
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 2500);
  }

  async function poll() {
    try {
      const response = await fetch(authenticated("/api/latest"), { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const latest = await response.json();
      pollFailures = 0;
      dot.classList.add("ok");
      statusText.textContent = latest.available
        ? latest.name
        : (latest.error || "已连接 · 等待画面");
      if (latest.available && latest.version !== currentVersion) {
        currentVersion = latest.version;
        currentName = latest.name;
        currentBridge = latest.bridge || "";
        frame.classList.remove("ready");
        frame.src = `${authenticated(`/screen/${encodeURIComponent(latest.name)}`)}?v=${encodeURIComponent(latest.version)}`;
        waiting.classList.add("hidden");
      }
    } catch (error) {
      pollFailures = Math.min(pollFailures + 1, 5);
      dot.classList.remove("ok");
      statusText.textContent = "连接暂停";
    } finally {
      const baseDelay = document.hidden ? 5000 : 1000;
      const maxDelay = document.hidden ? 30000 : 15000;
      const delay = pollFailures
        ? Math.min(maxDelay, baseDelay * (2 ** pollFailures))
        : baseDelay;
      setTimeout(poll, delay);
    }
  }

  frame.addEventListener("load", () => frame.classList.add("ready"));

  window.addEventListener("message", async message => {
    if (message.source !== frame.contentWindow) return;
    if (!message.data || message.data.source !== "visual-brainstorming") return;
    if (!currentBridge || message.data.bridge !== currentBridge) return;
    const event = Object.assign({}, message.data.event || {}, { screen: currentName });
    try {
      const response = await fetch(authenticated("/api/events"), {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-VB-Client": "1" },
        body: JSON.stringify(event)
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const saved = await response.json();
      const label = saved.event.label || saved.event.choice || saved.event.type;
      showToast(`已记录：${label}`);
    } catch (error) {
      showToast("未能记录选择，请回到聊天中直接说明。");
    }
  });

  if (sessionKey) {
    poll();
  } else {
    dot.classList.remove("ok");
    statusText.textContent = invalidLocationKey
      ? "链接包含冲突的会话凭据"
      : "链接缺少会话凭据";
    waiting.querySelector("h1").textContent = "无法连接本地会话";
    waiting.querySelector("p:not(.waiting-eyebrow)").textContent =
      "请从 Agent 返回的完整链接重新打开此页面。";
  }
})();
