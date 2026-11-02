---
name: security-task-router
description: Routes a specific security request to only the agents it needs (e.g. "check XSS in login", "review the crypto", "scan the ports"), resolving dependencies and ending at the remediation gate. Use when the user asks for a targeted check instead of a full audit.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 0
  authority: orchestration
---

# Security Task Router

## Overview

Maps the user's request to the smallest set of agents that answers it. A full
audit uses the coverage map of `audit-program-lead`; a targeted request uses this
router. Both follow `{{CORE}}/pipeline/PIPELINE_ORCHESTRATOR.md` and the ethical
directive. Answer in the user's language.

## When to use

- The user names a vulnerability class, a component or a single activity:
  "look for SQL injection", "is the login vulnerable to brute force?", "audit
  the logs", "rate our CSP", "map the network".
- Do not use it for "audit everything", "ISO audit" or "full pipeline": those go
  to `iso-audit-lifecycle` or `security-audit-pipeline`.

## Workflow

1. **Classify the request.**

   | Class | Signal | Route |
   |-------|--------|-------|
   | Targeted | Names one or more topics from the routing table | Step 2 |
   | Broad | "full audit", "everything", "ISO 19011", "pipeline" | Hand off to `iso-audit-lifecycle` / `security-audit-pipeline` |
   | Ambiguous | "check security", "is it safe?" with no topic | Ask one question listing the main topics; run nothing until answered |

2. **Match intents to agents** (a request can match several rows; take the
   union):

   | The request mentions… | Agents (in order) |
   |-----------------------|-------------------|
   | SQL injection, SQLi, queries, database input | `attack-surface-mapper` → `sqli-analyst` |
   | XSS, scripts, templates, HTML output, DOM | `attack-surface-mapper` → `xss-analyst` → `output-encoding-csp-reviewer` |
   | Encoding, CSP, security headers (static) | `output-encoding-csp-reviewer` |
   | Brute force, login, path traversal, file download/upload, CSRF | `attack-surface-mapper` → `web-vuln-analyst` |
   | Attack surface, entry points, attack vectors, APIs, parameters | `attack-surface-mapper` |
   | Cryptography, encryption, passwords, hashing, tokens, JWT, keys | `crypto-reviewer` |
   | Logs, detection, monitoring, auth/app/network/web server/OS logs | `log-auditor` |
   | Secrets, general code review, OWASP, CWE | `sast-auditor` |
   | Threat model, STRIDE, architecture, trust boundaries | `threat-modeler` |
   | Security requirements, SQUARE, abuse cases | `square-requirements` |
   | CIA triad, Saltzer & Schroeder, design principles, SDLC | `sdlc-security-lead` |
   | Risks, risk matrix, risk register, ISO 27005, prioritize | `risk-assessor` (needs existing findings) |
   | Processes, ITIL, change management, CI/CD, deployments | `itil-process-auditor` |
   | ISO 19011, compliance, audit report | `audit-program-lead` |
   | Network, ports, services, TLS, certificates (live) | `sandbox-manager` → `network-auditor` |
   | Headers, CORS, cookies, APIs, BOLA, live web testing | `sandbox-manager` → `web-dast-tester` |
   | Confirm, verify or prove a finding, PoC | `sandbox-manager` → `exploit-tester` |
   | Fix, patch, correct | Remediation gate → `secfix-patcher` → `regression-qa` |

3. **Resolve dependencies.**
   - `sqli-analyst`, `xss-analyst` and `web-vuln-analyst` read
     `reports/ATTACK_SURFACE.md`; if it is missing, run `attack-surface-mapper`
     first, limited to the area the user named.
   - `risk-assessor` needs findings; if none exist, run the matching analysts
     first.
   - Any live (Phase 2) agent needs `sandbox-manager` and verified isolation.
   - "Fix" requests need findings for the named IDs or topic; if there are
     none, analyze first and then go to the remediation gate.

4. **Check authorization.** Every route requires `reports/ENGAGEMENT_SCOPE.md`.
   An explicit live request ("scan the ports") counts as the Phase 2 approval,
   but scope, isolation and stop rules still apply.

5. **Narrow the scope.** Pass the area the user named (files, routes,
   components) to each agent so it does not analyze the whole repository.

6. **Run and record.** Run the selected agents automatically in pipeline order.
   In `reports/PIPELINE_STATUS.md` mark them `running`/`done` and every other
   agent `skipped` with the reason "not requested". Write the routing decision
   (request, matched intents, agents) in the "Blocks and decisions" table.

7. **Consolidate.** If two or more analysts produced findings, run
   `triage-master`. If there are findings, run `risk-assessor` to sort them by
   severity with recommendations.

8. **Remediation gate.** If there are findings, show the recommendations by
   severity and ask: **"Do you want to fix the vulnerabilities found?
   (yes/no)"**. On "yes", fix only the chosen IDs; on "no", do not touch the
   code. If the sandbox was used, close it with
   `sh {{CORE}}/sandbox/scripts/teardown.sh` (requires `teardown: OK`).

## Examples

| Request | Agents run |
|---------|------------|
| "Is there SQL injection in the search?" | `attack-surface-mapper` (search) → `sqli-analyst` → `risk-assessor` |
| "Check XSS and the CSP" | `attack-surface-mapper` → `xss-analyst` → `output-encoding-csp-reviewer` → `triage-master` → `risk-assessor` |
| "Are passwords stored safely?" | `crypto-reviewer` → `risk-assessor` |
| "Scan the open ports" | `sandbox-manager` → `network-auditor` → `risk-assessor` → teardown |
| "Is it secure?" | Ask which topics to cover |

## Rules

- Run only what the request needs; never widen the scope on your own.
- The source code is read in place and never copied.
- Code is changed only after an explicit "yes" at the remediation gate.
- If the request maps to nothing in the table, ask; do not guess.
