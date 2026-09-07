export {};

declare global {
  interface Window {
    __APEX_DESKTOP__?: {
      apiBase: string;
      selectProject: () => Promise<string | null>;
      platform: () => Promise<{ platform: string; arch: string }>;
    };
  }

  interface Window {
    __OPENWORK_ELECTRON__?: {
      invokeDesktop?: (command: string, ...args: unknown[]) => Promise<unknown>;
    };
  }
}
