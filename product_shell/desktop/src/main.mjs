import { randomBytes } from "node:crypto";
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { app, BrowserWindow, dialog, ipcMain, safeStorage } from "electron";
import {
  isLoopbackUrl,
  parseServiceUrl,
  rendererRoot,
  runtimeRoot,
  serviceArguments,
  serviceEnvironment,
} from "./service.mjs";
import { ProviderVault } from "./provider-vault.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const desktopRoot = path.resolve(__dirname, "..");
let mainWindow = null;
let apexService = null;
let apexServiceUrl = null;
let shuttingDown = false;
let providerVault = null;
const internalToken = randomBytes(32).toString("hex");

if (process.env.APEX_DESKTOP_USER_DATA?.trim()) {
  app.setPath("userData", path.resolve(process.env.APEX_DESKTOP_USER_DATA));
}

const hasInstanceLock = app.requestSingleInstanceLock();
if (!hasInstanceLock) {
  app.quit();
} else {
  app.on("second-instance", () => {
    if (!mainWindow) return;
    if (mainWindow.isMinimized()) mainWindow.restore();
    mainWindow.focus();
  });
}

function pythonCommand() {
  return process.env.APEX_PYTHON?.trim() || "python3";
}

function waitForService(child) {
  return new Promise((resolve, reject) => {
    let output = "";
    let settled = false;
    const timeout = setTimeout(() => finish(new Error("Apex Core service startup timed out")), 20_000);
    const finish = (error, url) => {
      if (settled) return;
      settled = true;
      clearTimeout(timeout);
      error ? reject(error) : resolve(url);
    };
    child.stdout.on("data", (chunk) => {
      output += String(chunk);
      const url = parseServiceUrl(output);
      if (url && isLoopbackUrl(url)) finish(null, url);
    });
    child.once("error", () => finish(new Error("Apex Core service could not be started")));
    child.once("exit", (code) => {
      if (!settled) finish(new Error(`Apex Core service exited during startup (${code ?? "unknown"})`));
    });
  });
}

async function healthCheck(baseUrl) {
  const deadline = Date.now() + 10_000;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(`${baseUrl}/api/health`);
      if (response.ok) return;
    } catch {
      // The service can announce its port just before the HTTP listener accepts.
    }
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error("Apex Core service health check timed out");
}

async function startApexService() {
  const root = runtimeRoot({ isPackaged: app.isPackaged, resourcesPath: process.resourcesPath, desktopRoot });
  const renderer = rendererRoot({ isPackaged: app.isPackaged, resourcesPath: process.resourcesPath, desktopRoot });
  if (!existsSync(path.join(root, "apex_code")) || !existsSync(path.join(renderer, "index.html"))) {
    throw new Error("Apex runtime resources are missing; build the renderer and package again");
  }
  apexService = spawn(pythonCommand(), serviceArguments(), {
    cwd: root,
    env: serviceEnvironment(process.env, root, internalToken),
    shell: false,
    stdio: ["ignore", "pipe", "ignore"],
  });
  apexServiceUrl = await waitForService(apexService);
  await healthCheck(apexServiceUrl);
  return { renderer };
}

async function internalPost(pathname, payload) {
  if (!apexServiceUrl) throw new Error("Apex Core service is unavailable");
  const response = await fetch(`${apexServiceUrl}${pathname}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Apex-Internal-Token": internalToken,
    },
    body: JSON.stringify(payload),
  });
  const body = await response.json();
  if (!response.ok) throw new Error("Apex provider configuration could not be applied");
  return body;
}

async function serviceProviderState() {
  if (!apexServiceUrl) return null;
  const response = await fetch(`${apexServiceUrl}/api/providers`);
  if (!response.ok) throw new Error("Apex provider state is unavailable");
  return response.json();
}

async function syncProviderRuntime() {
  const selection = providerVault?.getSelection();
  const credential = selection ? providerVault.resolveCredential(selection.provider_id) : null;
  return internalPost("/api/internal/provider-runtime", {
    provider_id: selection?.provider_id || "",
    model_id: selection?.model_id || "",
    credential,
  });
}

async function stopApexService() {
  const child = apexService;
  apexService = null;
  if (!child || child.exitCode !== null) return;
  child.kill("SIGTERM");
  await new Promise((resolve) => {
    const timer = setTimeout(() => {
      if (child.exitCode === null) child.kill("SIGKILL");
      resolve();
    }, 1_500);
    child.once("exit", () => {
      clearTimeout(timer);
      resolve();
    });
  });
}

function createWindow(renderer) {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 960,
    minWidth: 980,
    minHeight: 680,
    title: "Apex Code",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      preload: path.join(__dirname, "preload.cjs"),
      additionalArguments: [`--apex-api-base=${apexServiceUrl}`],
    },
  });
  mainWindow.on("closed", () => { mainWindow = null; });
  void mainWindow.loadFile(path.join(renderer, "index.html"));
}

ipcMain.handle("apex:select-project", async () => {
  if (!mainWindow) return null;
  const e2eProject = process.env.APEX_DESKTOP_E2E === "1" ? process.env.APEX_DESKTOP_TEST_PROJECT?.trim() : "";
  if (e2eProject && path.isAbsolute(e2eProject) && existsSync(e2eProject)) {
    return path.resolve(e2eProject);
  }
  const result = await dialog.showOpenDialog(mainWindow, {
    title: "Open Apex project",
    properties: ["openDirectory", "createDirectory"],
  });
  return result.canceled ? null : result.filePaths[0] ?? null;
});

ipcMain.handle("apex:platform", () => ({ platform: process.platform, arch: process.arch }));
ipcMain.handle("apex:get-provider-state", async () => providerVault.publicState(await serviceProviderState()));
ipcMain.handle("apex:set-provider-selection", async (_event, selection) => {
  providerVault.setSelection(selection?.provider_id, selection?.model_id);
  await syncProviderRuntime();
  return providerVault.publicState(await serviceProviderState());
});
ipcMain.handle("apex:save-provider-credential", async (_event, input) => {
  providerVault.saveCredential(input?.provider_id, input?.secret);
  await syncProviderRuntime();
  return providerVault.publicState(await serviceProviderState());
});
ipcMain.handle("apex:delete-provider-credential", async (_event, providerId) => {
  providerVault.deleteCredential(providerId);
  await syncProviderRuntime();
  return providerVault.publicState(await serviceProviderState());
});
ipcMain.handle("apex:test-provider", async () => {
  const selection = providerVault.getSelection();
  const credential = selection ? providerVault.resolveCredential(selection.provider_id) : null;
  if (!selection || !credential) return { status: "NO_CREDENTIAL", message: "Configure a credential before testing this provider." };
  return internalPost("/api/internal/provider-test", {
    provider_id: selection.provider_id,
    model_id: selection.model_id,
    credential,
  });
});

app.on("before-quit", (event) => {
  if (shuttingDown) return;
  event.preventDefault();
  shuttingDown = true;
  void stopApexService().finally(() => app.exit(0));
});

app.whenReady().then(async () => {
  if (!hasInstanceLock || !app.isReady() || shuttingDown) return;
  try {
    providerVault = new ProviderVault(app.getPath("userData"), safeStorage);
    const { renderer } = await startApexService();
    await syncProviderRuntime();
    createWindow(renderer);
  } catch {
    await stopApexService();
    dialog.showErrorBox("Apex Code could not start", "The local Apex Core service could not be started safely.");
    app.quit();
  }
});
