---
name: web-api-dast
description: Dynamically tests HTTP headers, CORS, cookies, SQLi/XSS confirmation and REST/GraphQL APIs (BOLA, rate limiting, mass assignment). Use with the application running in the sandbox and a valid authorization.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 2
  authority: sandbox
---

# Web & API DAST

## Overview

Dynamic audit from the point of view of a browser or HTTP client. Produces
`reports/WEB_DAST_REPORT.md` with reproducible findings. The full checklist
lives in the `web-dast-tester` agent.

## When to use

- The app is up in the sandbox and answers at `http://target-app:8080`.
- Headers, CORS, cookies or API endpoints must be validated.
- Static SQLi/XSS findings need dynamic confirmation.
- BOLA/IDOR, rate limiting abuse or mass assignment is suspected.

## Workflow

1. Check `SANDBOX_STATUS.md` and set the internal base URL.
2. Review security headers and their real value (CSP, HSTS, XFO, nosniff,
   Referrer-Policy, Permissions-Policy).
3. Analyze cookies (`HttpOnly`, `Secure`, `SameSite`) and CORS with an untrusted
   `Origin`.
4. Probe sensitive paths (`.git`, `.env`, backups, Swagger/OpenAPI, actuator)
   and confirm the content before reporting.
5. Confirm SQLi/XSS with differential, non-destructive probes by subtype.
6. Test APIs: BOLA with two accounts, auth/rate limiting, CSRF, pagination and
   upload limits, mass assignment, GraphQL introspection.
7. Record each `W-NN` finding with sanitized request/response and remediation.

## Output

`reports/WEB_DAST_REPORT.md`.

## Rules

- Only `target-app` inside `sandbox_net`; no mass scanners or DoS.
- At most 20 req/s and explicit timeouts.
- Do not alter data persistently; use test accounts and test data.
- Sanitize tokens, cookies and PII in the evidence.
