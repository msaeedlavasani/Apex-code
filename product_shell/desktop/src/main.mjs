import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { app, BrowserWindow, dialog, ipcMain } from "electron";
import {
  isLoopbackUrl,
  parseServiceUrl,
  rendererRoot,
  runtimeRoot,
  serviceArguments,
  serviceEnvironment,
} from "./service.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const desktopRoot = path.resolve(__dirname, "..");
let mainWindow = null;
let apexService = null;
let apexServiceUrl = null;
let shuttingDown = false;

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
    env: serviceEnvironment(process.env, root),
    shell: false,
    stdio: ["ignore", "pipe", "ignore"],
  });
  apexServiceUrl = await waitForService(apexService);
  await healthCheck(apexServiceUrl);
  return { renderer };
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

app.on("before-quit", (event) => {
  if (shuttingDown) return;
  event.preventDefault();
  shuttingDown = true;
  void stopApexService().finally(() => app.exit(0));
});

app.whenReady().then(async () => {
  if (!hasInstanceLock || !app.isReady() || shuttingDown) return;
  try {
    const { renderer } = await startApexService();
    createWindow(renderer);
  } catch {
    await stopApexService();
    dialog.showErrorBox("Apex Code could not start", "The local Apex Core service could not be started safely.");
    app.quit();
  }
});
