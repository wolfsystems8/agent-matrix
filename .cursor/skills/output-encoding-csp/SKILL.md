---
name: output-encoding-csp
description: "Verifies context-specific output encoding (inside HTML, inside script, in JSON, in URL and in CSS) and rates the Content Security Policy on four levels (None, Low, Medium, Strict). Use when reviewing XSS defenses or security headers."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Context-specific encoding and CSP

## Overview

Operational best practices against XSS: every output is encoded for the context
that interprets it, and the CSP limits the damage if something slips through.
Run by `output-encoding-csp-reviewer` → `reports/ENCODING_CSP_REVIEW.md`.

## When to use

- After finding XSS, to define the exact fix.
- When reviewing templates, JSON serialization or HTTP headers.

## Workflow

1. **Context-specific encoding:**

   | Context | Rule |
   |---------|------|
   | Inside HTML | HTML entities (autoescape) |
   | HTML attribute | Attribute encoding + quotes |
   | Inside script | Do not interpolate; pass data via JSON/`data-*` and `textContent` |
   | JSON response | `application/json`, serializer, no JSONP; `<` when embedded in HTML |
   | URL | `encodeURIComponent` on the parameter + scheme allowlist |
   | CSS | CSS hex escaping, or no data in CSS |

2. **CSP levels:**

   | Level | Description |
   |-------|-------------|
   | None | Missing, or `Report-Only` only |
   | Low | Domain allowlist with `unsafe-inline`/`unsafe-eval` |
   | Medium | Nonce or hash, no `unsafe-inline` |
   | Strict | Nonce/hash + `strict-dynamic`, `object-src 'none'`, `base-uri 'none'`, Trusted Types |

3. Propose the target policy (Strict) adapted to the application.

## Rules

- CSP is defense in depth: it does not close an XSS on its own.
- Read-only; write only to `reports/`.
