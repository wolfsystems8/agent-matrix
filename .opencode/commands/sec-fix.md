---
description: "Runs Phase 3: patches the findings the user chose to fix and validates with tests and PoCs."
---

# /sec-fix — Remediation and QA

Target: `$ARGUMENTS` (defaults to the findings the user approved).

Precondition: an explicit "yes" from the user with the IDs to fix, and
`reports/PENTEST_VERIFICATION.md` with **Confirmed** findings (or static
findings the user selected). Without the "yes", stop.

Follow the `security-remediation` and `security-regression-qa` skills,
answering in the user's language:

1. `secfix-patcher` applies minimal patches per authorized finding.
2. Add/update one regression test per finding.
3. Run tests, lint, typecheck and build.
4. `regression-qa` re-runs the PoCs in the sandbox and issues
   `reports/REMEDIATION_SUMMARY.md`.
5. If a finding is reopened, iterate (max. 3) or escalate to the user.

Do not touch unrelated code. Do not silence analyzers or delete tests.
