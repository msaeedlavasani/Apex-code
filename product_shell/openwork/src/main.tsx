import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ApexOpenWorkShell } from "./ApexOpenWorkShell";
import "./styles.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ApexOpenWorkShell />
  </StrictMode>,
);
