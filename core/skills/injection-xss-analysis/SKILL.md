---
name: injection-xss-analysis
description: Detects SQLi (union, error, boolean blind, time based) and XSS (reflected, stored, DOM) in code with the exact line, analyzes patterns such as concatenation or client-only validation, and assesses filters against evasion techniques. Use when there are SQL queries or HTML/JS output.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# SQLi and XSS analysis

## Overview

Finds SQL injection and XSS by tracing every piece of untrusted data from its
source to its sink, with exact file and line, exploitable type and fix. Run by
`attack-surface-mapper`, `sqli-analyst` and `xss-analyst`.

## When to use

- The code builds SQL queries or generates HTML/JS with user data.
- A generic SAST flagged injections and they need classifying by type.
- You need to know whether a home-made filter or WAF really protects.

## Workflow

1. **Surface.** `attack-surface-mapper` → `reports/ATTACK_SURFACE.md` with the
   vectors (user input, HTTP parameters, payload vectors, APIs, structured data)
   and their exposure.
2. **Risk patterns** to look for in every flow:
   - String concatenation into SQL or HTML.
   - Missing server-side input validation.
   - Trust in client-side validation.
   - Denylist filters.
3. **SQLi.** `sqli-analyst` → `reports/SQLI_FINDINGS.md`:

   | Type | Happens when… |
   |------|---------------|
   | Union based | The query result is shown |
   | Error based | Engine errors reach the client |
   | Boolean blind | The response changes with true/false |
   | Time based | Only the response time varies |

4. **XSS.** `xss-analyst` → `reports/XSS_FINDINGS.md`:

   | Type | Flow |
   |------|------|
   | Reflected | Parameter → same response |
   | Stored | Persisted data → another response |
   | DOM based | Browser source → JS sink |

5. **Evasion.** For every existing filter, assess whether it withstands the
   OWASP evasion families (case changes, layered encodings, comments,
   non-recursive stripping, alternative tags/events, mXSS). A filter that does
   not is "Not effective"; the fix is parameterization or context-specific
   encoding.

## Rules

- Static, read-only analysis: dynamic verification belongs to `web-api-dast`
  in the sandbox.
- Evasion techniques are described to assess defenses, never as weaponized or
  data-extraction payloads.
- Every finding carries file:line, short snippet, type, CWE and fix.
