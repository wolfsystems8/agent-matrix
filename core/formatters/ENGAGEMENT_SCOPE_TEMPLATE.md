# Engagement scope and authorization

> Fill in before running any dynamic test. Without this file, Phase 2 is
> blocked.

## 1. Identification

| Field | Value |
|-------|-------|
| Project / repository | |
| System owner | |
| Audit lead | |
| Authorization date | |
| Test window | |
| Emergency contact | |

## 2. Authorization

Statement (check and sign):

- [ ] I confirm I own the system or have written authorization to audit it.
- [ ] Tests will be limited to the sandbox environment defined in
      `docker-compose.sandbox.yml`.
- [ ] No third-party systems, domains or IPs will be tested.
- [ ] No destructive or denial-of-service tests will be performed.
- [ ] Data and secrets found will be treated confidentially.
- [ ] Source code will be analyzed in place (read-only) and changed only if I
      answer "yes" at the remediation gate.

Signature / record: ______________________________________________

## 3. Technical scope

| Item | Included | Notes |
|------|----------|-------|
| Systems audit (ISO 19011 / 27005 / ITIL) | Yes | |
| Source code (SAST) | Yes | |
| Web application (DAST) | Yes | |
| REST/GraphQL APIs | Yes | |
| Sandbox network and services | Yes | |
| Logs (paths) | | |
| Cloud infrastructure | No | |
| Social engineering | No | |
| DoS / brute force | No | Forbidden |

## 4. Objectives and exclusions

- Main objective:
- Critical components:
- Explicitly excluded:

## 5. Test data

- Test accounts:
- Allowed synthetic data:
- Forbidden: real customer data, PII, production secrets.

## 6. Stop criteria

- Traffic detected outside `sandbox_net`.
- Target unavailable.
- Accidental access to real data.
- Any action that could have an impact outside the sandbox.
