---
name: threat-modeling
description: "Builds a STRIDE threat model with trust boundaries, assets and prioritized threats. Use when designing a system, before a SAST or when reviewing the authentication and data architecture."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Threat Modeling (STRIDE)

## Overview

Produces `reports/THREAT_MODEL.md` from the repository's real architecture,
applying STRIDE to every flow and prioritizing by likelihood and impact. The
operational detail lives in the `threat-modeler` agent.

## When to use

- Before a code audit or a pentest.
- When designing a new endpoint, authentication flow or integration.
- When the user asks "what can go wrong?" or wants trust boundaries reviewed.

## Workflow

1. Locate entry points and assets: routes, handlers, queues, cron, CLI,
   databases, storage and third parties.
2. Draw a Mermaid diagram with actors, components and trust boundaries.
3. For every flow, walk the six categories: Spoofing, Tampering, Repudiation,
   Information Disclosure, Denial of Service, Elevation of Privilege.
4. Record for each threat: current control, missing control, likelihood,
   impact and proposal.
5. Mark assumptions and information gaps explicitly; never invent endpoints.

## Output

`reports/THREAT_MODEL.md` with summary, diagram, STRIDE matrix, top threats and
assumptions.

## Rules

- Read-only: do not modify code or configuration.
- Do not run dynamic tests.
- A threat without evidence is marked as a hypothesis, not a finding.
