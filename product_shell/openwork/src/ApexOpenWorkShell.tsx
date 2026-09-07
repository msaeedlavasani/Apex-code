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
  model_selection?: string;
};

type Status = {
  selected: boolean;
  state: string;
  job_state?: string | null;
  job_error?: string | null;
  execution?: Execution | null;
};

type History = { executions: Execution[] };

type ProviderModel = { model_id: string; display_name: string };
type ProviderRecord = {
  provider_id: string;
  display_name: string;
  configured: boolean;
  credential_status: string;
  models: ProviderModel[];
};
type ProviderStateData = {
  providers: ProviderRecord[];
  selection: { provider_id: string; model_id: string } | null;
  credential_status: string;
  secure_storage: string;
};

const API_BASE = window.__APEX_DESKTOP__?.apiBase || "";

async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, options);
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
  const [providerState, setProviderState] = useState<ProviderStateData>({ providers: [], selection: null, credential_status: "NOT_CONFIGURED", secure_storage: "UNAVAILABLE" });
  const [providerSecret, setProviderSecret] = useState("");
  const [providerTest, setProviderTest] = useState("");
  const [connectionState, setConnectionState] = useState("CONNECTING");
  const connected = connectionState === "READY";
  const sidebarOpen = useUiStateStore((state) => state.sidebarOpen);
  const toggleSidebar = useUiStateStore((state) => state.toggleSidebar);
  const layout = useWorkspaceShellLayout({ expandedRightWidth: 390 });

  const refresh = useCallback(async () => {
    if (!workspace) return;
    try {
      const providerRequest = window.__APEX_DESKTOP__?.getProviderState
        ? window.__APEX_DESKTOP__.getProviderState()
        : api<ProviderStateData>("/api/providers");
      const [nextStatus, nextHistory, nextProviderState] = await Promise.all([
        api<Status>("/api/status"),
        api<History>("/api/history"),
        providerRequest,
      ]);
      setStatus(nextStatus);
      setHistory(nextHistory);
      setProviderState(nextProviderState);
      setConnectionState("READY");
    } catch (error) {
      setConnectionState("CORE_UNAVAILABLE");
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
    void api<{ ok: boolean }>("/api/health").then(() => setConnectionState("READY")).catch(() => setConnectionState("CORE_UNAVAILABLE"));
  }, []);

  useEffect(() => {
    const load = window.__APEX_DESKTOP__?.getProviderState
      ? window.__APEX_DESKTOP__.getProviderState()
      : api<ProviderStateData>("/api/providers");
    void load.then(setProviderState).catch(() => setProviderTest("Provider settings unavailable"));
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
  const selectedProvider = providerState.providers.find((provider) => provider.provider_id === providerState.selection?.provider_id) || providerState.providers[0];
  const selectedModel = providerState.selection?.model_id || selectedProvider?.models[0]?.model_id || "";
  const providerReady = !window.__APEX_DESKTOP__ || providerState.credential_status === "CONFIGURED";
  const canSubmit = project.selected && providerReady && status.job_state !== "RUNNING" && currentState !== "RECOVERY_REQUIRED";
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

  async function selectProvider(providerId: string) {
    const provider = providerState.providers.find((item) => item.provider_id === providerId);
    const modelId = provider?.models[0]?.model_id || "";
    if (!window.__APEX_DESKTOP__ || !modelId) return;
    try {
      setProviderState(await window.__APEX_DESKTOP__.setProviderSelection({ provider_id: providerId, model_id: modelId }));
      setProviderTest("");
      setNotice("Provider selection saved");
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Provider selection failed");
    }
  }

  async function selectModel(modelId: string) {
    const providerId = providerState.selection?.provider_id || selectedProvider?.provider_id;
    if (!window.__APEX_DESKTOP__ || !providerId) return;
    try {
      setProviderState(await window.__APEX_DESKTOP__.setProviderSelection({ provider_id: providerId, model_id: modelId }));
      setProviderTest("");
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Model selection failed");
    }
  }

  async function saveProviderCredential() {
    const providerId = providerState.selection?.provider_id || selectedProvider?.provider_id;
    if (!window.__APEX_DESKTOP__ || !providerId || !providerSecret) return;
    try {
      if (!providerState.selection) {
        setProviderState(await window.__APEX_DESKTOP__.setProviderSelection({ provider_id: providerId, model_id: selectedModel }));
      }
      setProviderState(await window.__APEX_DESKTOP__.saveProviderCredential({ provider_id: providerId, secret: providerSecret }));
      setProviderSecret("");
      setProviderTest("");
      setNotice("Credential saved in OS-backed secure storage");
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Credential could not be saved");
    }
  }

  async function testProvider() {
    if (!window.__APEX_DESKTOP__) return;
    try {
      const result = await window.__APEX_DESKTOP__.testProvider();
      setProviderTest(`${result.status}: ${result.message}`);
    } catch (error) {
      setProviderTest(error instanceof Error ? error.message : "Provider test failed");
    }
  }

  async function deleteProviderCredential() {
    const providerId = providerState.selection?.provider_id || selectedProvider?.provider_id;
    if (!window.__APEX_DESKTOP__ || !providerId) return;
    try {
      setProviderState(await window.__APEX_DESKTOP__.deleteProviderCredential(providerId));
      setProviderTest("");
      setNotice("Credential removed; ambient credentials are not used");
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Credential could not be removed");
    }
  }

  async function chooseProject() {
    try {
      const selected = await window.__APEX_DESKTOP__?.selectProject();
      if (typeof selected === "string" && selected) {
        setWorkspace(selected);
        await openProject(selected);
      }
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Project could not be selected");
    }
  }

  return (
    <div className="ow-app" data-openwork-shell="true">
      <header className="ow-titlebar">
        <div className="ow-brand"><span className="ow-brand-mark">A</span><span><small>APEX CODE · OPENWORK SHELL</small><strong>Bounded creation workspace</strong></span></div>
        <div className={connected ? "ow-connection online" : "ow-connection"}>{connectionState}</div>
      </header>
      <div className="ow-layout" style={{ gridTemplateColumns: layoutColumns }}>
        {sidebarOpen && <aside className="ow-sidebar" data-openwork-surface="workspace-sidebar">
          <div className="ow-sidebar-heading"><span>WORKSPACES</span><button onClick={toggleSidebar} aria-label="Collapse workspace sidebar">×</button></div>
          <form id="project-form" className="ow-open-form" onSubmit={(event) => { event.preventDefault(); void openProject(workspace).catch((error) => setNotice(error instanceof Error ? error.message : "Project could not be opened")); }}>
            <label htmlFor="project-path">Local project</label>
            <input id="project-path" value={workspace} onChange={(event) => setWorkspace(event.target.value)} placeholder="/path/to/project" />
            {window.__APEX_DESKTOP__ && <button id="choose-project" className="ow-secondary" type="button" onClick={() => void chooseProject()}>Choose folder…</button>}
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
          <div className="ow-provider-card" data-openwork-surface="provider-settings">
            <div className="ow-card-kicker">AI PROVIDER SETTINGS</div>
            <h2>Choose the model for future Attempts</h2>
            {window.__APEX_DESKTOP__ ? <>
              <div className="ow-provider-grid">
                <label>Provider<select id="provider-select" value={selectedProvider?.provider_id || ""} onChange={(event) => void selectProvider(event.target.value)}>{providerState.providers.map((provider) => <option key={provider.provider_id} value={provider.provider_id}>{provider.display_name}</option>)}</select></label>
                <label>Model<select id="model-select" value={selectedModel} onChange={(event) => void selectModel(event.target.value)}>{(selectedProvider?.models || []).map((model) => <option key={model.model_id} value={model.model_id}>{model.display_name}</option>)}</select></label>
              </div>
              <div className="ow-provider-status"><span>Credential</span><strong>{providerState.credential_status}</strong><small>{providerState.secure_storage}</small></div>
              <div className="ow-provider-actions"><input id="provider-secret" type="password" autoComplete="off" value={providerSecret} onChange={(event) => setProviderSecret(event.target.value)} placeholder="Enter provider credential" aria-label="Provider credential" /><button className="ow-secondary" type="button" onClick={() => void saveProviderCredential()} disabled={!providerSecret}>Save credential</button><button className="ow-secondary" type="button" onClick={() => void testProvider()} disabled={providerState.credential_status !== "CONFIGURED"}>Test connection</button><button className="ow-secondary" type="button" onClick={() => void deleteProviderCredential()} disabled={providerState.credential_status !== "CONFIGURED"}>Remove</button></div>
              {providerTest && <div className="ow-provider-result" role="status">{providerTest}</div>}
            </> : <p className="ow-muted">Credential settings are desktop-only. The browser harness never persists credentials.</p>}
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
              <div><small>Provider / model</small><strong>{currentExecution.model_selection || "NOT_CONFIGURED"}</strong></div>
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
