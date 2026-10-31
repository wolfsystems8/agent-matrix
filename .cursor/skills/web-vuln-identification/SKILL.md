---
name: web-vuln-identification
description: "Identifies attack vectors and which web vulnerabilities the software is exposed to (XSS, SQLi, brute force, path traversal, CSRF), with the fundamentals of each and the exact line. Use for a complete web exposure classification."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Web vulnerability identification

## Overview

Answers "what is this web application exposed to?" with identification
techniques over the code: vector inventory, source → sink tracing and
classification by type. Run by `attack-surface-mapper` and `web-vuln-analyst`;
SQLi and XSS are delegated to `injection-xss-analysis`.

## When to use

- Before a web pentest, to aim it.
- When the user asks "what vulnerabilities does this web app/API have".
- When reviewing authentication, file download/upload or forms.

## Workflow

1. **Attack vectors** (`attack-surface-mapper`):

   | Category | Examples |
   |----------|----------|
   | User input | Forms, search, profiles |
   | HTTP parameters | Query, body, path, headers, cookies |
   | Payload vectors | Uploads, multipart, archives |
   | APIs | REST, GraphQL, WebSocket, webhooks |
   | Structured data | JSON, XML, YAML, CSV, serialized objects |

2. **Identification techniques:** dangerous sink search, source → sink tracing,
   validation review (server vs. client-only), comparison against requirements
   (`SR-NN`) and OWASP ASVS.
3. **Exposure classification** per vector: XSS, SQLi, brute force, path
   traversal, CSRF or others.
4. **Fundamentals per type** (`web-vuln-analyst` → `reports/WEB_VULN_FINDINGS.md`):

   | Type | Root cause | Correct control |
   |------|------------|-----------------|
   | Brute force | Unlimited attempts, distinguishable errors | Rate limiting, lockout, MFA, slow hash |
   | Path traversal | Path built from user data | Canonical path under a base directory, allowlist |
   | CSRF | State changed via cookie without proof of intent | Token, `SameSite`, `Origin` check |
   | SQLi | Concatenation into SQL | Parameterized queries |
   | XSS | Output without context-specific encoding | Autoescape, context encoding, CSP |

## Rules

- Read-only; write only to `reports/`.
- A vector without an identified sink is an assumption, not a finding.
- Every finding states file:line, vector, CWE and fix.
