---
name: sast-code-audit
description: "Audits source code for injections, secrets, weak cryptography and authorization flaws, with file and line. Use to review a repository without running it or before a pentest."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# SAST Code Audit

## Overview

Static review guided by OWASP Top 10, CWE and ASVS. Produces
`reports/SAST_RAW_FINDINGS.md` with verifiable evidence and concrete
remediation. The full checklist lives in the `sast-auditor` agent.

## When to use

- The user asks to "review the code for vulnerabilities".
- A PR or sensitive module (auth, payments, uploads, SQL) must be assessed.
- Before Phase 2, to aim the PoCs.

## Workflow

1. Identify the stack, framework and entry points.
2. Review in this order: data queries, command execution, HTML rendering,
   authentication/session, authorization, uploads, cryptography and secrets.
3. For every candidate, trace the source → sink flow and check whether there is
   effective validation or sanitization.
4. Run available tools read-only (`semgrep`, `bandit`, `npm audit`, `gosec`)
   and include the command.
5. Discard false positives with a justification; never delete them silently.
6. Write the findings table with `S-NN` ID, CWE, confidence and remediation.

## Output

`reports/SAST_RAW_FINDINGS.md`.

## Rules

- Do not modify code or run the application.
- Never report without file and line.
- Mask secrets; report the location, not the value.
- A dangerous pattern without an exploitable flow is marked "needs review".
