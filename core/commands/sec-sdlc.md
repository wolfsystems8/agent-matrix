---
name: sec-sdlc
description: "SDLC security review: CIA, Saltzer & Schroeder, SQUARE/STRIDE, SQLi, XSS, brute force, path traversal, CSRF, cryptography, encoding/CSP and logs."
phase: 1
---

# /sec-sdlc — Security in the software development lifecycle

Target: `$ARGUMENTS` (defaults to the current repository).

Answer in the user's language:

1. Require `reports/ENGAGEMENT_SCOPE.md`. If the scope is unclear, ask.
2. If `reports/AUDIT_PLAN.md` does not exist, delegate to `audit-program-lead`
   for the coverage map.
3. Automatically run, in this order, the agents marked `Yes`:
   `sdlc-security-lead` → `square-requirements` → `threat-modeler` →
   `attack-surface-mapper` → `sast-auditor` → `sqli-analyst` → `xss-analyst` →
   `web-vuln-analyst` → `crypto-reviewer` → `output-encoding-csp-reviewer` →
   `log-auditor` → `triage-master` → `risk-assessor`.
4. Mark the rest `skipped` with their reason in `reports/PIPELINE_STATUS.md`.
5. Present the count by severity and the top 5 risks with file:line, then
   **stop**: ask for approval for Phase 2 if the plan requires it.

Do not modify or copy the source code. Code is fixed only after an explicit
"yes" at the remediation gate.
