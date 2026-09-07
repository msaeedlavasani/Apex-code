import assert from "node:assert/strict";
import test from "node:test";
import path from "node:path";
import {
  isLoopbackUrl,
  parseServiceUrl,
  rendererRoot,
  runtimeRoot,
  serviceArguments,
  serviceEnvironment,
  LOOPBACK_HOST,
} from "../src/service.mjs";

test("service command is loopback-only and chooses an ephemeral port", () => {
  assert.deepEqual(serviceArguments(), ["-m", "apex_code.shell", "--ui", "openwork", "--host", LOOPBACK_HOST, "--port", "0"]);
  assert.equal(parseServiceUrl("Apex Code shell listening at http://127.0.0.1:43123"), "http://127.0.0.1:43123");
  assert.equal(parseServiceUrl("Apex Code shell listening at http://0.0.0.0:43123"), null);
  assert.equal(isLoopbackUrl("http://127.0.0.1:43123"), true);
  assert.equal(isLoopbackUrl("http://192.0.2.1:43123"), false);
});

test("desktop service environment excludes ambient credentials", () => {
  const env = serviceEnvironment({ PATH: "/bin", HOME: "/tmp/home", API_KEY: "must-not-pass", SECRET_TOKEN: "must-not-pass" }, "/tmp/apex-runtime");
  assert.equal(env.PYTHONPATH, "/tmp/apex-runtime");
  assert.equal(env.APEX_DESKTOP, "1");
  assert.equal(Object.hasOwn(env, "API_KEY"), false);
  assert.equal(Object.hasOwn(env, "SECRET_TOKEN"), false);
});

test("desktop service receives only its internal broker token explicitly", () => {
  const env = serviceEnvironment({ PATH: "/bin", OPENAI_API_KEY: "must-not-pass" }, "/tmp/apex-runtime", "broker-token");
  assert.equal(env.APEX_INTERNAL_TOKEN, "broker-token");
  assert.equal(Object.hasOwn(env, "OPENAI_API_KEY"), false);
});

test("packaged and development roots are deterministic", () => {
  const desktopRoot = "/repo/product_shell/desktop";
  assert.equal(runtimeRoot({ isPackaged: false, resourcesPath: "/resources", desktopRoot }), "/repo");
  assert.equal(rendererRoot({ isPackaged: false, resourcesPath: "/resources", desktopRoot }), path.resolve("/repo/product_shell/openwork/dist"));
  assert.equal(runtimeRoot({ isPackaged: true, resourcesPath: "/resources", desktopRoot }), "/resources/apex-runtime");
  assert.equal(rendererRoot({ isPackaged: true, resourcesPath: "/resources", desktopRoot }), "/resources/apex-runtime/product_shell/openwork/dist");
});
