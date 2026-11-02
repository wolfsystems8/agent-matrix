---
name: sdlc-security
description: Reviews software lifecycle security with the CIA triad, the Saltzer & Schroeder principles and per-phase risk management, and applies SQUARE or STRIDE depending on the system's state. Use when starting an SSDLC review or designing a system.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Security in the SDLC

## Overview

Sets the review frame before the code analysis: assets and CIA, secure design
principles, analysis methodology and risk in each phase of the lifecycle. Run by
`sdlc-security-lead`, `square-requirements` and `threat-modeler`.

## When to use

- When starting a security review of an application.
- When designing a new system or when security requirements are missing.
- When the user asks about CIA, Saltzer & Schroeder, SQUARE or STRIDE.

## Workflow

1. Delegate to `sdlc-security-lead` → `reports/SDLC_SECURITY_REVIEW.md`:
   - Assets classified by Confidentiality, Integrity and Availability.
   - The 8 Saltzer & Schroeder principles with status and evidence.
   - Chosen methodology and justification.
   - Gaps per phase: requirements, design, implementation, verification,
     deployment and maintenance.
2. Depending on the chosen methodology:

   | Choice | Action |
   |--------|--------|
   | SQUARE | `square-requirements` → `reports/SECURITY_REQUIREMENTS.md` (9 steps, abuse cases, `SR-NN` requirements) |
   | STRIDE | `threat-modeler` → `reports/THREAT_MODEL.md` |
   | Both | SQUARE first, then STRIDE using the requirements as criteria |

3. Pass assets and requirements to the code analysts
   (`injection-xss-analysis`, `web-vuln-identification`, `crypto-review`).

## Rules

- Read-only; write only to `reports/`.
- Without evidence, a principle is "No evidence", not "Not met".
- Requirements are verifiable and do not prescribe the implementation.
