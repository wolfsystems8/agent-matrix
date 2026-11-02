---
name: iso-audit-lifecycle
description: Runs the systems audit lifecycle per ISO 19011 (plan, sub-agent coverage map, automatic execution, ISO 27005 risks, ITIL processes, report and follow-up). Use when the user asks for a "systems audit", an "ISO audit" or a compliance report.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Audit lifecycle (ISO 19011)

## Overview

Coordinates a full systems audit of the repository, in place and read-only: the
code is neither copied nor modified. The `audit-program-lead` agent decides
which specialists are needed; the rest are skipped with a reason. The result is
an audit report with classified findings, a risk register sorted by severity and
improvement recommendations, written in the user's language.

## When to use

- "Audit this system", "ISO 19011/27001 audit", "assess risks", "review our
  change/deployment processes".
- Compliance evidence is needed, not just a list of vulnerabilities.
- Do not use it to review a single function (use `sast-code-audit`).

## Workflow

1. **Scope (Phase 0).** Without `reports/ENGAGEMENT_SCOPE.md` with explicit
   authorization, stop. Create `reports/PIPELINE_STATUS.md` from
   `{{CORE}}/formatters/PIPELINE_STATUS_TEMPLATE.md`.
2. **Plan and coverage map.** Delegate to `audit-program-lead` (start mode) →
   `reports/AUDIT_PLAN.md`. Read the "Coverage map" table.
3. **Automatic Phase 1 execution.** For every Phase 1 agent marked `Yes`, in
   this order and without asking for confirmation per agent:
   `sdlc-security-lead` → `square-requirements` → `threat-modeler` →
   `attack-surface-mapper` → `sast-auditor` → `sqli-analyst` → `xss-analyst` →
   `web-vuln-analyst` → `crypto-reviewer` → `output-encoding-csp-reviewer` →
   `log-auditor` → `triage-master` → `itil-process-auditor` → `risk-assessor`.
   Agents marked `No` become `skipped` in `PIPELINE_STATUS.md` with the plan's
   reason. If an agent fails, mark it `failed` and continue with those that do
   not depend on it.
4. **Gate 1.** Present the top 5 of `RISK_REGISTER.md` and the count by level.
   If the plan marks Phase 2 agents, ask for approval to use the sandbox;
   otherwise go to step 6.
5. **Phase 2 (if approved).** Run the Phase 2 agents marked `Yes` via
   `sandbox-pentest`. Then invoke `risk-assessor` again to move verified risks
   to `Confirmed`.
6. **Report.** Delegate to `audit-program-lead` (close mode) → the single
   unified report (`AUDIT_UNIFIED_REPORT.md`) consolidating all findings,
   recommendations and risk assessment.
7. **Remediation gate.** Show the recommendations by severity from
   `RISK_REGISTER.md` and ask, in the user's language:
   **"Do you want to fix the vulnerabilities found? (yes/no)"**
   - **Yes:** ask which IDs (all, by level or a list) and run
     `security-remediation` and `security-regression-qa` on those only.
   - **No:** record the decision in `PIPELINE_STATUS.md` and do not touch the
     code.
8. **Close.** If the sandbox was used, `sh {{CORE}}/sandbox/scripts/teardown.sh`
   must print `teardown: OK`. Deliver the orchestrator's closing format.

## Outputs

| File | Agent |
|------|-------|
| `AUDIT_PLAN.md` | `audit-program-lead` |
| `SDLC_SECURITY_REVIEW.md`, `THREAT_MODEL.md`, `SAST_RAW_FINDINGS.md`, specialist reports | Technical Phase 1 |
| `AUDIT_UNIFIED_REPORT.md` | `audit-program-lead` (final unified delivery) |
| `ITIL_PROCESS_AUDIT.md` | `itil-process-auditor` |
| `RISK_REGISTER.md` | `risk-assessor` |

## Rules

- The source code is read in place. It is never copied to another directory or
  into a container; the sandbox mounts it read-only.
- No agent in this skill writes outside `reports/`.
- Code is fixed only after an explicit "yes" at the remediation gate.
- Stable IDs across phases: `V-NN` (code), `P-NN` (processes), `R-NN` (risks),
  `N-NN` (network), `W-NN` (web).
