"""Bounded local application boundary for the first Apex product shell.

The application boundary exposes queries and one safe command.  It delegates
all execution ownership to :class:`ExecutionCoordinator`; the shell never
constructs Tasks or Attempts and never writes the execution ledger directly.
"""

from __future__ import annotations

import json
import threading
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .core import ExecutionCoordinator
from .reconciliation import ReconciliationLoop


class ApplicationError(RuntimeError):
    """A safe application-boundary request error."""


class ProjectSelectionError(ApplicationError):
    """The requested local project cannot be opened."""


class TaskBusyError(ApplicationError):
    """The selected workspace already has a shell-submitted task in flight."""


@dataclass
class _Job:
    job_id: str
    workspace: Path
    task_type: str
    future: Future[dict[str, Any]]


class ApexApplication:
    """Small local application service backed by the canonical Apex Core."""

    TASKS = {
        "report": "REPORT.md",
        "summary": "SUMMARY.md",
    }

    def __init__(self, adapter: Any | None = None) -> None:
        self.coordinator = ExecutionCoordinator(adapter)
        self.workspace: Path | None = None
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="apex-core")
        self._jobs: dict[str, _Job] = {}
        self._lock = threading.RLock()

    def close(self) -> None:
        self._executor.shutdown(wait=False, cancel_futures=False)

    def open_project(self, raw_path: str | Path) -> dict[str, Any]:
        if not str(raw_path).strip():
            raise ProjectSelectionError("project path is required")
        candidate = Path(raw_path).expanduser().resolve()
        if not candidate.is_dir():
            raise ProjectSelectionError("project path must be an existing directory")
        self.workspace = candidate
        self._startup_reconcile(candidate)
        return self.project_summary()

    def project_summary(self) -> dict[str, Any]:
        if self.workspace is None:
            return {"selected": False}
        entries: list[dict[str, Any]] = []
        try:
            children = sorted(self.workspace.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
        except OSError as exc:
            raise ProjectSelectionError("project contents could not be listed") from exc
        for child in children:
            # The shell shows names only and omits hidden/credential-shaped
            # entries. It never reads files for the project overview.
            if child.name.startswith(".") or self._looks_sensitive(child.name):
                continue
            entries.append({"name": child.name, "kind": "directory" if child.is_dir() else "file"})
        return {
            "selected": True,
            "name": self.workspace.name or str(self.workspace),
            "path": str(self.workspace),
            "entries": entries,
        }

    def submit_task(self, task_type: str = "report") -> dict[str, Any]:
        if self.workspace is None:
            raise ApplicationError("open a project before submitting a task")
        if task_type not in self.TASKS:
            raise ApplicationError("task must be report or summary")
        workspace = self.workspace
        readme = workspace / "README.md"
        if not readme.is_file() or readme.is_symlink():
            raise ApplicationError("selected project must contain a regular README.md")
        with self._lock:
            if any(not job.future.done() and job.workspace == workspace for job in self._jobs.values()):
                raise TaskBusyError("a bounded task is already running for this workspace")
            job_id = f"shell_{uuid.uuid4().hex[:16]}"
            runner = self.coordinator.run_report if task_type == "report" else self.coordinator.run_summary
            future = self._executor.submit(runner, workspace)
            self._jobs[job_id] = _Job(job_id, workspace, task_type, future)
        return {"job_id": job_id, "state": "SUBMITTED", "task_type": task_type, "workspace": str(workspace)}

    def status(self) -> dict[str, Any]:
        if self.workspace is None:
            return {"selected": False, "state": "NO_PROJECT"}
        history = self._history(self.workspace)
        with self._lock:
            jobs = [job for job in self._jobs.values() if job.workspace == self.workspace]
        latest = history[0] if history else None
        job_state = None
        job_error = None
        if jobs:
            job = jobs[-1]
            if job.future.done():
                try:
                    job.future.result()
                except Exception as exc:  # surface a safe message; no traceback/secret data
                    job_error = str(exc)
                job_state = "COMPLETED" if job_error is None else "FAILED"
            else:
                job_state = "RUNNING"
        return {
            "selected": True,
            "workspace": str(self.workspace),
            "state": self._display_state(latest, job_state),
            "job_state": job_state,
            "job_error": job_error,
            "execution": latest,
        }

    def history(self) -> dict[str, Any]:
        if self.workspace is None:
            return {"selected": False, "executions": []}
        return {"selected": True, "workspace": str(self.workspace), "executions": self._history(self.workspace)}

    def artifact(self, name: str) -> dict[str, Any]:
        if self.workspace is None:
            raise ApplicationError("open a project before reading an artifact")
        if name not in set(self.TASKS.values()):
            raise ApplicationError("artifact is outside the bounded result contract")
        snapshot = self._snapshot(self.workspace)
        record = snapshot.get("artifacts", {}).get(name)
        if not isinstance(record, dict) or record.get("path") != name:
            raise ApplicationError("artifact is not recorded as a Core result")
        path = self.workspace / name
        if path.resolve() != self.workspace / name or not path.is_file() or path.is_symlink():
            raise ApplicationError("artifact is not a safe regular file")
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise ApplicationError("artifact could not be read") from exc
        return {"name": name, "content": content, "sha256": record.get("sha256"), "attempt_id": record.get("attempt_id")}

    def _startup_reconcile(self, workspace: Path) -> None:
        ledger_path = workspace / "execution-ledger.json"
        if ledger_path.is_file():
            # No observation is fabricated on shell startup. Existing
            # non-terminal Attempts therefore remain fenced and become
            # RECOVERY_REQUIRED through the Core reconciliation policy.
            ReconciliationLoop(ledger_path).reconcile([])

    @staticmethod
    def _snapshot(workspace: Path) -> dict[str, Any]:
        ledger_path = workspace / "execution-ledger.json"
        if not ledger_path.is_file():
            return {"attempts": {}, "tasks": {}, "results": {}, "events": [], "artifacts": {}}
        try:
            return json.loads(ledger_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ApplicationError("execution history is unavailable") from exc

    @classmethod
    def _history(cls, workspace: Path) -> list[dict[str, Any]]:
        data = cls._snapshot(workspace)
        attempts = data.get("attempts", {})
        tasks = data.get("tasks", {})
        results = data.get("results", {})
        records: list[dict[str, Any]] = []
        if not isinstance(attempts, dict):
            return records
        for attempt_id, attempt in attempts.items():
            if not isinstance(attempt, dict):
                continue
            task_id = attempt.get("task_id")
            task = tasks.get(task_id, {}) if isinstance(tasks, dict) else {}
            result = results.get(attempt_id, {}) if isinstance(results, dict) else {}
            if not isinstance(task, dict):
                task = {}
            if not isinstance(result, dict):
                result = {}
            records.append(
                {
                    "attempt_id": attempt_id,
                    "task_id": task_id,
                    "title": task.get("title"),
                    "status": attempt.get("status"),
                    "reconciliation_state": attempt.get("reconciliation_state"),
                    "runtime_fact": result.get("runtime_fact", attempt.get("last_runtime_fact")),
                    "runtime_session_id": result.get("runtime_session_id", attempt.get("runtime_session_id")),
                    "runtime_identity": result.get("runtime_identity", attempt.get("runtime_identity")),
                    "semantic_success": result.get("semantic_success"),
                    "verification": result.get("verification"),
                    "verification_reason": result.get("verification_reason"),
                    "artifact": result.get("artifact"),
                    "manifest_id": attempt.get("manifest_id"),
                    "execution_epoch_id": attempt.get("execution_epoch_id"),
                    "authority_revision_id": attempt.get("authority_revision_id"),
                    "runtime_lane_id": attempt.get("runtime_lane_id"),
                }
            )
        return list(reversed(records))

    @staticmethod
    def _display_state(latest: dict[str, Any] | None, job_state: str | None) -> str:
        # A live shell job is not semantically complete until the Core call
        # has returned and finished its durable artifact/event writes.
        if job_state == "RUNNING":
            return "RUNNING"
        if job_state == "FAILED":
            return "RECOVERY_REQUIRED" if latest is not None else "FAILED"
        if latest is None:
            return job_state or "READY"
        if latest.get("reconciliation_state"):
            return str(latest["reconciliation_state"])
        if latest.get("semantic_success") is True:
            return "SUCCEEDED"
        if latest.get("runtime_fact") in {"UNKNOWN", "UNREACHABLE", "MISMATCH"}:
            return "RECOVERY_REQUIRED"
        if latest.get("runtime_fact") == "MISSING":
            return "LOST"
        if latest.get("semantic_success") is False and latest.get("verification") == "FAIL":
            return "VERIFICATION_FAILED"
        return str(latest.get("status") or job_state or "UNKNOWN")

    @staticmethod
    def _looks_sensitive(name: str) -> bool:
        lowered = name.lower()
        return lowered in {"credentials", "credentials.json", "id_rsa"} or lowered.startswith(".env") or lowered.endswith((".pem", ".key", ".p12", ".pfx"))


def create_application(adapter: Any | None = None) -> ApexApplication:
    """Factory kept small so tests and the local shell can inject an adapter."""

    return ApexApplication(adapter)
