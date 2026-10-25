---
name: security-audit-pipeline
description: Orquesta una auditoría de seguridad completa en tres fases (SSDLC, pentest en sandbox, remediación) con gates humanos. Usar cuando el usuario pide "auditar la seguridad" de un repositorio, "revisar vulnerabilidades" o ejecutar el pipeline completo.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 0
  authority: orchestration
---

# Security Audit Pipeline

## Overview

Ejecuta el pipeline de `{{CORE}}/pipeline/PIPELINE_ORCHESTRATOR.md` de forma
secuencial. Cada fase tiene un artefacto, una autoridad y un punto de control
humano. No se salta ninguna fase y no se escribe código hasta la Fase 3.

## When to use

- El usuario pide una auditoría completa, un pentest autorizado o una revisión
  de seguridad end-to-end.
- Hay que coordinar varios agentes especializados y producir reportes.
- No usar para una pregunta puntual sobre una línea de código (usa
  `sast-code-audit`) ni para un único escaneo de red (usa `network-tls-audit`).

## Workflow

1. **Fase 0 — Alcance.**
   - Confirma repositorio, propietario, entorno autorizado y ventana.
   - Crea `reports/ENGAGEMENT_SCOPE.md`. Sin este archivo, detente.
   - Crea `reports/PIPELINE_STATUS.md` con todas las fases en `pending`.
2. **Fase 1 — SSDLC (solo lectura).**
   - Delega en `threat-modeler` → `reports/THREAT_MODEL.md`.
   - Delega en `sast-auditor` → `reports/SAST_RAW_FINDINGS.md`.
   - Delega en `triage-master` → `reports/AUDIT_REPORT.md`.
   - **Gate 1:** presenta resumen por severidad y top 5. Pide aprobación.
3. **Fase 2 — Sandbox.**
   - Delega en `sandbox-manager` → `reports/SANDBOX_STATUS.md`.
   - Si el aislamiento no es `true` o hay egreso, detente.
   - Delega en `network-auditor` → `reports/NETWORK_AUDIT.md`.
   - Delega en `web-dast-tester` → `reports/WEB_DAST_REPORT.md`.
   - Delega en `exploit-tester` → `reports/PENTEST_VERIFICATION.md`.
   - **Gate 2:** muestra confirmados y pide autorización para parchear.
4. **Fase 3 — Remediación.**
   - Delega en `secfix-patcher` con los IDs confirmados.
   - Delega en `regression-qa` → `reports/REMEDIATION_SUMMARY.md`.
   - Si hay hallazgos reabiertos, repite hasta 3 veces; luego escala.
5. **Cierre.** Destruye el sandbox, actualiza `PIPELINE_STATUS.md` y entrega un
   resumen con rutas a los reportes.

## Reglas

- Las fases 1 y 2 no modifican código fuente; solo escriben en `reports/` y en
  los scripts del sandbox.
- No lances pruebas dinámicas fuera de Docker ni contra IPs públicas.
- Si falta Docker, bloquea la Fase 2; no improvises.
- Cada hallazgo conserva su ID (`V-NN`, `N-NN`, `W-NN`) entre fases.

## Salida

`reports/` con: `ENGAGEMENT_SCOPE.md`, `THREAT_MODEL.md`,
`SAST_RAW_FINDINGS.md`, `AUDIT_REPORT.md`, `SANDBOX_STATUS.md`,
`NETWORK_AUDIT.md`, `WEB_DAST_REPORT.md`, `PENTEST_VERIFICATION.md`,
`REMEDIATION_SUMMARY.md`, `PIPELINE_STATUS.md`.
