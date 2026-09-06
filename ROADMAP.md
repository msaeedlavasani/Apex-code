# Apex Code Roadmap

Status: **PROPOSED** as a directional product/system evolution record.

`ROADMAP.md` describes evolution and direction. It is not the active backlog,
Work Registry, Task Passport collection, sprint board, implementation checklist,
or execution authority. A future item authorizes no work without an active
Development Task and accepted scope.

## Past — evidence-backed evolution

### Product exploration

- OpenWork feasibility was audited and a thin-fork direction was recommended:
  [OpenWork feasibility](docs/evidence/OPENWORK-FEASIBILITY.md).
- OpenCode was established as the first runtime substrate direction, not the
  product identity; the architecture baseline records the boundary.

### Architecture foundation

- Product identity and principles: [vision and principles](docs/architecture/00-PRODUCT-VISION-AND-PRINCIPLES.md).
- Modular boundaries: [modular product architecture](docs/architecture/01-MODULAR-PRODUCT-ARCHITECTURE-v1.md).
- Execution data, lifecycle, and API: [data model](docs/architecture/02-EXECUTION-DATA-MODEL-v1.md),
  [execution model](docs/architecture/03-EXECUTION-MODEL-v1.md), and
  [execution API](docs/architecture/04-EXECUTION-API-v1.md).
- Authority and maturity limits remain recorded in [architecture status](docs/architecture/05-ARCHITECTURE-STATUS.md)
  and [open questions](docs/evidence/OPEN-QUESTIONS.md).

### Repository and development-control foundation

- Main normalization, protected-branch PR governance, and lean CI were merged
  in PR #1.
- DPT, Home Fit, and BaziGB development-control patterns were harvested in
  [the pattern harvest](docs/evidence/DEVELOPMENT-CONTROL-PATTERN-HARVEST.md).
- The DCS design, gap analysis, and Owner acceptance AC-ODS-0001 were merged
  in PR #2; see [the accepted decision record](docs/adr/0001-ac-ods-0001-development-control-system.md).

## Present — canonical development foundation

The current maturity frontier is canonical documentation materialization:
product definition, system design, terminology, Context Map, development
system, testing strategy, security model, agent contract, and this Roadmap.
This milestone is the subject of the current AC-MASTER-DOCS change and is not
marked complete until reviewed, merged, and validated.

## Future — directional evolution

### Agentic Creation Ecosystem

The long-term product direction is an **Agentic Creation Ecosystem**:

> Apex Code is not just where agents write code. It is where ideas take shape, evolve, and come to life.

The product philosophy is **Expansive by ambition. Disciplined by sequence.**
The ambition is broad creation and software-development support, governed by
evolution discipline rather than artificial scope limitation: build each thing
when the system is ready for it.

A possible future lifecycle is:

```text
Idea → Explore → Research → Shape → Challenge → Design → Plan → Build
     → Verify → Release → Observe → Learn → Evolve ↺
```

Possible future coverage includes Research, Product Discovery, Design,
Architecture, Development, Testing, Security, Deployment, Operations,
Analytics, Knowledge, Teamwork, and Agent Workforce. These are exploration
domains, not a committed module list, package structure, entitlement plan, or
implementation sequence.

### Supervised Autonomous Workforce direction

Apex may eventually evolve toward a supervised autonomous workforce model in
which persistent supervisory control can understand missions, decompose work,
coordinate dependencies, delegate to multiple agents, observe progress, verify
results, recover from failures, reassign work, and escalate genuine human
gates. Candidate concepts include Foreman/supervisory orchestration, Mission
Control, Autonomous Workforce, Human Gate visualization, and task/dependency or
failure/recovery views. These names and concepts are exploratory and are not
frozen.

Any future workforce capability must remain above and governed by Apex Core,
authority, execution, and development-control boundaries. DPT remains optional;
Orchestration remains optional and independent from DPT.

### Spatial and persistent experience direction

A future visual or spatial interface may project canonical Apex state into a
graphical operational model: work domains, agent assignment or handoff,
dependencies, active/failed/blocked states, Human Gate prompts, and
recovery/reassignment visibility. The visual world would be a projection of
Apex state, never the authoritative owner of that state.

Apex may also reduce context switching by preserving continuity across project
state, decisions, tasks, evidence, agents, and next actions. The intended
experience should help answer: “What is happening now? What is next? Where is
the human needed?” This remains product-experience direction, not an
implementation requirement.

The following sequence is directional, not frozen phase numbering:

```text
Runtime Adapter Contract
        ↓
Core Safe Execution
        ↓
OpenCode Adapter
        ↓
First Safe Execution Vertical Slice
        ↓
Product Shell Integration
        ↓
Execution / Verification / Recovery Hardening
        ↓
Orchestration Capability
        ↓
Advanced Routing
        ↓
DPT Capability
        ↓
Commercial / Enterprise Maturity
```

Future entries require reconciliation with architecture status and evidence.
They do not authorize Runtime Adapter, Orchestration, DPT, or product work.
