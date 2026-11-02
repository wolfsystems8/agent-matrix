---
name: sec-audit
description: "Runs Phase 1 (SSDLC) on the repository: threat model, SAST and CVSS triage."
phase: 1
agent: audit-program-lead
---

# /sec-audit — Static analysis and threat model

Target: `$ARGUMENTS` (defaults to the current repository).

Follow the `security-audit-pipeline` skill limited to **Phase 0 and Phase 1**,
answering in the user's language:

1. Create `reports/ENGAGEMENT_SCOPE.md` if it does not exist. If the scope is
   unclear, ask before continuing.
2. Delegate to `threat-modeler` → `reports/THREAT_MODEL.md`.
3. Delegate to `sast-auditor` → `reports/SAST_RAW_FINDINGS.md`.
4. Delegate to `triage-master` → `reports/AUDIT_REPORT.md` with CVSS v3.1.
5. Update `reports/PIPELINE_STATUS.md`.

Do not modify source code. Do not run dynamic tests. When done, present the
count by severity and the top 5 findings, then **stop** and ask for approval
for Phase 2.
