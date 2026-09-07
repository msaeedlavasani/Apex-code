import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { ProviderVault } from "../src/provider-vault.mjs";

function fakeSafeStorage() {
  return {
    isEncryptionAvailable: () => true,
    encryptString: (value) => Buffer.from(`encrypted:${value}`, "utf8"),
    decryptString: (value) => Buffer.from(value).toString("utf8").replace(/^encrypted:/, ""),
  };
}

test("provider vault persists selection and encrypted credential status without plaintext", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "apex-provider-vault-"));
  try {
    const vault = new ProviderVault(root, fakeSafeStorage());
    vault.setSelection("openai", "gpt-4o-mini");
    vault.saveCredential("openai", "unit-test-secret");
    const raw = fs.readFileSync(path.join(root, "apex-provider-state.json"), "utf8");
    assert.equal(raw.includes("unit-test-secret"), false);
    assert.equal(vault.publicState().credential_status, "CONFIGURED");
    assert.equal(Object.hasOwn(vault.publicState(), "credential"), false);

    const reloaded = new ProviderVault(root, fakeSafeStorage());
    assert.deepEqual(reloaded.getSelection(), { provider_id: "openai", model_id: "gpt-4o-mini" });
    assert.equal(reloaded.credentialStatus("openai"), "CONFIGURED");
    reloaded.deleteCredential("openai");
    assert.equal(reloaded.credentialStatus("openai"), "NOT_CONFIGURED");
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
