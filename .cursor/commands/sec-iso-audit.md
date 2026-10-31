# /sec-iso-audit — Systems audit (ISO 19011)

Target: `$ARGUMENTS` (defaults to the current repository).

Follow the `iso-audit-lifecycle` skill and answer in the user's language:

1. Require `reports/ENGAGEMENT_SCOPE.md`. If the scope is unclear, ask before
   continuing.
2. Delegate to `audit-program-lead` → `reports/AUDIT_PLAN.md` with the coverage
   map.
3. Automatically run the Phase 1 agents marked `Yes` and mark the rest
   `skipped` with their reason in `reports/PIPELINE_STATUS.md`.
4. Delegate to `risk-assessor` → `reports/RISK_REGISTER.md` sorted by severity.
5. Present the count by level and the top 5 risks, then **stop**: ask for
   approval for Phase 2 if the plan requires it.

Do not modify or copy the source code. Code is fixed only after an explicit
"yes" at the remediation gate.
