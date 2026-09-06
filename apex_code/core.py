"""Core primitives for the first safe executable vertical slice."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from .runtime import OpenCodeRuntimeAdapter, RuntimeExecution


class SafetyError(RuntimeError):
    """A fail-closed execution or authority condition."""


class AuthorityDenied(SafetyError):
    """An operation is outside the Core-owned PermissionEnvelope."""


class RuntimeFact(str, Enum):
    RUNNING = "RUNNING"
    EXITED = "EXITED"
    MISSING = "MISSING"
    UNREACHABLE = "UNREACHABLE"
    MISMATCH = "MISMATCH"
    UNKNOWN = "UNKNOWN"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class ExecutionRequest:
    request_id: str
    objective: str
    workspace: str


@dataclass
class Execution:
    execution_id: str
    request_id: str
    status: str = "CREATED"


@dataclass
class Task:
    task_id: str
    execution_id: str
    title: str
    semantic_state: str = "PENDING"


@dataclass(frozen=True)
class PermissionEnvelope:
    read_paths: tuple[str, ...]
    write_paths: tuple[str, ...]
    denied_paths: tuple[str, ...]


@dataclass(frozen=True)
class AuthorityRevision:
    authority_revision_id: str
    envelope: PermissionEnvelope
    created_at: str

    @property
    def content_digest(self) -> str:
        return digest(asdict(self))


@dataclass(frozen=True)
class ExecutionManifest:
    manifest_id: str
    attempt_id: str
    task_id: str
    authority_revision_id: str
    agent_selection: str
    model_selection: str
    runtime_requirement: str
    workspace_snapshot: str
    created_at: str


@dataclass(frozen=True)
class RuntimeLane:
    runtime_lane_id: str
    attempt_id: str
    workspace: str
    created_at: str


@dataclass(frozen=True)
class AuthorityEvidence:
    authority_revision_id: str
    authority_digest: str
    runtime_lane_id: str
    attempt_id: str
    execution_epoch_id: str
    materialized: bool
    substrate_activation_confirmed: bool
    binding_mode: str


@dataclass
class Attempt:
    attempt_id: str
    task_id: str
    execution_epoch_id: str
    status: str
    manifest: ExecutionManifest
    lane: RuntimeLane
    authority: AuthorityRevision
    barrier: str = "CLOSED"
    runtime_session_id: str | None = None
    result: dict[str, Any] | None = None


class ExecutionLedger:
    """Small atomic JSON ledger for sufficient slice evidence."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.data: dict[str, Any] = {
            "requests": {},
            "executions": {},
            "tasks": {},
            "attempts": {},
            "manifests": {},
            "authorities": {},
            "lanes": {},
            "barriers": {},
            "events": [],
            "artifacts": {},
            "results": {},
        }
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8"))

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=f".{self.path.name}.", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(self.data, stream, indent=2, sort_keys=True)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def put(self, collection: str, key: str, value: dict[str, Any]) -> None:
        self.data[collection][key] = value
        self._save()

    def event(self, event_type: str, payload: dict[str, Any]) -> None:
        self.data["events"].append(
            {
                "event_id": new_id("evt"),
                "event_type": event_type,
                "occurred_at": now(),
                "payload": payload,
            }
        )
        self._save()


class ExecutionBarrier:
    """Core gate for the bounded Core-mediated authority mode."""

    @staticmethod
    def release(manifest: ExecutionManifest, lane: RuntimeLane, evidence: AuthorityEvidence) -> None:
        if not evidence.materialized:
            raise SafetyError("authority is not materialized")
        if evidence.authority_revision_id != manifest.authority_revision_id:
            raise SafetyError("authority revision mismatch")
        if evidence.runtime_lane_id != lane.runtime_lane_id or evidence.attempt_id != manifest.attempt_id:
            raise SafetyError("runtime identity mismatch")
        if evidence.binding_mode != "CORE_MEDIATED_NO_RUNTIME_IO":
            raise SafetyError("unsupported authority binding mode")
        # This is a bounded Core-owned fence: OpenCode is granted no file or
        # shell authority, so Core retains the only side-effect path. It is not
        # proof that OpenCode itself activated Apex authority.
        return


class ExecutionCoordinator:
    """Create, gate, execute, verify, and persist one safe slice."""

    def __init__(self, adapter: OpenCodeRuntimeAdapter | None = None) -> None:
        self.adapter = adapter or OpenCodeRuntimeAdapter()

    @staticmethod
    def _authority() -> AuthorityRevision:
        return AuthorityRevision(
            authority_revision_id="ar_slice_report_001",
            envelope=PermissionEnvelope(
                read_paths=("README.md",),
                write_paths=("REPORT.md",),
                denied_paths=("../**", "~/.ssh/**", "~/.aws/**", "~/.config/**"),
            ),
            created_at=now(),
        )

    @staticmethod
    def _safe_path(workspace: Path, relative: str, operation: str) -> Path:
        root = workspace.resolve()
        raw = root / relative
        if raw.is_symlink():
            raise AuthorityDenied(f"symlink target denied: {relative}")
        candidate = raw.resolve()
        if candidate.parent != root or candidate == root:
            raise AuthorityDenied(f"{operation} denied outside bounded workspace: {relative}")
        if operation == "read" and relative != "README.md":
            raise AuthorityDenied(f"read denied by PermissionEnvelope: {relative}")
        if operation == "write" and relative != "REPORT.md":
            raise AuthorityDenied(f"write denied by PermissionEnvelope: {relative}")
        return candidate

    def run_report(self, workspace: Path) -> dict[str, Any]:
        workspace = workspace.resolve()
        if not workspace.is_dir():
            raise SafetyError(f"workspace missing: {workspace}")
        ledger = ExecutionLedger(workspace / "execution-ledger.json")
        request = ExecutionRequest(new_id("req"), "Inspect README and create REPORT.md", str(workspace))
        execution = Execution(new_id("exec"), request.request_id)
        task = Task(new_id("task"), execution.execution_id, request.objective)
        authority = self._authority()
        attempt_id = new_id("att")
        epoch_id = new_id("epoch")
        lane = RuntimeLane(new_id("lane"), attempt_id, str(workspace), now())
        manifest = ExecutionManifest(
            manifest_id=new_id("manifest"),
            attempt_id=attempt_id,
            task_id=task.task_id,
            authority_revision_id=authority.authority_revision_id,
            agent_selection="opencode-worker",
            model_selection=self.adapter.model,
            runtime_requirement="text-worker-no-runtime-filesystem-io",
            workspace_snapshot=digest({"workspace": str(workspace), "read": "README.md"}),
            created_at=now(),
        )
        attempt = Attempt(attempt_id, task.task_id, epoch_id, "CREATED", manifest, lane, authority)
        ledger.put("executions", execution.execution_id, asdict(execution))
        ledger.put("requests", request.request_id, asdict(request))
        ledger.put("tasks", task.task_id, asdict(task))
        ledger.put("manifests", manifest.manifest_id, asdict(manifest))
        ledger.put("authorities", authority.authority_revision_id, asdict(authority))
        ledger.put("lanes", lane.runtime_lane_id, asdict(lane))
        ledger.put(
            "attempts",
            attempt.attempt_id,
            {
                "attempt_id": attempt.attempt_id,
                "task_id": attempt.task_id,
                "execution_epoch_id": attempt.execution_epoch_id,
                "status": attempt.status,
                "barrier": attempt.barrier,
                "manifest_id": manifest.manifest_id,
                "authority_revision_id": authority.authority_revision_id,
                "runtime_lane_id": lane.runtime_lane_id,
            },
        )
        ledger.event("attempt.created", {"attempt_id": attempt_id, "task_id": task.task_id})
        ledger.event("manifest.created", {"manifest_id": manifest.manifest_id, "immutable": True})

        readme_path = self._safe_path(workspace, "README.md", "read")
        readme = readme_path.read_text(encoding="utf-8")
        if not readme.strip():
            raise SafetyError("README.md is empty")
        authority_evidence = AuthorityEvidence(
            authority_revision_id=authority.authority_revision_id,
            authority_digest=authority.content_digest,
            runtime_lane_id=lane.runtime_lane_id,
            attempt_id=attempt_id,
            execution_epoch_id=epoch_id,
            materialized=False,
            substrate_activation_confirmed=False,
            binding_mode="CORE_MEDIATED_NO_RUNTIME_IO",
        )
        # The adapter materializes its deny-all configuration before the
        # barrier. The digest is then checked against Core's immutable revision.
        config_dir, materialized_digest = self.adapter.materialize_authority(authority.content_digest)
        authority_evidence = AuthorityEvidence(
            **{**asdict(authority_evidence), "materialized": True, "authority_digest": materialized_digest}
        )
        if authority_evidence.authority_digest != authority.content_digest:
            raise SafetyError("materialized authority digest mismatch")
        ledger.event(
            "authority.materialized",
            {
                "authority_revision_id": authority.authority_revision_id,
                "authority_digest": authority.content_digest,
                "config_dir": config_dir,
                "substrate_activation_confirmed": False,
            },
        )
        ExecutionBarrier.release(manifest, lane, authority_evidence)
        ledger.put("barriers", attempt_id, {**asdict(authority_evidence), "state": "RELEASED"})
        attempt.status = "RUNNING"
        attempt.barrier = "RELEASED"
        ledger.put("attempts", attempt_id, {**ledger.data["attempts"][attempt_id], "status": attempt.status, "barrier": attempt.barrier})
        ledger.event("execution.barrier_released", {"attempt_id": attempt_id, "mode": authority_evidence.binding_mode})

        prompt = self._prompt(readme)
        runtime: RuntimeExecution = self.adapter.execute(
            prompt,
            authority.content_digest,
            workspace,
            config_dir=config_dir,
        )
        attempt.runtime_session_id = runtime.session_id
        ledger.event(
            "runtime.fact",
            {
                "attempt_id": attempt_id,
                "runtime_session_id": runtime.session_id,
                "fact": runtime.fact,
                "exit_code": runtime.exit_code,
            },
        )
        report = self._extract_report(runtime.text)
        verified = False
        artifact_path: Path | None = None
        verification_reason = "runtime completion is not semantic success"
        if runtime.fact == RuntimeFact.EXITED.value and runtime.exit_code == 0 and report:
            artifact_path = self._safe_path(workspace, "REPORT.md", "write")
            if artifact_path.exists() and artifact_path.is_symlink():
                raise AuthorityDenied("existing REPORT.md symlink denied")
            artifact_path.write_text(report, encoding="utf-8")
            verified = artifact_path.read_text(encoding="utf-8") == report
            verification_reason = "Core verified exact bounded artifact write and readback"
        semantic_success = bool(verified)
        task.semantic_state = "SUCCEEDED" if semantic_success else "UNKNOWN"
        attempt.status = "SUCCEEDED" if semantic_success else "FAILED"
        result = {
            "attempt_id": attempt_id,
            "runtime_fact": runtime.fact,
            "runtime_session_id": runtime.session_id,
            "exit_code": runtime.exit_code,
            "runtime_event_count": runtime.event_count,
            "runtime_text_digest": digest(runtime.text),
            "semantic_success": semantic_success,
            "verification": "PASS" if verified else "FAIL",
            "verification_reason": verification_reason,
            "artifact": "REPORT.md" if artifact_path else None,
            "authority_binding": "CORE_MEDIATED_NO_RUNTIME_IO",
            "substrate_authority_activation": "NOT_PROVEN",
        }
        ledger.put("results", attempt_id, result)
        ledger.put("tasks", task.task_id, {**asdict(task), "semantic_state": task.semantic_state})
        ledger.put("attempts", attempt_id, {**ledger.data["attempts"][attempt_id], "status": attempt.status, "runtime_session_id": runtime.session_id})
        if artifact_path:
            ledger.put("artifacts", "REPORT.md", {"path": "REPORT.md", "sha256": sha256_file(artifact_path), "attempt_id": attempt_id})
        ledger.event("verification.completed", {"attempt_id": attempt_id, "result": result["verification"]})
        ledger.event("task.semantic_state", {"task_id": task.task_id, "state": task.semantic_state})
        return {
            "execution_id": execution.execution_id,
            "task_id": task.task_id,
            "attempt_id": attempt_id,
            "manifest_id": manifest.manifest_id,
            "runtime_session_id": runtime.session_id,
            "runtime_fact": runtime.fact,
            "semantic_success": semantic_success,
            "verification": result["verification"],
            "artifact": result["artifact"],
            "ledger": str(ledger.path),
            "authority_revision_id": authority.authority_revision_id,
            "authority_digest": authority.content_digest,
            "substrate_authority_activation": "NOT_PROVEN",
        }

    @staticmethod
    def _prompt(readme: str) -> str:
        return (
            "You are a bounded report-writing worker. Do not use tools and do not read or write files. "
            "Using only the README content supplied below, return exactly a concise Markdown report "
            "between the markers REPORT_CONTENT_BEGIN and REPORT_CONTENT_END. The report must state "
            "the repository/product name, its purpose, and that this report was generated by the "
            "Apex Code safe vertical slice. Do not include any other markers or tool calls.\n\n"
            "README CONTENT:\n---\n"
            + readme
            + "\n---\n"
            "REPORT_CONTENT_BEGIN\n"
            "REPORT_CONTENT_END"
        )

    @staticmethod
    def _extract_report(text: str) -> str | None:
        start = "REPORT_CONTENT_BEGIN"
        end = "REPORT_CONTENT_END"
        if start not in text or end not in text:
            return None
        body = text.split(start, 1)[1].split(end, 1)[0].strip()
        if not body or "REPORT_CONTENT_BEGIN" in body or "REPORT_CONTENT_END" in body:
            return None
        return body + "\n"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
