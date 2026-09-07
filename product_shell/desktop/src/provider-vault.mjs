import fs from "node:fs";
import path from "node:path";

const STATE_VERSION = 1;

function validProviderId(providerId) {
  return typeof providerId === "string" && /^[a-z][a-z0-9-]{1,31}$/.test(providerId);
}

function cleanSelection(selection) {
  if (!selection || !validProviderId(selection.provider_id) || typeof selection.model_id !== "string" || !selection.model_id.trim()) {
    return null;
  }
  return { provider_id: selection.provider_id, model_id: selection.model_id.trim() };
}

export class ProviderVault {
  constructor(userDataPath, safeStorage) {
    this.userDataPath = userDataPath;
    this.safeStorage = safeStorage;
    this.statePath = path.join(userDataPath, "apex-provider-state.json");
    this.state = this.load();
  }

  isAvailable() {
    return Boolean(this.safeStorage?.isEncryptionAvailable?.());
  }

  getSelection() {
    return this.state.selection ? { ...this.state.selection } : null;
  }

  setSelection(providerId, modelId) {
    const selection = cleanSelection({ provider_id: providerId, model_id: modelId });
    if (!selection) throw new Error("provider/model selection is invalid");
    this.state.selection = selection;
    this.persist();
    return this.getSelection();
  }

  credentialStatus(providerId) {
    return this.state.credentials[providerId]?.encrypted
      ? "CONFIGURED"
      : "NOT_CONFIGURED";
  }

  saveCredential(providerId, secret) {
    if (!validProviderId(providerId) || typeof secret !== "string" || !secret.trim()) {
      throw new Error("provider credential is required");
    }
    if (!this.isAvailable()) {
      throw new Error("OS-backed secure storage is unavailable");
    }
    const encrypted = this.safeStorage.encryptString(secret);
    this.state.credentials[providerId] = {
      encrypted: Buffer.from(encrypted).toString("base64"),
    };
    this.persist();
    return this.credentialStatus(providerId);
  }

  deleteCredential(providerId) {
    delete this.state.credentials[providerId];
    this.persist();
    return this.credentialStatus(providerId);
  }

  resolveCredential(providerId) {
    const encoded = this.state.credentials[providerId]?.encrypted;
    if (!encoded || !this.isAvailable()) return null;
    return this.safeStorage.decryptString(Buffer.from(encoded, "base64"));
  }

  publicState(serviceState = null) {
    return {
      ...(serviceState || {}),
      selection: this.getSelection(),
      secure_storage: this.isAvailable() ? "OS_BACKED" : "UNAVAILABLE",
      credential_status: this.state.selection
        ? this.credentialStatus(this.state.selection.provider_id)
        : "NOT_CONFIGURED",
    };
  }

  load() {
    try {
      const parsed = JSON.parse(fs.readFileSync(this.statePath, "utf8"));
      return {
        version: STATE_VERSION,
        selection: cleanSelection(parsed.selection),
        credentials: parsed.credentials && typeof parsed.credentials === "object" ? parsed.credentials : {},
      };
    } catch {
      return { version: STATE_VERSION, selection: null, credentials: {} };
    }
  }

  persist() {
    fs.mkdirSync(this.userDataPath, { recursive: true, mode: 0o700 });
    const temporary = `${this.statePath}.tmp-${process.pid}`;
    const safeState = {
      version: STATE_VERSION,
      selection: this.state.selection,
      credentials: this.state.credentials,
    };
    fs.writeFileSync(temporary, `${JSON.stringify(safeState, null, 2)}\n`, { mode: 0o600 });
    fs.renameSync(temporary, this.statePath);
  }
}

export { cleanSelection, validProviderId };
