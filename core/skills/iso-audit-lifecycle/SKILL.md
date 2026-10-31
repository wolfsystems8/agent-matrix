---
name: iso-audit-lifecycle
description: Conduce el ciclo de vida de una auditoría de sistemas según ISO 19011 (plan, mapa de subagentes, ejecución automática, riesgos ISO 27005, procesos ITIL, informe y seguimiento). Usar cuando el usuario pide una "auditoría de sistemas", "auditoría ISO" o un informe de cumplimiento.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Ciclo de vida de auditoría (ISO 19011)

## Overview

Coordina una auditoría de sistemas completa sobre el repositorio, en su sitio y
en solo lectura: el código no se copia ni se modifica. El agente
`audit-program-lead` decide qué especialistas hacen falta; el resto se omite con
motivo. El resultado es un informe de auditoría con hallazgos clasificados, un
registro de riesgos ordenado por severidad y recomendaciones de mejora.

## When to use

- "Audita este sistema", "auditoría ISO 19011/27001", "evalúa riesgos",
  "revisa nuestros procesos de cambio/despliegue".
- Se necesita evidencia de cumplimiento, no solo una lista de vulnerabilidades.
- No usar para revisar una sola función (usa `sast-code-audit`).

## Workflow

1. **Alcance (Fase 0).** Sin `reports/ENGAGEMENT_SCOPE.md` con autorización
   explícita, detente. Crea `reports/PIPELINE_STATUS.md` desde
   `{{CORE}}/formatters/PIPELINE_STATUS_TEMPLATE.md`.
2. **Plan y mapa de cobertura.** Delega en `audit-program-lead` (modo inicio)
   → `reports/AUDIT_PLAN.md`. Lee la tabla "Mapa de cobertura".
3. **Ejecución automática de la Fase 1.** Para cada agente de Fase 1 marcado
   `Sí`, en este orden y sin pedir confirmación individual:
   `sdlc-security-lead` → `square-requirements` → `threat-modeler` →
   `attack-surface-mapper` → `sast-auditor` → `sqli-analyst` → `xss-analyst` →
   `web-vuln-analyst` → `crypto-reviewer` → `output-encoding-csp-reviewer` →
   `log-auditor` → `triage-master` → `itil-process-auditor` → `risk-assessor`.
   Los marcados `No` quedan `skipped` en `PIPELINE_STATUS.md` con el motivo del
   plan. Si un agente falla, márcalo `failed` y continúa con los que no dependen
   de él.
4. **Gate 1.** Presenta el top 5 de `RISK_REGISTER.md` y el conteo por nivel.
   Si el plan marca agentes de Fase 2, pide aprobación para el sandbox; si no,
   pasa directamente al paso 6.
5. **Fase 2 (si se aprueba).** Ejecuta los agentes de Fase 2 marcados `Sí` vía
   `sandbox-pentest`. Después re-invoca `risk-assessor` para pasar a
   `Confirmado` los riesgos verificados.
6. **Informe.** Delega en `audit-program-lead` (modo cierre) →
   `reports/ISO19011_AUDIT_REPORT.md`.
7. **Gate de remediación.** Muestra las recomendaciones por severidad de
   `RISK_REGISTER.md` y pregunta literalmente:
   **"¿Deseas corregir las vulnerabilidades halladas? (sí/no)"**
   - **Sí:** pide qué IDs (todos, por nivel o lista) y ejecuta
     `security-remediation` y `security-regression-qa` solo sobre ellos.
   - **No:** registra la decisión en `PIPELINE_STATUS.md` y no toques el código.
8. **Cierre.** Si hubo sandbox, `sh {{CORE}}/sandbox/scripts/teardown.sh` debe
   imprimir `teardown: OK`. Entrega el formato de cierre del orquestador.

## Salidas

| Archivo | Agente |
|---------|--------|
| `AUDIT_PLAN.md` | `audit-program-lead` |
| `THREAT_MODEL.md`, `SAST_RAW_FINDINGS.md`, `AUDIT_REPORT.md` | Fase 1 técnica |
| `ITIL_PROCESS_AUDIT.md` | `itil-process-auditor` |
| `RISK_REGISTER.md` | `risk-assessor` |
| `ISO19011_AUDIT_REPORT.md` | `audit-program-lead` |

## Reglas

- El código fuente se lee en su sitio. No se copia a otro directorio ni a un
  contenedor; el sandbox lo monta en solo lectura.
- Ningún agente de esta skill escribe fuera de `reports/`.
- Solo se corrige código tras un "sí" explícito en el gate de remediación.
- IDs estables entre fases: `V-NN` (código), `P-NN` (procesos), `R-NN`
  (riesgos), `N-NN` (red), `W-NN` (web).
