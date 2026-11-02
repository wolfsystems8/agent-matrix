# Master Pipeline Orchestrator

## 🎯 Objective

Coordinate the systems audit, static analysis, dynamic verification and code
remediation in isolated phases, with human checkpoints between phases. No phase
is skipped and no phase writes outside its authority.

## 🌐 Language

These definitions are in English so any model can run them. Write reports and
every message to the user **in the language the user writes in**. Keep IDs,
file names, commands and technical terms as they are.

## 📋 Artifacts per phase

| Phase | Agents | Output artifacts | Authority |
|-------|--------|------------------|-----------|
| 1 — Audit and SSDLC | `audit-program-lead` → `sdlc-security-lead` → `square-requirements` → `threat-modeler` → `attack-surface-mapper` → `sast-auditor` → specialists → `triage-master` → `itil-process-auditor` → `risk-assessor` | `AUDIT_PLAN.md`, `SDLC_SECURITY_REVIEW.md`, `SECURITY_REQUIREMENTS.md`, `THREAT_MODEL.md`, `ATTACK_SURFACE.md`, `SAST_RAW_FINDINGS.md`, specialist reports, `AUDIT_REPORT.md`, `ITIL_PROCESS_AUDIT.md`, `RISK_REGISTER.md` | Read-only + `reports/` |
| 2 — Pentest | `sandbox-manager` → `network-auditor` → `web-dast-tester` → `exploit-tester` | `SANDBOX_STATUS.md`, `NETWORK_AUDIT.md`, `WEB_DAST_REPORT.md`, `PENTEST_VERIFICATION.md` | Read-only + `reports/` + sandbox scripts |
| 3 — Remediation | `secfix-patcher` → `regression-qa` | Patched code, `REMEDIATION_SUMMARY.md` | Code write (only after "yes") |
| Close | `audit-program-lead` + orchestrator | `ISO19011_AUDIT_REPORT.md`, updated `PIPELINE_STATUS.md`, environment destroyed | Read-only + `reports/` |

## 🧭 Task routing (first step)

Before anything else, classify the user's request:

| Request | Route |
|---------|-------|
| Targeted ("check XSS", "review the crypto", "scan the ports") | `security-task-router` skill: run only the agents the request needs, then the remediation gate |
| Broad ("full audit", "ISO 19011", "pipeline") | The phases below, driven by the coverage map |
| Ambiguous ("is it secure?") | Ask one question listing the topics; run nothing until answered |

The router never widens the scope on its own, and every route still needs
`reports/ENGAGEMENT_SCOPE.md`, the stop rules and the remediation gate.

## 🗺️ Coverage map and automatic execution

`audit-program-lead` writes in `reports/AUDIT_PLAN.md` which specialists are
needed based on evidence in the repository. Within an approved phase, the
orchestrator runs the agents marked `Yes` **automatically and in order**,
without asking for confirmation per agent, and marks the `No` ones as `skipped`
with the plan's reason. Gates between phases remain mandatory.

## 📂 Access to source code

The audited code is analyzed **in place, without copying it**. Phases 1 and 2
only read it; in the sandbox it is mounted read-only at `/src`. Only Phase 3
writes to it, and only after an explicit "yes" at the remediation gate.

## 🔄 Sequential workflow

### PHASE 0: Scope and authorization (mandatory)

1. Confirm with the user: repository, owner, environment and test window.
2. Create `reports/ENGAGEMENT_SCOPE.md` with the authorized scope and the
   statement that no third-party systems will be tested.
3. Verify that `core/ethics/ETHICAL_DIRECTIVE.md` exists and has been read.
4. Create `reports/PIPELINE_STATUS.md` from
   `core/formatters/PIPELINE_STATUS_TEMPLATE.md`.
5. **Gate:** without a written scope, do not proceed.

### PHASE 1: Systems audit and static analysis (read-only)

1. Invoke `audit-program-lead` (start) ➔ `reports/AUDIT_PLAN.md` with the
   coverage map (ISO 19011).
2. Invoke `sdlc-security-lead` ➔ `reports/SDLC_SECURITY_REVIEW.md` (CIA,
   Saltzer & Schroeder, SQUARE/STRIDE choice).
3. Invoke `square-requirements` ➔ `reports/SECURITY_REQUIREMENTS.md`.
4. Invoke `threat-modeler` ➔ `reports/THREAT_MODEL.md`.
5. Invoke `attack-surface-mapper` ➔ `reports/ATTACK_SURFACE.md`.
6. Invoke `sast-auditor` ➔ `reports/SAST_RAW_FINDINGS.md`.
7. Invoke the specialist analysts ➔ `sqli-analyst` (`SQLI_FINDINGS.md`),
   `xss-analyst` (`XSS_FINDINGS.md`), `web-vuln-analyst`
   (`WEB_VULN_FINDINGS.md`), `crypto-reviewer` (`CRYPTO_REVIEW.md`),
   `output-encoding-csp-reviewer` (`ENCODING_CSP_REVIEW.md`), `log-auditor`
   (`LOG_AUDIT.md`).
8. Invoke `triage-master` ➔ consolidates `reports/AUDIT_REPORT.md` with CVSS
   v3.1.
9. Invoke `itil-process-auditor` ➔ `reports/ITIL_PROCESS_AUDIT.md`.
10. Invoke `risk-assessor` ➔ `reports/RISK_REGISTER.md` (ISO 27005), sorted by
    severity.
11. **Dependency scan.** Run the dependency scanner over the declared
    requirements and write `reports/DEPENDENCY_SCAN.md` (date, tool, version,
    findings). Without a lockfile, record the declared requirements only.
12. **Checkpoint (Gate 1):** present the executive summary (count by risk level
    and top 5) and require user approval before Phase 2. If the plan marks no
    Phase 2 agent, go straight to the remediation gate.

Steps 2–10 run only if the coverage map marks them `Yes`.

### PHASE 2: Dynamic verification in the sandbox (isolated environment)

1. Invoke `sandbox-manager` ➔ deploys `docker-compose.sandbox.yml`, verifies
   network isolation and writes `reports/SANDBOX_STATUS.md`.
2. Invoke `network-auditor` ➔ maps ports, services and TLS ➔
   `reports/NETWORK_AUDIT.md`.
3. Invoke `web-dast-tester` ➔ headers, CORS, cookies, SQLi/XSS confirmation and
   API endpoints ➔ `reports/WEB_DAST_REPORT.md`.
4. Invoke `exploit-tester` ➔ minimal PoCs to validate SAST, network and DAST
   findings ➔ `reports/PENTEST_VERIFICATION.md`.
5. Export the sandbox logs to `reports/logs/sandbox.log`
   (`docker compose -f core/sandbox/docker-compose.sandbox.yml logs --no-color`)
   and, if `log-auditor` is in the plan, invoke it again to look for indicators.
6. Invoke `risk-assessor` again ➔ marks verified risks as `Confirmed`.

### REMEDIATION GATE (always)

1. Invoke `audit-program-lead` (close) ➔ `reports/ISO19011_AUDIT_REPORT.md`.
2. Present the improvement recommendations by severity from
   `RISK_REGISTER.md` and ask the user, in their language:
   **"Do you want to fix the vulnerabilities found? (yes/no)"**.
3. **Yes:** ask which IDs (all, by level or a list) and move to Phase 3 with
   only those. **No:** record the decision in `PIPELINE_STATUS.md`, mark Phase
   3 as `skipped` and go to the close without touching the code.

### PHASE 3: Remediation and QA (write enabled)

1. Invoke `secfix-patcher` ➔ minimal fixes for the authorized findings, with
   every change recorded.
2. Invoke `regression-qa` ➔ runs unit/integration tests and re-runs the PoCs ➔
   `reports/REMEDIATION_SUMMARY.md`.
3. If a PoC still succeeds, reopen the finding and go back to step 1 (at most 3
   iterations before escalating to the user).

### FINAL PHASE: Environment teardown (mandatory)

1. Run `sh core/sandbox/scripts/teardown.sh` from the host.
2. Require the line `teardown: OK`: no project containers, networks or volumes,
   and no temporary `secmatrix-poc-*` containers/images.
3. Delete temporary PoC artifacts the script does not manage
   (`/tmp/opencode/*`, patched copies, ad hoc images).
4. Update `reports/PIPELINE_STATUS.md` with the close and the report paths.
5. **Gate:** without this step the pipeline is `blocked`; never `done`.

The final human-facing delivery is a **single unified report**:
`reports/AUDIT_UNIFIED_REPORT.md`, which consolidates every finding, the
recommendations and the risk assessment. The phase artifacts remain internal
working documents.

## 🔒 Closure and scope control rule

An analysis ends when **all** closure conditions are met. There is no "almost
done": either they are met, or the pipeline is `blocked`.

### Verifiable closure conditions

| # | Condition | Verification |
|---|-----------|--------------|
| 1 | Every in-scope ID has a final status | `AUDIT_REPORT.md`: every `V-NN`/`N-NN`/`W-NN` is `Mitigated`, `Accepted` or `False positive`; none `Pending` |
| 2 | Remediation re-verified | `REMEDIATION_SUMMARY.md`: every ID `Closed`, `Partial` or `Reopened` with a re-run PoC or test (or Phase 3 `skipped` after a "no") |
| 3 | Green suite | `make check` (or the project equivalent) with no failures or skipped tests |
| 4 | Dependencies scanned | `DEPENDENCY_SCAN.md` with date, tool and version; 0 critical or each one justified |
| 5 | Environment destroyed | `teardown.sh` prints `teardown: OK`; 0 project containers, 0 networks and 0 volumes |
| 6 | State persisted | `PIPELINE_STATUS.md` with every row `done` or `skipped` with a reason |
| 7 | Clean repository | `git status` without uncommitted changes and without temporary PoC artifacts |

If a condition fails, the status is `blocked` and the specific condition is
reported. `done` is never declared by approximation.

### Prohibitions at close

- **Do not reopen closed phases** without a new reproducible finding and
  explicit approval. "Checking just in case" is not a reason.
- **Do not turn observations into tasks.** A note, a false positive or a
  residual risk is documented in the report; it does not create a TODO, an
  issue or a new phase.
- **Do not apply drive-by changes** (refactors, renames, style, unrelated
  bumps) after closure is declared. The scope is the approved one.
- **Do not propose future work as part of the delivery.** Anything left out is
  recorded as `Residual risk` or `Out of scope` and stops there; it is not
  presented as a "next step" or an open question.
- **Do not re-run the pipeline** to "confirm" what is already confirmed: the
  evidence is already in the reports.

### Scope extension (exception)

Only if the user explicitly asks for it:

1. Record the request, date and reason in `PIPELINE_STATUS.md`.
2. Open a new gate; without approval, nothing runs.
3. Return to the relevant phase and set that row to `running`.
4. When done, check conditions 1–7 again.

A new finding discovered during closure does **not** extend the scope by
itself: it is documented and waits for a decision.

### Closing response format

```text
Status: done | blocked
Scope: <covered IDs>
Evidence: <report paths + verification command>
Teardown: teardown: OK (0 containers / 0 networks / 0 volumes)
Out of scope: <none | list>
```

The closing deliverable is the single unified report with all findings and
recommendations; phase reports are internal artifacts.

No "next steps" sections or questions that imply new work.

## 🛑 Stop rules

- Target outside `sandbox_net` or a resolved public IP ➔ stop and log it.
- Docker not available ➔ stop Phase 2; never improvise local tests.
- Missing authorization at a gate ➔ stop the next phase.
- Any attempt to write code during Phase 1/2 ➔ block it.
- Destructive result or data loss ➔ stop everything and report.

## 📊 Pipeline status

Keep `reports/PIPELINE_STATUS.md` with a table:

| Phase | Agent | Status | Artifact | Timestamp |
|-------|-------|--------|----------|-----------|
| 1 | threat-modeler | ✅ done | `reports/THREAT_MODEL.md` | 2026-01-01T10:00Z |

Allowed statuses: `pending`, `running`, `blocked`, `done`, `failed`, `skipped`
(with a reason).
