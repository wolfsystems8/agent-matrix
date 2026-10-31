# /sec-pipeline — Full audit with gates

Target: `$ARGUMENTS` (defaults to the current repository).

Run `security-audit-pipeline` end to end, respecting the gates and answering in
the user's language:

1. **Phase 0:** scope and authorization in `reports/ENGAGEMENT_SCOPE.md`.
2. **Phase 1:** `audit-program-lead` builds the coverage map; the agents marked
   `Yes` run automatically (SDLC, specialists, triage, ITIL, risks).
   **GATE 1:** ask for approval.
3. **Phase 2:** `sandbox-manager` → `network-auditor` → `web-dast-tester` →
   `exploit-tester`.
4. **Remediation gate:** ISO 19011 report, recommendations by severity and the
   question "Do you want to fix the vulnerabilities found? (yes/no)".
5. **Phase 3 (only on "yes"):** `secfix-patcher` → `regression-qa`.
6. **Close:** run `sh core/sandbox/scripts/teardown.sh` (requires
   `teardown: OK`: no containers, networks, volumes or temporary PoCs),
   summarize closed/partial/reopened findings and link every report.

Never move to the next phase without explicit approval. If an orchestrator stop
condition is met, stop and explain it.
