---
name: network-tls-audit
description: Maps and audits ports, services, banners, TLS protocols and certificates inside the sandbox. Use to review the network surface, exposed services and encryption strength.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 2
  authority: sandbox
---

# Network & TLS Audit

## Overview

Discovers the sandbox network surface and assesses services and transport. The
command detail and report format live in the `network-auditor` agent.

## When to use

- The application exposes ports or infrastructure services.
- TLS, certificates or reachable data services must be verified.
- Before a DAST, to learn the real endpoints.

## Workflow

1. Resolve hosts and subnet from `pentest-runner`; never leave `sandbox_net`.
2. Full TCP scan (`nmap -sT -sV -p-`). UDP and raw scans (`-sS`, `-sU`) are out:
   the hardened runner does not run as root.
3. Identify versions/banners and unnecessary or obsolete services.
4. Audit TLS (`ssl-enum-ciphers`, `sslyze`, `openssl`): obsolete protocols, weak
   suites, certificate validity and chain.
5. Check data services/queues exposed without authentication using read-only
   commands only (`PING`, `nc -z`).
6. Document evidence (command + output) and remediation per `N-NN` finding.

## Output

`reports/NETWORK_AUDIT.md`.

## Rules

- No scans outside `sandbox_net`.
- No DoS, flooding, brute force or exploits.
- Do not change the network or compose configuration.
