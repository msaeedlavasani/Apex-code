import path from "node:path";

export const LOOPBACK_HOST = "127.0.0.1";

export function serviceArguments() {
  return ["-m", "apex_code.shell", "--ui", "openwork", "--host", LOOPBACK_HOST, "--port", "0"];
}

export function serviceEnvironment(baseEnvironment, runtimeRoot, internalToken = "") {
  const allowed = ["PATH", "HOME", "TMPDIR", "USER", "LANG", "LC_ALL", "LC_CTYPE", "TERM"];
  const environment = Object.fromEntries(
    allowed
      .filter((name) => typeof baseEnvironment[name] === "string" && baseEnvironment[name].length > 0)
      .map((name) => [name, baseEnvironment[name]]),
  );
  const serviceEnv = {
    ...environment,
    APEX_DESKTOP: "1",
    PYTHONPATH: runtimeRoot,
    PYTHONUNBUFFERED: "1",
  };
  if (internalToken) serviceEnv.APEX_INTERNAL_TOKEN = internalToken;
  return serviceEnv;
}

export function parseServiceUrl(output) {
  const match = output.match(/Apex Code shell listening at http:\/\/127\.0\.0\.1:(\d+)/);
  return match ? `http://${LOOPBACK_HOST}:${match[1]}` : null;
}

export function isLoopbackUrl(rawUrl) {
  try {
    const url = new URL(rawUrl);
    return url.protocol === "http:" && (url.hostname === LOOPBACK_HOST || url.hostname === "[::1]" || url.hostname === "::1");
  } catch {
    return false;
  }
}

export function runtimeRoot({ isPackaged, resourcesPath, desktopRoot }) {
  return isPackaged ? path.join(resourcesPath, "apex-runtime") : path.resolve(desktopRoot, "../..");
}

export function rendererRoot({ isPackaged, resourcesPath, desktopRoot }) {
  return isPackaged
    ? path.join(resourcesPath, "apex-runtime", "product_shell", "openwork", "dist")
    : path.resolve(desktopRoot, "../openwork", "dist");
}
