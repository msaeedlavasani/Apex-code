import { useCallback, useEffect, useMemo, useState } from "react";
import { useWorkspaceShellLayout } from "./openwork/workspace-shell-layout";
import { useUiStateStore } from "./openwork/ui-state-store";

type Project = {
  selected: boolean;
  name?: string;
  path?: string;
  entries?: Array<{ name: string; kind: string }>;
};

type Execution = {
  attempt_id: string;
  task_id: string;
  title?: string;
  status?: string;
  reconciliation_state?: string | null;
  runtime_fact?: string;
  runtime_identity?: { session_id?: string | null };
  semantic_success?: boolean | null;
  verification?: string | null;
  verification_reason?: string | null;
  artifact?: string | null;
  manifest_id?: string;
};

type Status = {
  selected: boolean;
  state: string;
  job_state?: string | null;
  job_error?: string | null;
  execution?: Execution | null;
};

type History = { executions: Execution[] };

async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(path, options);
  const payload = await response.json() as T & { error?: string };
  if (!response.ok) throw new Error(payload.error || "Apex application request failed");
  return payload;
}

function stateLabel(execution: Execution | null | undefined, state: string): string {
  return execution?.reconciliation_state || (execution?.semantic_success ? "SUCCEEDED" : state || "UNKNOWN");
}

export function ApexOpenWorkShell() {
  const [project, setProject] = useState<Project>({ selected: false });
  const [workspace, setWorkspace] = useState(() => localStorage.getItem("apex.lastWorkspace") || "");
  const [status, setStatus] = useState<Status>({ selected: false, state: "READY" });
  const [history, setHistory] = useState<History>({ executions: [] });
  const [task, setTask] = useState("report");
  const [artifact, setArtifact] = useState<{ name: string; content: string; sha256?: string } | null>(null);
  const [notice, setNotice] = useState("");
  const [connected, setConnected] = useState(false);
  const sidebarOpen = useUiStateStore((state) => state.sidebarOpen);
  const toggleSidebar = useUiStateStore((state) => state.toggleSidebar);
  const layout = useWorkspaceShellLayout({ expandedRightWidth: 390 });

  const refresh = useCallback(async () => {
    if (!workspace) return;
    try {
      const [nextStatus, nextHistory] = await Promise.all([
        api<Status>("/api/status"),
        api<History>("/api/history"),
      ]);
      setStatus(nextStatus);
      setHistory(nextHistory);
      setConnected(true);
    } catch (error) {
      setConnected(false);
      setNotice(error instanceof Error ? error.message : "Apex application unavailable");
    }
  }, [workspace]);

  const openProject = useCallback(async (path: string) => {
    const nextProject = await api<Project>("/api/project", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path }),
    });
    setProject(nextProject);
    setWorkspace(nextProject.path || path);
    localStorage.setItem("apex.lastWorkspace", nextProject.path || path);
    setArtifact(null);
    setNotice("Project connected to Apex Core");
  }, []);

  useEffect(() => {
    void api<{ ok: boolean }>("/api/health").then(() => setConnected(true)).catch(() => setConnected(false));
  }, []);

  useEffect(() => {
    if (!workspace) return;
    void api<Project>(`/api/project?path=${encodeURIComponent(workspace)}`).then(setProject).catch(() => undefined);
    void refresh();
    const interval = window.setInterval(() => void refresh(), 900);
    return () => window.clearInterval(interval);
  }, [refresh, workspace]);

  const currentExecution = status.execution || history.executions[0] || null;
  const currentState = stateLabel(currentExecution, status.state);
  const canSubmit = project.selected && status.job_state !== "RUNNING" && currentState !== "RECOVERY_REQUIRED";
  const visibleEntries = project.entries || [];
  const layoutColumns = useMemo(
    () => `${sidebarOpen ? layout.leftSidebarWidth : 0}px minmax(0, 1fr) ${layout.rightSidebarWidth}px`,
    [layout.leftSidebarWidth, layout.rightSidebarWidth, sidebarOpen],
  );

  async function submitTask(event: React.FormEvent) {
    event.preventDefault();
    if (!canSubmit) return;
    try {
      await api("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task }),
      });
      setNotice("Task accepted by Apex Core");
      await refresh();
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Task submission failed");
    }
  }

  async function showArtifact(name: string) {
    try {
      setArtifact(await api(`/api/artifact?name=${encodeURIComponent(name)}`));
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Artifact unavailable");
    }
  }

  return (
    <div className="ow-app" data-openwork-shell="true">
      <header className="ow-titlebar">
        <div className="ow-brand"><span className="ow-brand-mark">A</span><span><small>APEX CODE · OPENWORK SHELL</small><strong>Bounded creation workspace</strong></span></div>
        <div className={connected ? "ow-connection online" : "ow-connection"}>{connected ? "Core connected" : "Core unavailable"}</div>
      </header>
      <div className="ow-layout" style={{ gridTemplateColumns: layoutColumns }}>
        {sidebarOpen && <aside className="ow-sidebar" data-openwork-surface="workspace-sidebar">
          <div className="ow-sidebar-heading"><span>WORKSPACES</span><button onClick={toggleSidebar} aria-label="Collapse workspace sidebar">×</button></div>
          <form id="project-form" className="ow-open-form" onSubmit={(event) => { event.preventDefault(); void openProject(workspace).catch((error) => setNotice(error instanceof Error ? error.message : "Project could not be opened")); }}>
            <label htmlFor="project-path">Local project</label>
            <input id="project-path" value={workspace} onChange={(event) => setWorkspace(event.target.value)} placeholder="/path/to/project" />
            <button type="submit">Open project</button>
          </form>
          <div className="ow-workspace-card" data-openwork-surface="workspace-identity">
            <span className="ow-dot" />
            <div><strong>{project.name || "No project selected"}</strong><small>{project.path || "Select a local workspace"}</small></div>
          </div>
          <div className="ow-sidebar-label">PROJECT FILES</div>
          <div className="ow-file-tree" id="file-list" data-openwork-surface="file-tree">
            {visibleEntries.length ? visibleEntries.map((entry) => <div className="ow-file" key={entry.name}><span>{entry.kind === "directory" ? "▸" : "•"}</span>{entry.name}</div>) : <span className="ow-muted">No visible entries</span>}
          </div>
        </aside>}
        {!sidebarOpen && <button className="ow-sidebar-open" onClick={toggleSidebar} aria-label="Open workspace sidebar">☰</button>}
        <main className="ow-main" data-openwork-surface="session-view">
          <div className="ow-main-heading"><div><small>BOUNDED CORE SESSION</small><h1>{project.name || "Open a project to begin"}</h1></div><span id="execution-pill" className={`ow-state state-${currentState}`}>{currentState}</span></div>
          <div className="ow-task-card" data-openwork-surface="task-composer">
            <div className="ow-card-kicker">TASK COMPOSER</div>
            <h2>Turn a bounded instruction into verified evidence</h2>
            <p>The shell sends a command through the Apex Application Boundary. Core owns the Task, Attempt, authority barrier, runtime facts, verification, and semantic result.</p>
            <form id="task-form" onSubmit={submitTask}>
              <label htmlFor="task-type">Task shape</label>
              <select id="task-type" value={task} onChange={(event) => setTask(event.target.value)}><option value="report">Inspect README.md and create REPORT.md</option><option value="summary">Inspect README.md and create SUMMARY.md</option></select>
              <button id="submit-task" type="submit" disabled={!canSubmit}>Submit bounded task</button>
            </form>
          </div>
          <div className="ow-result-card" data-openwork-surface="result-view">
            <div className="ow-card-kicker">CORE RESULT</div>
            {currentExecution ? <div className="ow-metrics">
              <div><small>Core state</small><strong className={`state-${currentState}`}>{currentState}</strong></div>
              <div><small>Runtime fact</small><strong>{currentExecution.runtime_fact || "NOT_OBSERVED"}</strong></div>
              <div><small>Task</small><strong className="mono">{currentExecution.task_id}</strong></div>
              <div><small>Attempt</small><strong className="mono">{currentExecution.attempt_id}</strong></div>
              <div><small>Verification</small><strong>{currentExecution.verification || "NOT_RUN"}</strong></div>
              <div><small>Artifact</small><strong>{currentExecution.artifact || "None"}</strong></div>
            </div> : <span className="ow-muted">No Core execution selected.</span>}
            {currentExecution?.artifact && <button className="ow-secondary" data-artifact={currentExecution.artifact} onClick={() => void showArtifact(currentExecution.artifact!)}>View verified artifact</button>}
            {artifact && <pre className="ow-artifact-preview artifact-preview" aria-label="Verified artifact">{artifact.content}</pre>}
            {status.job_error && <div className="ow-error">{status.job_error}</div>}
          </div>
          {notice && <div className="ow-notice" role="status">{notice}</div>}
        </main>
        <aside className="ow-history" data-openwork-surface="history-panel">
          <div className="ow-history-heading"><span>EXECUTION HISTORY</span><button onClick={layout.toggleRightSidebar} aria-label="Toggle history panel">{layout.rightSidebarExpanded ? "›" : "‹"}</button></div>
          <p>Canonical history is reloaded from the Apex Core ledger. Shell UI state is presentation only.</p>
          <div id="history-count" className="ow-history-count">{history.executions.length} attempt{history.executions.length === 1 ? "" : "s"}</div>
          <div className="ow-history-list">
            {history.executions.map((item) => <div className="ow-history-row" key={item.attempt_id}><strong>{item.title || "Bounded task"}</strong><small className="mono">{item.attempt_id}</small><span className={`state-${stateLabel(item, item.status || "UNKNOWN")}`}>{stateLabel(item, item.status || "UNKNOWN")}</span><span>{item.runtime_fact || "NOT_OBSERVED"} · {item.verification || "NOT_RUN"}</span>{item.artifact && <button className="ow-link" data-artifact={item.artifact} onClick={() => void showArtifact(item.artifact!)}>View artifact</button>}</div>)}
            {!history.executions.length && <span className="ow-muted">No bounded executions yet.</span>}
          </div>
        </aside>
        {sidebarOpen && <div className="ow-resize-handle" onPointerDown={layout.startLeftSidebarResize} aria-hidden="true" />}
      </div>
    </div>
  );
}
