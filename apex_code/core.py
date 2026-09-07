"""Core primitives for the first safe executable vertical slice."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .contract import RuntimeAdapter, RuntimeExecution, RuntimeFact, RuntimeIdentity
from .events import EventEnvelope


class SafetyError(RuntimeError):
    """A fail-closed execution or authority condition."""


class AuthorityDenied(SafetyError):
    """An operation is outside the Core-owned PermissionEnvelope."""


class DuplicateStart(SafetyError):
    """A durable fence already exists for this Attempt."""


class IdentityMismatch(SafetyError):
    """Immutable Attempt/Manifest/Lane identity is inconsistent."""


class ResourceConflict(SafetyError):
    """An exclusive resource is already durably claimed."""


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
    runtime_identity: RuntimeIdentity | None = None
    result: dict[str, Any] | None = None


@dataclass(frozen=True)
class ArtifactTaskSpec:
    """Internal bounded task shape for a single authorized artifact output."""

    objective: str
    input_name: str
    output_name: str
    begin_marker: str
    end_marker: str


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
            "fences": {},
            "claims": {},
            "events": [],
            "artifacts": {},
            "results": {},
        }
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8"))

    def _save_unlocked(self) -> None:
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

    def _mutate(self, callback: Any) -> Any:
        """Apply one mutation while holding the single-controller file lock."""
        import fcntl

        lock_path = self.path.with_name(f".{self.path.name}.lock")
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a+", encoding="utf-8") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            if self.path.exists():
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            result = callback(self.data)
            self._save_unlocked()
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
            return result

    def put(self, collection: str, key: str, value: dict[str, Any]) -> None:
        def mutate(data: dict[str, Any]) -> None:
            data.setdefault(collection, {})[key] = value

        self._mutate(mutate)

    def event(self, event_type: str, payload: dict[str, Any]) -> None:
        def mutate(data: dict[str, Any]) -> None:
            events = data.setdefault("events", [])
            event = EventEnvelope.create(new_id("evt"), event_type, now(), payload, sequence=len(events) + 1)
            events.append(event.to_record())

        self._mutate(mutate)

    def snapshot(self) -> dict[str, Any]:
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        snapshot = json.loads(json.dumps(self.data))
        snapshot["_ledger_path"] = str(self.path)
        return snapshot

    def validate_attempt_identity(self, attempt_id: str) -> dict[str, Any]:
        data = self.snapshot()
        attempt = data.get("attempts", {}).get(attempt_id)
        if not attempt:
            raise IdentityMismatch(f"unknown Attempt: {attempt_id}")
        manifest = data.get("manifests", {}).get(attempt.get("manifest_id"))
        lane = data.get("lanes", {}).get(attempt.get("runtime_lane_id"))
        if not manifest or manifest.get("attempt_id") != attempt_id:
            raise IdentityMismatch(f"manifest relation mismatch for Attempt: {attempt_id}")
        if manifest.get("task_id") != attempt.get("task_id"):
            raise IdentityMismatch(f"task relation mismatch for Attempt: {attempt_id}")
        if not lane or lane.get("attempt_id") != attempt_id:
            raise IdentityMismatch(f"RuntimeLane relation mismatch for Attempt: {attempt_id}")
        if attempt.get("authority_revision_id") != manifest.get("authority_revision_id"):
            raise IdentityMismatch(f"authority relation mismatch for Attempt: {attempt_id}")
        fence = data.get("fences", {}).get(attempt_id)
        if not fence or fence.get("manifest_id") != manifest.get("manifest_id") or fence.get("runtime_lane_id") != lane.get("runtime_lane_id"):
            raise IdentityMismatch(f"execution fence relation mismatch for Attempt: {attempt_id}")
        return attempt

    def claim_attempt_start(self, attempt_id: str, manifest_id: str, lane_id: str) -> dict[str, Any]:
        def mutate(data: dict[str, Any]) -> dict[str, Any]:
            attempt = data.get("attempts", {}).get(attempt_id)
            if not attempt or attempt.get("manifest_id") != manifest_id or attempt.get("runtime_lane_id") != lane_id:
                raise IdentityMismatch(f"start identity mismatch for Attempt: {attempt_id}")
            if data.setdefault("fences", {}).get(attempt_id):
                raise DuplicateStart(f"durable start fence already exists for Attempt: {attempt_id}")
            fence = {
                "fence_id": new_id("fence"),
                "attempt_id": attempt_id,
                "manifest_id": manifest_id,
                "runtime_lane_id": lane_id,
                "state": "HELD",
                "acquired_at": now(),
            }
            data["fences"][attempt_id] = fence
            events = data.setdefault("events", [])
            event = EventEnvelope.create(
                new_id("evt"),
                "execution.fence_acquired",
                now(),
                {"attempt_id": attempt_id, "fence_id": fence["fence_id"]},
                sequence=len(events) + 1,
            )
            events.append(event.to_record())
            return fence

        return self._mutate(mutate)

    def update_fence(self, attempt_id: str, state: str) -> None:
        def mutate(data: dict[str, Any]) -> None:
            fence = data.setdefault("fences", {}).get(attempt_id)
            if not fence:
                raise IdentityMismatch(f"missing fence for Attempt: {attempt_id}")
            fence["state"] = state
            fence["updated_at"] = now()

        self._mutate(mutate)

    def claim_resource(self, attempt_id: str, manifest_id: str, resource: str) -> dict[str, Any]:
        """Acquire one durable exclusive claim; stale reclaim is fail-closed."""
        def mutate(data: dict[str, Any]) -> dict[str, Any]:
            for claim in data.setdefault("claims", {}).values():
                if claim.get("resource") == resource and claim.get("state") == "HELD":
                    if claim.get("attempt_id") != attempt_id:
                        raise ResourceConflict(f"resource already claimed: {resource}")
                    return claim
            claim = {
                "claim_id": new_id("claim"),
                "attempt_id": attempt_id,
                "manifest_id": manifest_id,
                "resource": resource,
                "exclusive": True,
                "state": "HELD",
                "claimed_at": now(),
            }
            data["claims"][claim["claim_id"]] = claim
            events = data.setdefault("events", [])
            event = EventEnvelope.create(
                new_id("evt"),
                "resource.claimed",
                now(),
                {"resource_claim_id": claim["claim_id"], "attempt_id": attempt_id, "resource": resource},
                sequence=len(events) + 1,
            )
            events.append(event.to_record())
            return claim

        return self._mutate(mutate)

    def release_resource(self, claim_id: str, attempt_id: str) -> None:
        """Release a claim only for its owning Attempt after known termination."""
        def mutate(data: dict[str, Any]) -> None:
            claim = data.setdefault("claims", {}).get(claim_id)
            if not claim or claim.get("attempt_id") != attempt_id:
                raise IdentityMismatch(f"resource claim relation mismatch: {claim_id}")
            if claim.get("state") == "RELEASED":
                return
            if claim.get("state") != "HELD":
                raise SafetyError(f"resource claim is not releasable: {claim_id}")
            claim["state"] = "RELEASED"
            claim["released_at"] = now()
            events = data.setdefault("events", [])
            event = EventEnvelope.create(
                new_id("evt"),
                "resource.released",
                now(),
                {"resource_claim_id": claim_id, "attempt_id": attempt_id, "resource": claim.get("resource")},
                sequence=len(events) + 1,
            )
            events.append(event.to_record())

        self._mutate(mutate)


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

    def __init__(self, adapter: RuntimeAdapter | None = None) -> None:
        if adapter is None:
            # Default composition is kept for the bounded CLI/API convenience,
            # while the Core module itself remains free of a concrete adapter
            # import until this boundary is explicitly used.
            from .runtime import OpenCodeRuntimeAdapter

            adapter = OpenCodeRuntimeAdapter()
        self.adapter = adapter

    @staticmethod
    def _authority(input_name: str = "README.md", output_name: str = "REPORT.md") -> AuthorityRevision:
        return AuthorityRevision(
            authority_revision_id=f"ar_bounded_{digest({'input': input_name, 'output': output_name})[:16]}",
            envelope=PermissionEnvelope(
                read_paths=(input_name,),
                write_paths=(output_name,),
                denied_paths=("../**", "~/.ssh/**", "~/.aws/**", "~/.config/**"),
            ),
            created_at=now(),
        )

    @staticmethod
    def _safe_path(
        workspace: Path,
        relative: str,
        operation: str,
        input_name: str = "README.md",
        output_name: str = "REPORT.md",
    ) -> Path:
        root = workspace.resolve()
        raw = root / relative
        if raw.is_symlink():
            raise AuthorityDenied(f"symlink target denied: {relative}")
        candidate = raw.resolve()
        if candidate.parent != root or candidate == root:
            raise AuthorityDenied(f"{operation} denied outside bounded workspace: {relative}")
        if operation == "read" and relative != input_name:
            raise AuthorityDenied(f"read denied by PermissionEnvelope: {relative}")
        if operation == "write" and relative != output_name:
            raise AuthorityDenied(f"write denied by PermissionEnvelope: {relative}")
        return candidate

    def run_report(self, workspace: Path) -> dict[str, Any]:
        return self.run_artifact_task(
            workspace,
            ArtifactTaskSpec(
                objective="Inspect README and create REPORT.md",
                input_name="README.md",
                output_name="REPORT.md",
                begin_marker="REPORT_CONTENT_BEGIN",
                end_marker="REPORT_CONTENT_END",
            ),
        )

    def run_summary(self, workspace: Path) -> dict[str, Any]:
        return self.run_artifact_task(
            workspace,
            ArtifactTaskSpec(
                objective="Inspect README and create SUMMARY.md",
                input_name="README.md",
                output_name="SUMMARY.md",
                begin_marker="SUMMARY_CONTENT_BEGIN",
                end_marker="SUMMARY_CONTENT_END",
            ),
        )

    def run_artifact_task(self, workspace: Path, spec: ArtifactTaskSpec) -> dict[str, Any]:
        workspace = workspace.resolve()
        if not workspace.is_dir():
            raise SafetyError(f"workspace missing: {workspace}")
        if not spec.input_name or Path(spec.input_name).name != spec.input_name:
            raise SafetyError("input must be one workspace file")
        if not spec.output_name or Path(spec.output_name).name != spec.output_name:
            raise SafetyError("output must be one workspace file")
        if spec.input_name == spec.output_name:
            raise SafetyError("input and output must differ")
        ledger = ExecutionLedger(workspace / "execution-ledger.json")
        request = ExecutionRequest(new_id("req"), spec.objective, str(workspace))
        execution = Execution(new_id("exec"), request.request_id)
        task = Task(new_id("task"), execution.execution_id, request.objective)
        authority = self._authority(spec.input_name, spec.output_name)
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
            workspace_snapshot=digest({"workspace": str(workspace), "read": spec.input_name}),
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
                "runtime_identity": None,
            },
        )
        ledger.event("attempt.created", {"attempt_id": attempt_id, "task_id": task.task_id})
        ledger.event("manifest.created", {"manifest_id": manifest.manifest_id, "immutable": True})
        ledger.claim_attempt_start(attempt_id, manifest.manifest_id, lane.runtime_lane_id)
        resource_claim = ledger.claim_resource(attempt_id, manifest.manifest_id, f"workspace:{workspace}")

        readme_path = self._safe_path(workspace, spec.input_name, "read", spec.input_name, spec.output_name)
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
        preparation = self.adapter.materialize_authority(authority.content_digest)
        authority_evidence = AuthorityEvidence(
            **{
                **asdict(authority_evidence),
                "materialized": True,
                "authority_digest": preparation.authority_digest,
            }
        )
        if authority_evidence.authority_digest != authority.content_digest:
            raise SafetyError("materialized authority digest mismatch")
        ledger.event(
            "authority.materialized",
            {
                "authority_revision_id": authority.authority_revision_id,
                "authority_digest": authority.content_digest,
                "preparation_id": preparation.preparation_id,
                "mode": preparation.mode,
                "substrate_activation_confirmed": False,
            },
        )
        ExecutionBarrier.release(manifest, lane, authority_evidence)
        ledger.put("barriers", attempt_id, {**asdict(authority_evidence), "state": "RELEASED"})
        attempt.status = "RUNNING"
        attempt.barrier = "RELEASED"
        ledger.put("attempts", attempt_id, {**ledger.data["attempts"][attempt_id], "status": attempt.status, "barrier": attempt.barrier})
        ledger.event("execution.barrier_released", {"attempt_id": attempt_id, "mode": authority_evidence.binding_mode})

        prompt = self._prompt(readme, spec)
        runtime: RuntimeExecution = self.adapter.execute(
            prompt,
            workspace,
            preparation,
        )
        if runtime.preparation_id != preparation.preparation_id:
            raise SafetyError("runtime preparation identity mismatch")
        if runtime.authority_config_digest != authority.content_digest:
            raise SafetyError("runtime authority digest mismatch")
        attempt.runtime_session_id = runtime.session_id
        attempt.runtime_identity = runtime.identity
        ledger.event(
            "runtime.fact",
            {
                "attempt_id": attempt_id,
                "runtime_session_id": runtime.session_id,
                "runtime_identity": asdict(runtime.identity),
                "fact": runtime.fact.value,
                "exit_code": runtime.exit_code,
            },
        )
        report = self._extract_report(runtime.text, spec)
        verified = False
        artifact_path: Path | None = None
        verification_reason = "runtime completion is not semantic success"
        if runtime.fact is RuntimeFact.EXITED and runtime.exit_code == 0 and report:
            artifact_path = self._safe_path(workspace, spec.output_name, "write", spec.input_name, spec.output_name)
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
            "runtime_fact": runtime.fact.value,
            "runtime_session_id": runtime.session_id,
            "runtime_identity": asdict(runtime.identity),
            "exit_code": runtime.exit_code,
            "runtime_event_count": runtime.event_count,
            "runtime_text_digest": digest(runtime.text),
            "semantic_success": semantic_success,
            "verification": "PASS" if verified else "FAIL",
            "verification_reason": verification_reason,
            "artifact": spec.output_name if artifact_path else None,
            "authority_binding": "CORE_MEDIATED_NO_RUNTIME_IO",
            "substrate_authority_activation": "NOT_PROVEN",
        }
        ledger.put("results", attempt_id, result)
        ledger.put("tasks", task.task_id, {**asdict(task), "semantic_state": task.semantic_state})
        ledger.put(
            "attempts",
            attempt_id,
            {
                **ledger.data["attempts"][attempt_id],
                "status": attempt.status,
                "runtime_session_id": runtime.session_id,
                "runtime_identity": asdict(runtime.identity),
            },
        )
        ledger.update_fence(attempt_id, "RELEASED" if semantic_success else "QUARANTINED")
        if runtime.fact is RuntimeFact.EXITED:
            ledger.release_resource(resource_claim["claim_id"], attempt_id)
        if artifact_path:
            ledger.put("artifacts", spec.output_name, {"path": spec.output_name, "sha256": sha256_file(artifact_path), "attempt_id": attempt_id})
        ledger.event("verification.completed", {"attempt_id": attempt_id, "result": result["verification"]})
        ledger.event("task.semantic_state", {"task_id": task.task_id, "state": task.semantic_state})
        return {
            "execution_id": execution.execution_id,
            "task_id": task.task_id,
            "attempt_id": attempt_id,
            "manifest_id": manifest.manifest_id,
            "runtime_session_id": runtime.session_id,
            "runtime_identity": asdict(runtime.identity),
            "runtime_fact": runtime.fact.value,
            "semantic_success": semantic_success,
            "verification": result["verification"],
            "artifact": result["artifact"],
            "ledger": str(ledger.path),
            "authority_revision_id": authority.authority_revision_id,
            "authority_digest": authority.content_digest,
            "substrate_authority_activation": "NOT_PROVEN",
        }

    @staticmethod
    def _prompt(readme: str, spec: ArtifactTaskSpec) -> str:
        return (
            "You are a bounded report-writing worker. Do not use tools and do not read or write files. "
            "Using only the README content supplied below, return exactly a concise Markdown report "
            f"between the markers {spec.begin_marker} and {spec.end_marker}. The report must state "
            "the repository/product name, its purpose, and that this report was generated by the "
            "Apex Code safe vertical slice. Do not include any other markers or tool calls.\n\n"
            "README CONTENT:\n---\n"
            + readme
            + "\n---\n"
            + spec.begin_marker
            + "\n"
            + spec.end_marker
        )

    @staticmethod
    def _extract_report(text: str, spec: ArtifactTaskSpec) -> str | None:
        start = spec.begin_marker
        end = spec.end_marker
        if start not in text or end not in text:
            return None
        body = text.split(start, 1)[1].split(end, 1)[0].strip()
        if not body or start in body or end in body:
            return None
        return body + "\n"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
