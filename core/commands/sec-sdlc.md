---
name: sec-sdlc
description: "Revisión de seguridad del SDLC: CIA, Saltzer & Schroeder, SQUARE/STRIDE, SQLi, XSS, fuerza bruta, path traversal, CSRF, criptografía, encoding/CSP y logs."
phase: 1
---

# /sec-sdlc — Seguridad en el ciclo de vida del software

Objetivo: `$ARGUMENTS` (por defecto, el repositorio actual).

1. Exige `reports/ENGAGEMENT_SCOPE.md`. Si el alcance no está claro, pregunta.
2. Si no existe `reports/AUDIT_PLAN.md`, delega en `audit-program-lead` para el
   mapa de cobertura.
3. Ejecuta en automático, en este orden, los agentes marcados `Sí`:
   `sdlc-security-lead` → `square-requirements` → `threat-modeler` →
   `attack-surface-mapper` → `sast-auditor` → `sqli-analyst` → `xss-analyst` →
   `web-vuln-analyst` → `crypto-reviewer` → `output-encoding-csp-reviewer` →
   `log-auditor` → `triage-master` → `risk-assessor`.
4. Marca el resto `skipped` con su motivo en `reports/PIPELINE_STATUS.md`.
5. Presenta el conteo por severidad, el top 5 de riesgos con archivo:línea y
   **detente**: pide aprobación para la Fase 2 si el plan la requiere.

No modifiques código fuente ni lo copies. Solo se corrige tras un "sí"
explícito en el gate de remediación.
