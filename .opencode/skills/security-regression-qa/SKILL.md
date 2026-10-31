---
name: security-regression-qa
description: "Verifies that patches close the vulnerabilities and do not break the application, re-running tests and PoCs. Use at the end of remediation to issue the closure report."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 3
  authority: write
---

# Security Regression QA

## Overview

Closes the loop: runs the suite, re-validates the PoCs in the sandbox and issues
`reports/REMEDIATION_SUMMARY.md` with the final status of every finding. The
detailed procedure lives in the `regression-qa` agent.

## When to use

- Security patches were applied and must be verified.
- Before declaring an audit finished or opening a security PR.
- When a PoC must stop reproducing.

## Workflow

1. Run the project suite (`npm test`, `pytest`, `go test ./...`).
2. Run lint, typecheck and build if they exist.
3. Re-run every `poc_<id>` in the sandbox and compare before/after.
4. Test the affected critical flows (login, permissions, payments, uploads).
5. Mark each finding: Closed, Partial or Reopened.
6. If any are reopened, go back to `security-remediation` (max. 3 iterations).
7. **Mandatory close.** Run `sh core/sandbox/scripts/teardown.sh` and
   confirm it prints `teardown: OK` (no containers, networks or volumes).
   Document the environment used in `REMEDIATION_SUMMARY.md`.

## Output

`reports/REMEDIATION_SUMMARY.md`.

## Rules

- No re-run, no closure.
- Do not adapt tests to hide a real failure.
- If you cannot run something, say so; never assume success.
- Do not leave sandbox containers or volumes running: the close is part of the
  work, not an extra.
