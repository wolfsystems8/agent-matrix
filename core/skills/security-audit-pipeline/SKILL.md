---
name: security-audit-pipeline
description: Orchestrates a full security audit (systems audit and SSDLC, sandbox pentest, remediation) with human gates, running only the sub-agents the coverage map requires. Use when the user asks to "audit security", "review vulnerabilities" or run the full pipeline.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 0
  authority: orchestration
---

# Security Audit Pipeline

## Overview

Runs the pipeline in `{{CORE}}/pipeline/PIPELINE_ORCHESTRATOR.md` sequentially.
Each phase has an artifact, an authority and a human checkpoint. No phase is
skipped and no code is written until the user says "yes" at the remediation
gate. Reports and messages go in the user's language.

## When to use

- The user asks for a full audit, an authorized pentest or an end-to-end
  security review.
- Several specialist agents must be coordinated and reports produced.
- Do not use it for a one-off question about a line of code (use
  `sast-code-audit`) or a single network scan (use `network-tls-audit`).

## Workflow

1. **Phase 0 — Scope.**
   - Confirm repository, owner, authorized environment and window.
   - Create `reports/ENGAGEMENT_SCOPE.md`. Without it, stop.
   - Create `reports/PIPELINE_STATUS.md` with every phase `pending`.
2. **Phase 1 — Systems audit and SSDLC (read-only).**
   - Delegate to `audit-program-lead` → `reports/AUDIT_PLAN.md` with the
     coverage map. Run only the agents marked `Yes` automatically; the rest
     become `skipped` with a reason (see skill `iso-audit-lifecycle`).
   - Delegate to `sdlc-security-lead` and, per its choice,
     `square-requirements` and/or `threat-modeler` (skill `sdlc-security`).
   - Delegate to `attack-surface-mapper` and `sast-auditor`.
   - Delegate to the analysts: `sqli-analyst`, `xss-analyst`,
     `web-vuln-analyst`, `crypto-reviewer`, `output-encoding-csp-reviewer`,
     `log-auditor`.
   - Delegate to `triage-master` → `reports/AUDIT_REPORT.md`.
   - Delegate to `itil-process-auditor` → `reports/ITIL_PROCESS_AUDIT.md`.
   - Delegate to `risk-assessor` → `reports/RISK_REGISTER.md` by severity.
   - **Gate 1:** present the count by risk level and the top 5. Ask for
     approval.
3. **Phase 2 — Sandbox.**
   - Delegate to `sandbox-manager` → `reports/SANDBOX_STATUS.md`.
   - If isolation is not `true` or there is egress, stop.
   - Delegate to `network-auditor` → `reports/NETWORK_AUDIT.md`.
   - Delegate to `web-dast-tester` → `reports/WEB_DAST_REPORT.md`.
   - Delegate to `exploit-tester` → `reports/PENTEST_VERIFICATION.md`.
   - Invoke `risk-assessor` again to mark confirmed risks.
   - **Gate 2 (remediation):** delegate to `audit-program-lead` (close) →
     `reports/ISO19011_AUDIT_REPORT.md`, show the recommendations by severity
     and ask whether to fix them. On "no", mark Phase 3 `skipped` and go to the
     close without touching the code.
4. **Phase 3 — Remediation.**
   - Delegate to `secfix-patcher` with the IDs the user chose.
   - Delegate to `regression-qa` → `reports/REMEDIATION_SUMMARY.md`.
   - If findings are reopened, repeat up to 3 times; then escalate.
5. **Mandatory close.** Run `sh {{CORE}}/sandbox/scripts/teardown.sh` and check
   that it prints `teardown: OK` (no containers, networks, volumes or PoC
   images). Update `PIPELINE_STATUS.md` and deliver a summary with report
   paths. Without the close, the pipeline is `blocked`, not `done`.

## Rules

- Phases 1 and 2 do not modify source code; they only write to `reports/` and
  sandbox scripts. The code is read in place and never copied.
- Never run dynamic tests outside Docker or against public IPs.
- If Docker is missing, block Phase 2; do not improvise.
- Every finding keeps its ID (`V-NN`, `N-NN`, `W-NN`, `R-NN`) across phases.
- When the last phase ends everything is closed: no containers, networks,
  volumes or temporary PoC artifacts remain.
- **Closure and scope.** The analysis is done when the 7 conditions in
  `PIPELINE_ORCHESTRATOR.md` are met (IDs with final status, remediation
  re-verified, green suite, dependencies scanned, `teardown: OK`, state
  persisted and clean repository). If the user says it is done, it is closed:
  no phases are reopened, observations do not become tasks, no drive-by changes
  are applied and no "next steps" are proposed. Extending scope requires an
  explicit request, a record in `PIPELINE_STATUS.md` and a new gate.

## Output

`reports/` with: `ENGAGEMENT_SCOPE.md`, `AUDIT_PLAN.md`, Phase 1 reports,
`AUDIT_REPORT.md`, `RISK_REGISTER.md`, Phase 2 reports,
`ISO19011_AUDIT_REPORT.md`, `REMEDIATION_SUMMARY.md` (if "yes"),
`PIPELINE_STATUS.md`.
