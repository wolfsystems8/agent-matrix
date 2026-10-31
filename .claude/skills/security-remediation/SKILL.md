---
name: security-remediation
description: "Applies minimal, secure patches to the findings the user chose to fix, with regression tests. Use only after the user answers yes at the remediation gate, to fix vulnerabilities without changing functionality."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 3
  authority: write
---

# Security Remediation

## Overview

Fixes confirmed vulnerabilities with the smallest necessary change and evidence
that expected behavior is preserved. The catalog of secure patterns lives in the
`secfix-patcher` agent.

## When to use

- The user answered **yes** at the remediation gate and chose which IDs to fix.
- `PENTEST_VERIFICATION.md` has **Confirmed** findings, or the user selected
  static findings explicitly.
- Never for cosmetic refactors or unverified findings.

## Workflow

1. Select only the authorized findings, sorted by severity.
2. Read the full flow and find the test that covers the behavior.
3. Apply the matching secure pattern:
   - SQL/NoSQL → prepared statements.
   - Commands → no shell, argument allowlist.
   - XSS → context-specific encoding + CSP.
   - Input → schema validation.
   - Path traversal → canonical path under a base directory.
   - CSRF → token + `SameSite` + `Origin` check.
   - Brute force → rate limiting and lockout.
   - Secrets → environment variables + rotation.
   - Passwords → Argon2id/bcrypt.
   - Authorization → check ownership and role on every access.
   - Session → secure cookies, JWT with a pinned algorithm.
4. Add or update a test that fails before and passes after.
5. Run tests, lint, typecheck and build.
6. Record the change in `reports/REMEDIATION_SUMMARY.md`.

## Output

Patched code + changes table in `REMEDIATION_SUMMARY.md`.

## Rules

- One finding per change, no unrelated refactors.
- Do not silence analyzers (`@ts-ignore`, `# noqa`, `eslint-disable`).
- Do not delete or weaken tests.
- If the patch changes a public contract, document the migration.
