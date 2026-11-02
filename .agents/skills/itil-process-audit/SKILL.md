---
name: itil-process-audit
description: "Audits ITIL 4 operational practices (change, deployment, configuration, assets, incidents, monitoring, access, continuity) with repository evidence and a maturity level. Use when there is CI/CD, IaC or operational documentation."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Process audit with ITIL 4

## Overview

Assesses whether the service management practices that protect the CIA triad
are implemented, with a maturity level from 1 to 5 and `P-NN` findings. The
operational detail lives in the `itil-process-auditor` agent.

## When to use

- The repository has pipelines, IaC, containers or operational documentation.
- The user asks about change management, deployments, incidents or continuity
  as part of an audit.
- Do not use it to look for code vulnerabilities (use `sast-code-audit`).

## Workflow

1. Locate the evidence: CI workflows, `CODEOWNERS`, IaC, `Dockerfile`,
   lockfiles, `SECURITY.md`, `CHANGELOG`, runbooks, logging configuration.
2. Walk through the practices: change enablement, release and deployment,
   configuration, IT assets, incidents, problems, monitoring and events,
   information security, access and continuity.
3. Assign maturity (1 initial · 2 repeatable · 3 defined · 4 managed ·
   5 optimized) with file and line as evidence.
4. Raise one `P-NN` per practice with maturity ≤ 2 or a missing security
   control, with its CIA impact and a concrete recommendation.
5. Write `reports/ITIL_PROCESS_AUDIT.md`.

## Rules

- What is not in the repository is marked "no evidence", not "nonconformity".
- Do not modify pipelines or configuration.
- Write only to `reports/`.
