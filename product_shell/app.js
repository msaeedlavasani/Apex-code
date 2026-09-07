(function () {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const state = { workspace: "", polling: null, toastTimer: null };

  function toast(message) {
    const node = $("toast");
    node.textContent = message;
    node.classList.add("visible");
    clearTimeout(state.toastTimer);
    state.toastTimer = setTimeout(() => node.classList.remove("visible"), 3600);
  }

  async function request(url, options) {
    const response = await fetch(url, options);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Request failed");
    return payload;
  }

  function renderProject(project) {
    $("submit-task").disabled = !project.selected;
    $("project-pill").textContent = project.selected ? "Selected" : "Not selected";
    if (!project.selected) {
      $("project-summary").innerHTML = '<div class="empty">Choose a disposable project to begin.</div>';
      $("file-list").innerHTML = "";
      return;
    }
    state.workspace = project.path;
    localStorage.setItem("apex.lastWorkspace", project.path);
    $("project-summary").innerHTML = `<strong>${escapeHtml(project.name)}</strong><code>${escapeHtml(project.path)}</code>`;
    $("file-list").innerHTML = project.entries.map((entry) => `<div class="file-entry"><span>${escapeHtml(entry.name)}</span><span class="kind">${escapeHtml(entry.kind)}</span></div>`).join("") || '<div class="empty">No visible entries.</div>';
  }

  function displayState(value) {
    return `<span class="state-${escapeHtml(value || "UNKNOWN")}">${escapeHtml(value || "UNKNOWN")}</span>`;
  }

  function renderExecution(status) {
    const execution = status.execution;
    $("execution-pill").innerHTML = displayState(status.state || "READY");
    if (!execution) {
      $("execution-card").innerHTML = `<div class="empty">${status.state === "RUNNING" ? "Core is creating the execution record…" : "No execution selected."}</div>`;
      return;
    }
    $("execution-card").innerHTML = `<div class="execution-grid">
      <div class="metric"><span>Core state</span><strong>${displayState(status.state)}</strong></div>
      <div class="metric"><span>Runtime fact</span><strong>${escapeHtml(execution.runtime_fact || "NOT_OBSERVED")}</strong></div>
      <div class="metric"><span>Task</span><strong class="mono">${escapeHtml(execution.task_id)}</strong></div>
      <div class="metric"><span>Attempt</span><strong class="mono">${escapeHtml(execution.attempt_id)}</strong></div>
      <div class="metric"><span>Verification</span><strong>${escapeHtml(execution.verification || "NOT_RUN")}</strong></div>
      <div class="metric"><span>Artifact</span><strong>${escapeHtml(execution.artifact || "None")}</strong></div>
    </div>${status.job_error ? `<p class="help state-FAILED">${escapeHtml(status.job_error)}</p>` : ""}`;
  }

  function renderHistory(payload) {
    const executions = payload.executions || [];
    $("history-count").textContent = `${executions.length} attempt${executions.length === 1 ? "" : "s"}`;
    if (!executions.length) {
      $("history-list").innerHTML = '<div class="empty">No bounded executions yet.</div>';
      return;
    }
    $("history-list").innerHTML = executions.map((item) => `<div class="history-row">
      <div><strong>${escapeHtml(item.title || "Bounded task")}</strong><small class="mono">${escapeHtml(item.attempt_id)}</small></div>
      <div><small>state</small>${displayState(item.reconciliation_state || (item.semantic_success ? "SUCCEEDED" : item.status || "UNKNOWN"))}</div>
      <div><small>runtime fact</small>${escapeHtml(item.runtime_fact || "NOT_OBSERVED")}</div>
      <div><small>verification</small>${escapeHtml(item.verification || "NOT_RUN")}</div>
      ${item.artifact ? `<button class="artifact-button" data-artifact="${escapeHtml(item.artifact)}">View artifact</button>` : "<span></span>"}
    </div>`).join("");
    document.querySelectorAll("[data-artifact]").forEach((button) => button.addEventListener("click", async () => {
      try {
        const artifact = await request(`/api/artifact?name=${encodeURIComponent(button.dataset.artifact)}`);
        $("execution-card").innerHTML = `<div class="eyebrow">CORE-RECORDED ARTIFACT · ${escapeHtml(artifact.name)}</div><pre class="artifact-preview">${escapeHtml(artifact.content)}</pre><div class="help mono">sha256 ${escapeHtml(artifact.sha256 || "unknown")}</div>`;
      } catch (error) { toast(error.message); }
    }));
  }

  async function refresh() {
    if (!state.workspace) return;
    try {
      const [status, history] = await Promise.all([request("/api/status"), request("/api/history")]);
      renderExecution(status);
      renderHistory(history);
      $("connection-status").dataset.state = "online";
      $("connection-status").textContent = "Core connected";
    } catch (error) {
      $("connection-status").dataset.state = "offline";
      $("connection-status").textContent = "Core unavailable";
    }
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[character]));
  }

  $("project-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const project = await request("/api/project", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ path: $("project-path").value.trim() }) });
      renderProject(project);
      await refresh();
      toast("Project connected to Apex Core");
    } catch (error) { toast(error.message); }
  });

  $("task-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    $("submit-task").disabled = true;
    try {
      await request("/api/tasks", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ task: $("task-type").value }) });
      toast("Task accepted by Apex Core");
      await refresh();
    } catch (error) { toast(error.message); }
    finally { $("submit-task").disabled = !state.workspace; }
  });

  $("project-path").value = localStorage.getItem("apex.lastWorkspace") || "";
  request("/api/health").then(() => { $("connection-status").dataset.state = "online"; $("connection-status").textContent = "Core connected"; }).catch(() => {});
  const remembered = localStorage.getItem("apex.lastWorkspace");
  if (remembered) request(`/api/project?path=${encodeURIComponent(remembered)}`).then(renderProject).then(refresh).catch(() => {});
  state.polling = setInterval(refresh, 1000);
}());
