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
  getProviderState() {
    return ipcRenderer.invoke("apex:get-provider-state");
  },
  setProviderSelection(selection) {
    return ipcRenderer.invoke("apex:set-provider-selection", selection);
  },
  saveProviderCredential(input) {
    return ipcRenderer.invoke("apex:save-provider-credential", input);
  },
  deleteProviderCredential(providerId) {
    return ipcRenderer.invoke("apex:delete-provider-credential", providerId);
  },
  testProvider() {
    return ipcRenderer.invoke("apex:test-provider");
  },
});
