---
name: risk-assessment-iso27005
description: "Identifies, analyzes, evaluates and proposes risk treatment per ISO/IEC 27005 and builds a risk table sorted by severity with recommendations. Use after SAST/pentest or when the user asks for a risk matrix or register."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Risk assessment and treatment (ISO/IEC 27005)

## Overview

Turns technical findings (`V-NN`, `W-NN`, `N-NN`) and process findings (`P-NN`)
into `R-NN` risks with likelihood, impact, level, treatment option and
recommendation. The operational detail lives in the `risk-assessor` agent.

## When to use

- There are audit reports and they must be prioritized by business risk.
- The user asks for a "risk matrix", "risk register", "risk treatment" or
  "ISO 27005".
- Before deciding what to fix first.

## Workflow

1. **Context.** Define assets (data, credentials, services, availability) and
   acceptance criteria: `Low` may be retained; the rest is treated or
   explicitly accepted.
2. **Identification.** For each finding build the scenario
   asset → threat → vulnerability → consequence and mark the CIA dimension.
   Group findings that materialize the same scenario into a single risk.
3. **Analysis.** Likelihood and impact from 1 to 5, each with its justification.
   A finding confirmed in the sandbox raises likelihood by one level.
4. **Evaluation.** Score = L × I. Critical 20–25 · High 12–19 ·
   Medium 6–11 · Low 1–5.
5. **Treatment.** Modify, Retain, Avoid or Share, with the ISO/IEC 27001:2022
   Annex A control and the expected residual risk.
6. **Sort** from highest to lowest score and write `reports/RISK_REGISTER.md`
   with heat map, register and recommendations grouped by level.

## Example row

```markdown
| R-01 | Database exfiltration via SQLi | Customer data | C, I | V-02, W-01 | 5 | 5 | 25 | Critical | Modify | A.8.28 Secure coding | Low | Confirmed |
```

## Rules

- No evidence, no risk: a hypothesis is recorded as such.
- Do not apply treatments; only recommend them. The decision is the user's.
- Write only to `reports/`.
