# Standard Vulnerability Report Template (CVSS v3.1)

## Findings table

| ID | Methodology / Module | Component / Line | Vulnerability (CWE) | STRIDE vector | CVSS v3.1 | Severity | Sandbox status |
|---|---|---|---|---|---|---|---|
| V-01 | SAST | `src/auth.js:42` | SQL Injection (CWE-89) | Tampering | 9.8 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | 🔴 Critical | Pending |
| V-02 | DAST | `GET /api/users/1` | BOLA / IDOR (CWE-639) | Elevation of Privilege | 8.1 `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` | 🟠 High | Confirmed |

## Severity scale

| CVSS v3.1 | Severity | Suggested SLA |
|-----------|----------|---------------|
| 9.0 – 10.0 | 🔴 Critical | 24 h |
| 7.0 – 8.9 | 🟠 High | 7 days |
| 4.0 – 6.9 | 🟡 Medium | 30 days |
| 0.1 – 3.9 | 🔵 Low | 90 days |
| 0.0 | ⚪ Informational | Backlog |

## Technical detail (repeat per finding)

### V-01 — SQL Injection in authentication

- **Location:** `src/auth.js:42`
- **CWE / Category:** CWE-89 — Improper Neutralization of Special Elements used in an SQL Command
- **Subtype:** union based / error based / boolean blind / time based
- **STRIDE vector:** Tampering
- **CVSS v3.1:** `9.8` — `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
- **Description:** The query is built by concatenating the `email` parameter,
  which allows altering the `WHERE` clause and authenticating without valid
  credentials.
- **Evidence:** sanitized request/response or code snippet.
- **Impact:** unauthorized read/write access to the database.
- **Suggested remediation:** use prepared statements with bound parameters;
  validate the input schema with Zod/Joi.
- **Sandbox status:** Pending / Confirmed / Mitigated / False positive.
- **References:** OWASP ASVS 5.3.4, OWASP Top 10 A03:2021.

## Writing rules

1. One finding per section, with a stable ID (`V-01`, `V-02`, …).
2. No real secrets or personal data; mask them.
3. Every Confirmed finding includes a reproducible PoC or evidence.
4. Every finding includes a concrete, verifiable remediation.
5. False positives are documented and justified, never removed silently.
6. Write the report in the user's language; keep IDs and technical terms as-is.
