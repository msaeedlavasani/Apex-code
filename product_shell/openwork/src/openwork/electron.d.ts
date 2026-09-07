export {};

declare global {
  interface Window {
    __OPENWORK_ELECTRON__?: {
      invokeDesktop?: (command: string, ...args: unknown[]) => Promise<unknown>;
    };
  }
}
