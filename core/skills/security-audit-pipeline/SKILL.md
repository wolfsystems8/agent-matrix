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
2. **Fase 1 — Auditoría y SSDLC (solo lectura).**
   - Delega en `audit-program-lead` → `reports/AUDIT_PLAN.md` con el mapa de
     cobertura. Ejecuta en automático solo los agentes marcados `Sí`; el resto
     queda `skipped` con motivo (ver skill `iso-audit-lifecycle`).
   - Delega en `sdlc-security-lead` y, según su elección,
     `square-requirements` y/o `threat-modeler` (skill `sdlc-security`).
   - Delega en `attack-surface-mapper` y `sast-auditor`.
   - Delega en los analistas: `sqli-analyst`, `xss-analyst`,
     `web-vuln-analyst`, `crypto-reviewer`, `output-encoding-csp-reviewer`,
     `log-auditor`.
   - Delega en `triage-master` → `reports/AUDIT_REPORT.md`.
   - Delega en `itil-process-auditor` → `reports/ITIL_PROCESS_AUDIT.md`.
   - Delega en `risk-assessor` → `reports/RISK_REGISTER.md` por severidad.
   - **Gate 1:** presenta conteo por nivel de riesgo y top 5. Pide aprobación.
3. **Fase 2 — Sandbox.**
   - Delega en `sandbox-manager` → `reports/SANDBOX_STATUS.md`.
   - Si el aislamiento no es `true` o hay egreso, detente.
   - Delega en `network-auditor` → `reports/NETWORK_AUDIT.md`.
   - Delega en `web-dast-tester` → `reports/WEB_DAST_REPORT.md`.
   - Delega en `exploit-tester` → `reports/PENTEST_VERIFICATION.md`.
   - Re-invoca `risk-assessor` para marcar los riesgos confirmados.
   - **Gate 2 (remediación):** delega en `audit-program-lead` (cierre) →
     `reports/ISO19011_AUDIT_REPORT.md`, muestra las recomendaciones por
     severidad y pregunta si se desean corregir. Con "no", salta a la Fase 3
     como `skipped` y pasa al cierre sin tocar el código.
4. **Fase 3 — Remediación.**
   - Delega en `secfix-patcher` con los IDs confirmados.
   - Delega en `regression-qa` → `reports/REMEDIATION_SUMMARY.md`.
   - Si hay hallazgos reabiertos, repite hasta 3 veces; luego escala.
5. **Cierre obligatorio.** Ejecuta `sh {{CORE}}/sandbox/scripts/teardown.sh` y
   comprueba que imprime `teardown: OK` (sin contenedores, redes, volúmenes ni
   imágenes de PoC). Actualiza `PIPELINE_STATUS.md` y entrega un resumen con
   rutas a los reportes. Sin cierre, el pipeline queda `blocked`, no `done`.

## Reglas

- Las fases 1 y 2 no modifican código fuente; solo escriben en `reports/` y en
  los scripts del sandbox.
- No lances pruebas dinámicas fuera de Docker ni contra IPs públicas.
- Si falta Docker, bloquea la Fase 2; no improvises.
- Cada hallazgo conserva su ID (`V-NN`, `N-NN`, `W-NN`) entre fases.
- Al terminar la última fase se cierra todo: no quedan contenedores, redes,
  volúmenes ni artefactos temporales de PoC.
- **Cierre y alcance.** El análisis está listo cuando se cumplen las 7
  condiciones de `PIPELINE_ORCHESTRATOR.md` (IDs con estado final, remediación
  re-verificada, suite verde, dependencias escaneadas, `teardown: OK`, estado
  persistido y repo limpio). Si el usuario dice que está listo, se cierra: no se
  reabren fases, no se convierten observaciones en tareas, no se aplican cambios
  "de paso" ni se proponen "próximos pasos". Ampliar alcance exige petición
  explícita, registro en `PIPELINE_STATUS.md` y un gate nuevo.

## Salida

`reports/` con: `ENGAGEMENT_SCOPE.md`, `THREAT_MODEL.md`,
`SAST_RAW_FINDINGS.md`, `AUDIT_REPORT.md`, `SANDBOX_STATUS.md`,
`NETWORK_AUDIT.md`, `WEB_DAST_REPORT.md`, `PENTEST_VERIFICATION.md`,
`REMEDIATION_SUMMARY.md`, `PIPELINE_STATUS.md`.
