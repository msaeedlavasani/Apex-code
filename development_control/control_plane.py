"""Durable, executor-neutral development control plane.

The control plane is deliberately separate from ``apex_code``. It schedules
Development Tasks and records development Attempts; it never owns Apex Core
Task/Attempt/Manifest state and never turns evidence absence into proof.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping


class TaskStatus(str, Enum):
    DONE = "DONE"
    BACKLOG = "BACKLOG"
    BLOCKED = "BLOCKED"
    READY = "READY"
    ELIGIBLE = "ELIGIBLE"
    BATCHED = "BATCHED"
    IN_PROGRESS = "IN_PROGRESS"
    VERIFYING = "VERIFYING"
    HUMAN_GATE = "HUMAN_GATE"
    QUARANTINED = "QUARANTINED"
    DEFERRED = "DEFERRED"


class FailureClass(str, Enum):
    TASK_FAILURE = "TASK_FAILURE"
    SYSTEM_FAILURE = "SYSTEM_FAILURE"


EVIDENCE_STATES = {
    "NOT_PROVEN",
    "PROVEN",
    "PARTIAL",
    "NOT_RUN",
    "PASS",
    "FAIL",
}
TERMINAL_TASK_STATUSES = {
    TaskStatus.DONE.value,
    TaskStatus.BLOCKED.value,
    TaskStatus.HUMAN_GATE.value,
    TaskStatus.QUARANTINED.value,
    TaskStatus.DEFERRED.value,
}
BATCH_TERMINAL_OUTCOMES = {"PASS", "FAIL", "RECOVERED", "QUARANTINED"}
PASSPORT_FIELDS = (
    "goal",
    "scope",
    "out_of_scope",
    "dependencies",
    "resource_claims",
    "architecture_constraints",
    "acceptance_criteria",
    "validation",
    "risk",
    "executor_compatibility",
    "human_gates",
)
FORBIDDEN_SECRET_KEYS = {
    "secret",
    "secrets",
    "api_key",
    "apikey",
    "token",
    "password",
    "private_key",
    "authorization",
    "cookie",
    "access_key",
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    _assert_no_secret_material(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _read_json(path: Path, default: Mapping[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return dict(default)
    with path.open(encoding="utf-8") as handle:
        loaded = json.load(handle)
    if not isinstance(loaded, dict):
        raise ValueError(f"control-plane document must be an object: {path}")
    return loaded


def _assert_no_secret_material(value: Any, path: str = "root") -> None:
    """Reject secret-shaped fields before control-plane state is persisted."""
    if isinstance(value, Mapping):
        for key, nested in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in FORBIDDEN_SECRET_KEYS:
                raise ValueError(f"secret-bearing control-plane field is forbidden: {path}.{key}")
            _assert_no_secret_material(nested, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _assert_no_secret_material(nested, f"{path}[{index}]")


def _claims(task: Mapping[str, Any]) -> set[str]:
    values = task.get("resource_claims", [])
    if not isinstance(values, list):
        return set()
    return {str(value) for value in values if isinstance(value, str) and value.strip()}


def _priority(task: Mapping[str, Any]) -> int:
    return {"P0": 1000, "P1": 700, "P2": 400, "P3": 200, "P4": 100}.get(str(task.get("priority", "P3")), 0)


@dataclass(frozen=True)
class BatchSnapshot:
    batch_id: str
    created_at: str
    task_ids: tuple[str, ...]
    concurrency: int
    scores: dict[str, float]
    backlog_revision: int


@dataclass(frozen=True)
class RunSummary:
    run_id: str
    started_at: str
    ended_at: str
    batches: int
    considered_tasks: int
    executed_tasks: int
    verified_tasks: int
    recovered_tasks: int
    incidents: int
    corrective_tasks: int
    backlog_returns: int
    human_gates: tuple[str, ...]
    remaining_eligible: tuple[str, ...]
    stop_reason: str
    critical_path_progress: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "batches": self.batches,
            "considered_tasks": self.considered_tasks,
            "executed_tasks": self.executed_tasks,
            "verified_tasks": self.verified_tasks,
            "recovered_tasks": self.recovered_tasks,
            "incidents": self.incidents,
            "corrective_tasks": self.corrective_tasks,
            "backlog_returns": self.backlog_returns,
            "human_gates": list(self.human_gates),
            "remaining_eligible": list(self.remaining_eligible),
            "stop_reason": self.stop_reason,
            "critical_path_progress": self.critical_path_progress,
        }


class ControlPlaneStore:
    """Durable files for one canonical backlog and its operational history."""

    def __init__(self, backlog_path: Path, passports_dir: Path, state_path: Path) -> None:
        self.backlog_path = Path(backlog_path)
        self.passports_dir = Path(passports_dir)
        self.state_path = Path(state_path)

    def load_backlog(self) -> dict[str, Any]:
        document = _read_json(self.backlog_path, {"schema_version": 1, "revision": 0, "tasks": []})
        tasks = document.get("tasks")
        if not isinstance(tasks, list):
            raise ValueError("backlog tasks must be a list")
        return document

    def save_backlog(self, document: Mapping[str, Any]) -> None:
        _write_json(self.backlog_path, dict(document))

    def load_state(self) -> dict[str, Any]:
        return _read_json(
            self.state_path,
            {
                "schema_version": 1,
                "attempts": [],
                "batches": [],
                "incidents": [],
                "owner_decisions": [],
                "run_summaries": [],
            },
        )

    def save_state(self, state: Mapping[str, Any]) -> None:
        _write_json(self.state_path, dict(state))

    def load_passport(self, task_id: str) -> dict[str, Any]:
        return _read_json(self.passports_dir / f"{task_id}.json", {})

    def save_passport(self, task_id: str, passport: Mapping[str, Any]) -> None:
        _write_json(self.passports_dir / f"{task_id}.json", dict(passport))


class DevelopmentControlPlane:
    """Backlog admission, immutable batching, failure handling, and run loop."""

    def __init__(self, store: ControlPlaneStore, executor_id: str = "generic-executor") -> None:
        self.store = store
        self.executor_id = executor_id

    def _documents(self) -> tuple[dict[str, Any], dict[str, Any]]:
        return self.store.load_backlog(), self.store.load_state()

    @staticmethod
    def _task_map(backlog: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
        return {str(task["task_id"]): task for task in backlog.get("tasks", []) if isinstance(task, dict) and task.get("task_id")}

    def passport_complete(self, task_id: str) -> tuple[bool, list[str]]:
        passport = self.store.load_passport(task_id)
        missing = []
        for field in PASSPORT_FIELDS:
            value = passport.get(field)
            if value is None or value == "" or (not value and field not in {"dependencies", "resource_claims", "human_gates"}):
                missing.append(field)
        return not missing, missing

    def _dependency_reasons(self, task: Mapping[str, Any], tasks: Mapping[str, Mapping[str, Any]]) -> list[str]:
        reasons: list[str] = []
        for dependency in task.get("dependencies", []):
            dependency_id = dependency if isinstance(dependency, str) else dependency.get("task_id") if isinstance(dependency, dict) else None
            if not dependency_id:
                reasons.append("DEPENDENCY_REFERENCE_INVALID")
                continue
            prerequisite = tasks.get(str(dependency_id))
            if prerequisite is None:
                reasons.append(f"DEPENDENCY_MISSING:{dependency_id}")
                continue
            if prerequisite.get("status") not in {TaskStatus.DONE.value, "VERIFIED"} or (
                prerequisite.get("status") == TaskStatus.DONE.value
                and prerequisite.get("verification_status") != "VERIFIED"
            ):
                reasons.append(f"DEPENDENCY_NOT_VERIFIED:{dependency_id}")
        return reasons

    def _policy_reasons(self, task: Mapping[str, Any]) -> list[str]:
        reasons: list[str] = []
        if not task.get("autonomous_allowed", False):
            reasons.append("AUTONOMOUS_POLICY_DISALLOWS")
        if str(task.get("risk", "LOW")) == "CRITICAL":
            reasons.append("CRITICAL_RISK_HUMAN_GATE")
        if str(task.get("decision_class", "ROUTINE")) != "ROUTINE":
            reasons.append("NON_ROUTINE_DECISION_CLASS")
        compatibility = task.get("executor_compatibility", {})
        if isinstance(compatibility, dict):
            required = compatibility.get("executors", [])
            if required and self.executor_id not in required and "*" not in required:
                reasons.append("EXECUTOR_INCOMPATIBLE")
        return reasons

    def readiness(self, task_id: str) -> dict[str, Any]:
        backlog = self.store.load_backlog()
        tasks = self._task_map(backlog)
        task = tasks.get(task_id)
        if task is None:
            raise KeyError(task_id)
        complete, missing = self.passport_complete(task_id)
        reasons = [] if complete else [f"PASSPORT_MISSING:{field}" for field in missing]
        reasons.extend(self._dependency_reasons(task, tasks))
        gates = task.get("human_gates", [])
        if gates:
            reasons.append("HUMAN_GATE_OPEN")
        if task.get("blockers"):
            reasons.append("EXTERNAL_BLOCKER")
        reasons.extend(self._policy_reasons(task))
        return {
            "task_id": task_id,
            "ready": not reasons,
            "eligible": not reasons and task.get("status") in {TaskStatus.BACKLOG.value, TaskStatus.READY.value, TaskStatus.ELIGIBLE.value},
            "reasons": reasons,
        }

    def refresh_readiness(self) -> list[dict[str, Any]]:
        backlog = self.store.load_backlog()
        tasks = self._task_map(backlog)
        eligible: list[dict[str, Any]] = []
        for task in backlog["tasks"]:
            task_id = str(task.get("task_id"))
            if task.get("status") in {
                TaskStatus.DONE.value,
                TaskStatus.IN_PROGRESS.value,
                TaskStatus.VERIFYING.value,
                TaskStatus.BATCHED.value,
                TaskStatus.DEFERRED.value,
                TaskStatus.QUARANTINED.value,
            }:
                continue
            result = self.readiness(task_id)
            task["readiness_reasons"] = result["reasons"]
            if result["ready"]:
                task["status"] = TaskStatus.ELIGIBLE.value
                eligible.append(task)
            elif "HUMAN_GATE_OPEN" in result["reasons"]:
                task["status"] = TaskStatus.HUMAN_GATE.value
            elif any(reason.startswith("DEPENDENCY_") for reason in result["reasons"]) or "EXTERNAL_BLOCKER" in result["reasons"]:
                task["status"] = TaskStatus.BLOCKED.value
            elif task.get("status") not in {TaskStatus.DEFERRED.value, TaskStatus.QUARANTINED.value}:
                task["status"] = TaskStatus.BACKLOG.value
        backlog["revision"] = int(backlog.get("revision", 0)) + 1
        self.store.save_backlog(backlog)
        return eligible

    def _score(self, task: Mapping[str, Any]) -> float:
        age = float(task.get("aging_days", 0))
        critical_path = float(task.get("critical_path_weight", 0))
        unlock = float(task.get("downstream_unlock_value", 0))
        risk_penalty = {"LOW": 0, "MEDIUM": 10, "HIGH": 35, "CRITICAL": 1000}.get(str(task.get("risk", "LOW")), 20)
        return _priority(task) + critical_path * 10 + unlock * 5 + min(age, 365) - risk_penalty

    def select_batch(self, concurrency: int = 1) -> BatchSnapshot | None:
        if concurrency < 1:
            raise ValueError("concurrency must be positive")
        self.refresh_readiness()
        backlog, state = self._documents()
        candidates = [task for task in backlog["tasks"] if task.get("status") == TaskStatus.ELIGIBLE.value]
        candidates.sort(key=lambda task: (-self._score(task), str(task["task_id"])))
        selected: list[dict[str, Any]] = []
        claimed: set[str] = set()
        for task in candidates:
            task_claims = _claims(task)
            if task_claims & claimed:
                continue
            selected.append(task)
            claimed.update(task_claims)
            if len(selected) >= concurrency:
                break
        if not selected:
            return None
        snapshot = BatchSnapshot(
            batch_id=_id("batch"),
            created_at=_now(),
            task_ids=tuple(str(task["task_id"]) for task in selected),
            concurrency=concurrency,
            scores={str(task["task_id"]): self._score(task) for task in selected},
            backlog_revision=int(backlog.get("revision", 0)),
        )
        for task in selected:
            task["status"] = TaskStatus.BATCHED.value
            task["batch_id"] = snapshot.batch_id
        backlog["revision"] = int(backlog.get("revision", 0)) + 1
        state.setdefault("batches", []).append(
            {
                "batch_id": snapshot.batch_id,
                "created_at": snapshot.created_at,
                "task_ids": list(snapshot.task_ids),
                "concurrency": snapshot.concurrency,
                "scores": snapshot.scores,
                "backlog_revision": snapshot.backlog_revision,
                "status": "OPEN",
                "integration_verification": "NOT_RUN",
            }
        )
        self.store.save_backlog(backlog)
        self.store.save_state(state)
        return snapshot

    def record_attempt(self, task_id: str, batch_id: str, outcome: Mapping[str, Any]) -> str:
        backlog, state = self._documents()
        tasks = self._task_map(backlog)
        if task_id not in tasks:
            raise KeyError(task_id)
        attempt_id = _id("dev_attempt")
        state.setdefault("attempts", []).append(
            {
                "attempt_id": attempt_id,
                "task_id": task_id,
                "batch_id": batch_id,
                "executor": self.executor_id,
                "created_at": _now(),
                "outcome": dict(outcome),
            }
        )
        self.store.save_state(state)
        return attempt_id

    def _record_batch_outcome(self, batch_id: str, task_id: str, outcome: Mapping[str, Any]) -> None:
        state = self.store.load_state()
        batch = next(item for item in state.get("batches", []) if item.get("batch_id") == batch_id)
        batch.setdefault("task_outcomes", {})[task_id] = dict(outcome)
        self.store.save_state(state)

    def _incident(self, task_id: str, failure_class: FailureClass, signature: str, evidence: Mapping[str, Any]) -> dict[str, Any]:
        _, state = self._documents()
        fingerprint = hashlib.sha256(f"{failure_class.value}:{signature}".encode("utf-8")).hexdigest()[:20]
        incidents = state.setdefault("incidents", [])
        incident = next((item for item in incidents if item.get("fingerprint") == fingerprint), None)
        if incident is None:
            incident = {
                "incident_id": _id("incident"),
                "fingerprint": fingerprint,
                "classification": failure_class.value,
                "status": "OPEN",
                "affected_task_ids": [],
                "evidence": [],
                "occurrences": 0,
                "systemic": False,
                "resolution": None,
                "corrective_task_ids": [],
            }
            incidents.append(incident)
        if task_id not in incident["affected_task_ids"]:
            incident["affected_task_ids"].append(task_id)
        incident["evidence"].append({"at": _now(), "task_id": task_id, **dict(evidence)})
        incident["occurrences"] += 1
        incident["systemic"] = failure_class == FailureClass.SYSTEM_FAILURE or incident["occurrences"] >= 3
        self.store.save_state(state)
        return incident

    def fail_task(
        self,
        task_id: str,
        batch_id: str,
        failure_class: FailureClass,
        signature: str,
        evidence: Mapping[str, Any],
        max_rework: int = 2,
    ) -> dict[str, Any]:
        backlog, _ = self._documents()
        tasks = self._task_map(backlog)
        task = tasks[task_id]
        attempt_id = self.record_attempt(task_id, batch_id, {"status": "FAIL", "failure_class": failure_class.value})
        incident = self._incident(task_id, failure_class, signature, evidence)
        task["rework_count"] = int(task.get("rework_count", 0)) + 1
        task["last_failure_class"] = failure_class.value
        task["last_attempt_id"] = attempt_id
        task["incident_id"] = incident["incident_id"]
        if task["rework_count"] > max_rework or incident.get("systemic"):
            task["status"] = TaskStatus.QUARANTINED.value
        else:
            task["status"] = TaskStatus.BACKLOG.value
        self.store.save_backlog(backlog)
        self._record_batch_outcome(
            batch_id,
            task_id,
            {"status": "QUARANTINED" if task["status"] == TaskStatus.QUARANTINED.value else "FAIL", "failure_class": failure_class.value},
        )
        return {"attempt_id": attempt_id, "incident_id": incident["incident_id"], "status": task["status"]}

    def complete_task(self, task_id: str, batch_id: str, outcome: Mapping[str, Any]) -> str:
        backlog, _ = self._documents()
        tasks = self._task_map(backlog)
        task = tasks[task_id]
        attempt_id = self.record_attempt(task_id, batch_id, {"status": "PASS", **dict(outcome)})
        task["status"] = TaskStatus.DONE.value
        task["verification_status"] = "VERIFIED"
        task["last_attempt_id"] = attempt_id
        task["evidence_status"] = str(outcome.get("evidence_status", "PROVEN"))
        self.store.save_backlog(backlog)
        self._record_batch_outcome(batch_id, task_id, {"status": "PASS", **dict(outcome)})
        return attempt_id

    def queue_owner_decision(self, task_id: str, gate: str, evidence_refs: Iterable[str]) -> str:
        _, state = self._documents()
        decision_id = _id("decision")
        state.setdefault("owner_decisions", []).append(
            {
                "decision_id": decision_id,
                "task_id": task_id,
                "gate": gate,
                "evidence_refs": list(evidence_refs),
                "status": "OPEN",
                "created_at": _now(),
            }
        )
        self.store.save_state(state)
        return decision_id

    def open_human_gates(self) -> list[dict[str, Any]]:
        _, state = self._documents()
        return [item for item in state.get("owner_decisions", []) if item.get("status") == "OPEN"]

    def verify_batch(self, batch_id: str, integration_verification: str = "NOT_RUN") -> dict[str, Any]:
        backlog, state = self._documents()
        batch = next(item for item in state.get("batches", []) if item.get("batch_id") == batch_id)
        tasks = self._task_map(backlog)
        recorded_outcomes = batch.get("task_outcomes", {})
        outcomes = {
            task_id: recorded_outcomes.get(task_id, {}).get("status", tasks[task_id].get("status"))
            for task_id in batch["task_ids"]
            if task_id in tasks
        }
        dangling = [task_id for task_id in batch["task_ids"] if task_id not in tasks]
        unresolved = [
            task_id
            for task_id, status in outcomes.items()
            if status not in TERMINAL_TASK_STATUSES and status not in BATCH_TERMINAL_OUTCOMES
        ]
        requires_integration = any(tasks[task_id].get("requires_integration_verification") for task_id in outcomes)
        if requires_integration and integration_verification not in {"PASS", "FAIL"}:
            unresolved.append("INTEGRATION_VERIFICATION")
        batch["integration_verification"] = integration_verification
        batch["outcomes"] = outcomes
        batch["dangling_task_ids"] = dangling
        if not unresolved and not dangling:
            batch["status"] = "COMPLETED_WITH_OUTCOMES"
            batch["completed_at"] = _now()
            self.store.save_state(state)
            if integration_verification == "FAIL":
                self._incident(
                    "BATCH:" + batch_id,
                    FailureClass.SYSTEM_FAILURE,
                    "batch-integration-verification",
                    {"batch_id": batch_id, "validation": "FAIL"},
                )
        else:
            batch["status"] = "OPEN"
            self.store.save_state(state)
        return {"batch_id": batch_id, "closed": batch["status"] != "OPEN", "unresolved": unresolved, "dangling": dangling, "outcomes": outcomes}

    def recover_task(self, task_id: str, batch_id: str, evidence: Mapping[str, Any]) -> str:
        """Record a bounded recovery as a distinct development Attempt."""
        backlog, _ = self._documents()
        task = self._task_map(backlog)[task_id]
        attempt_id = self.record_attempt(task_id, batch_id, {"status": "RECOVERED", **dict(evidence)})
        task["status"] = TaskStatus.BACKLOG.value
        task["recovery_count"] = int(task.get("recovery_count", 0)) + 1
        task["last_attempt_id"] = attempt_id
        self.store.save_backlog(backlog)
        return attempt_id

    def generate_corrective_task(
        self,
        incident_id: str,
        task_id: str,
        title: str,
        passport: Mapping[str, Any],
    ) -> str:
        """Create a linked, durable corrective Development Task."""
        backlog, state = self._documents()
        new_task_id = str(passport.get("development_task_id") or _id("AC-CORRECTIVE"))
        if any(item.get("task_id") == new_task_id for item in backlog.get("tasks", [])):
            raise ValueError(f"task already exists: {new_task_id}")
        task = {
            "task_id": new_task_id,
            "title": title,
            "status": TaskStatus.BACKLOG.value,
            "verification_status": "NOT_RUN",
            "evidence_status": "NOT_PROVEN",
            "priority": "P1",
            "risk": "MEDIUM",
            "decision_class": "ROUTINE",
            "autonomous_allowed": True,
            "executor_compatibility": {"executors": ["*"]},
            "dependencies": [task_id],
            "resource_claims": [],
            "requires_integration_verification": False,
            "incident_id": incident_id,
            "downstream_unlock_value": 0,
            "critical_path_weight": 0,
            "aging_days": 0,
        }
        backlog.setdefault("tasks", []).append(task)
        backlog["revision"] = int(backlog.get("revision", 0)) + 1
        state_incident = next(item for item in state.get("incidents", []) if item.get("incident_id") == incident_id)
        state_incident.setdefault("corrective_task_ids", []).append(new_task_id)
        self.store.save_backlog(backlog)
        self.store.save_passport(new_task_id, passport)
        self.store.save_state(state)
        return new_task_id

    def systemic_circuit_breaker_open(self) -> bool:
        return any(item.get("systemic") for item in self.store.load_state().get("incidents", []))

    def run(
        self,
        executor: Callable[[Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any]],
        concurrency: int = 1,
        max_batches: int | None = None,
    ) -> RunSummary:
        started = _now()
        run_id = _id("run")
        batches = considered = executed = verified = recovered = incidents = corrective = backlog_returns = 0
        while max_batches is None or batches < max_batches:
            if self.systemic_circuit_breaker_open():
                break
            snapshot = self.select_batch(concurrency)
            if snapshot is None:
                break
            batches += 1
            considered += len(snapshot.task_ids)
            backlog = self.store.load_backlog()
            tasks = self._task_map(backlog)
            for task_id in snapshot.task_ids:
                task = tasks[task_id]
                task["status"] = TaskStatus.IN_PROGRESS.value
                self.store.save_backlog(backlog)
                outcome = dict(executor(dict(task), self.store.load_passport(task_id)))
                executed += 1
                if outcome.get("status") in {"PASS", "DONE", "VERIFIED"}:
                    task["status"] = TaskStatus.VERIFYING.value
                    self.store.save_backlog(backlog)
                    self.complete_task(task_id, snapshot.batch_id, outcome)
                    verified += 1
                else:
                    failure_class = FailureClass(str(outcome.get("failure_class", FailureClass.TASK_FAILURE.value)))
                    result = self.fail_task(
                        task_id,
                        snapshot.batch_id,
                        failure_class,
                        str(outcome.get("signature", "unspecified-failure")),
                        {"validation": outcome.get("validation", "NOT_RUN")},
                    )
                    incidents += 1
                    if result["status"] == TaskStatus.BACKLOG.value:
                        backlog_returns += 1
            verification = self.verify_batch(snapshot.batch_id, "PASS")
            if not verification["closed"]:
                break
        remaining = self.refresh_readiness()
        open_gates = self.open_human_gates()
        if any(item.get("systemic") for item in self.store.load_state().get("incidents", [])):
            stop_reason = "SYSTEMIC_CIRCUIT_BREAKER"
        elif remaining:
            stop_reason = "AUTONOMOUS_WORK_REMAINS" if max_batches is not None and batches >= max_batches else "NO_SAFE_BATCH"
        elif open_gates:
            stop_reason = "HUMAN_GATES_ONLY"
        else:
            stop_reason = "NO_ELIGIBLE_WORK"
        summary = RunSummary(
            run_id=run_id,
            started_at=started,
            ended_at=_now(),
            batches=batches,
            considered_tasks=considered,
            executed_tasks=executed,
            verified_tasks=verified,
            recovered_tasks=recovered,
            incidents=incidents,
            corrective_tasks=corrective,
            backlog_returns=backlog_returns,
            human_gates=tuple(item["task_id"] for item in open_gates),
            remaining_eligible=tuple(str(task["task_id"]) for task in remaining),
            stop_reason=stop_reason,
            critical_path_progress=self.critical_path_progress(),
        )
        state = self.store.load_state()
        state.setdefault("run_summaries", []).append(summary.as_dict())
        self.store.save_state(state)
        return summary

    def critical_path_progress(self) -> dict[str, Any]:
        backlog = self.store.load_backlog()
        tasks = [task for task in backlog.get("tasks", []) if isinstance(task, dict)]
        total = len(tasks)
        done = sum(task.get("status") == TaskStatus.DONE.value for task in tasks)
        return {"done": done, "total": total, "ratio": done / total if total else 1.0}
