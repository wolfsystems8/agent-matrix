---
name: sec-task
description: "Runs a targeted security check: routes the request to only the agents it needs (SQLi, XSS, crypto, logs, ports, risks…)."
phase: 0
---

# /sec-task — Targeted security check

Request: `$ARGUMENTS`

Follow the `security-task-router` skill, answering in the user's language:

1. Require `reports/ENGAGEMENT_SCOPE.md`. If the scope is unclear, ask.
2. Classify the request. If it is broad, hand off to `iso-audit-lifecycle` or
   `security-audit-pipeline`; if it is ambiguous, ask one question and stop.
3. Match the request to agents with the routing table, resolve dependencies and
   narrow each agent to the area the user named.
4. Run the selected agents automatically and record the routing decision and
   the `skipped` agents in `reports/PIPELINE_STATUS.md`.
5. If there are findings, consolidate them, sort them by severity with
   `risk-assessor` and ask whether to fix them (yes/no).

Do not modify or copy the source code. Code is fixed only after an explicit
"yes".
