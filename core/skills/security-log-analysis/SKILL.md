---
name: security-log-analysis
description: Assesses log coverage for authentication, application, network, web server and operating system, log quality (no sensitive data or injection), and detects attack indicators in in-scope logs. Use in security analysis and detection work.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Security log analysis

## Overview

Checks that the system can detect and investigate an attack and, if logs are
available, looks for indicators. Run by `log-auditor` → `reports/LOG_AUDIT.md`.

## When to use

- In an audit that assesses detection and response.
- After Phase 2, with the sandbox logs exported to `reports/logs/`.
- When the user provides logs within the authorized scope.

## Workflow

1. **Coverage** by source: authentication, application, network, web server and
   operating system.
2. **Quality:** structured format, timestamps, correlation, no secrets or PII
   (CWE-532), no log injection (CWE-117), retention.
3. **Indicators:** brute force, scanning, SQLi/XSS in URLs, path traversal, OS
   escalation; each one with the log line as evidence.
4. Link each indicator to the existing `V-NN`/`W-NN` findings.

## Rules

- Only logs within scope; mask personal data.
- Read-only; write only to `reports/`.
