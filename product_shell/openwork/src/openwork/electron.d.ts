export {};

declare global {
  interface Window {
    __APEX_DESKTOP__?: {
      apiBase: string;
      selectProject: () => Promise<string | null>;
      platform: () => Promise<{ platform: string; arch: string }>;
      getProviderState: () => Promise<ApexDesktopProviderState>;
      setProviderSelection: (selection: { provider_id: string; model_id: string }) => Promise<ApexDesktopProviderState>;
      saveProviderCredential: (input: { provider_id: string; secret: string }) => Promise<ApexDesktopProviderState>;
      deleteProviderCredential: (providerId: string) => Promise<ApexDesktopProviderState>;
      testProvider: () => Promise<{ status: string; message: string }>;
    };
  }

  interface Window {
    __OPENWORK_ELECTRON__?: {
      invokeDesktop?: (command: string, ...args: unknown[]) => Promise<unknown>;
    };
  }
}

type ApexDesktopProviderState = {
  providers: Array<{
    provider_id: string;
    display_name: string;
    configured: boolean;
    credential_status: string;
    models: Array<{ model_id: string; display_name: string }>;
  }>;
  selection: { provider_id: string; model_id: string } | null;
  credential_status: string;
  secure_storage: string;
};
