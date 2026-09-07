const { contextBridge, ipcRenderer } = require("electron");

const apiBaseArgument = process.argv.find((argument) => argument.startsWith("--apex-api-base="));
const apiBase = apiBaseArgument ? apiBaseArgument.slice("--apex-api-base=".length) : "";

contextBridge.exposeInMainWorld("__APEX_DESKTOP__", {
  apiBase,
  selectProject() {
    return ipcRenderer.invoke("apex:select-project");
  },
  platform() {
    return ipcRenderer.invoke("apex:platform");
  },
});
