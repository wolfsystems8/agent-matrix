---
name: sdlc-security
description: Revisa la seguridad del ciclo de vida del software con la tríada CIA, los principios de Saltzer & Schroeder y la gestión de riesgos por fase, y aplica SQUARE o STRIDE según el estado del sistema. Usar al empezar una revisión SSDLC o al diseñar un sistema.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Seguridad en el SDLC

## Overview

Fija el marco de la revisión antes del análisis de código: activos y CIA,
principios de diseño seguro, metodología de análisis y riesgo en cada fase del
ciclo. Lo ejecutan `sdlc-security-lead`, `square-requirements` y
`threat-modeler`.

## When to use

- Al iniciar una revisión de seguridad de una aplicación.
- Cuando se diseña un sistema nuevo o faltan requisitos de seguridad.
- Cuando el usuario pregunta por CIA, Saltzer & Schroeder, SQUARE o STRIDE.

## Workflow

1. Delega en `sdlc-security-lead` → `reports/SDLC_SECURITY_REVIEW.md`:
   - Activos clasificados por Confidencialidad, Integridad y Disponibilidad.
   - Los 8 principios de Saltzer & Schroeder con estado y evidencia.
   - Metodología elegida y justificación.
   - Brechas por fase: requisitos, diseño, implementación, verificación,
     despliegue y mantenimiento.
2. Según la metodología elegida:

   | Elección | Acción |
   |----------|--------|
   | SQUARE | `square-requirements` → `reports/SECURITY_REQUIREMENTS.md` (9 pasos, casos de abuso, requisitos `SR-NN`) |
   | STRIDE | `threat-modeler` → `reports/THREAT_MODEL.md` |
   | Ambas | Primero SQUARE, luego STRIDE usando los requisitos como criterio |

3. Pasa los activos y requisitos a los analistas de código
   (`injection-xss-analysis`, `web-vuln-identification`, `crypto-review`).

## Reglas

- Solo lectura; escribe únicamente en `reports/`.
- Sin evidencia, un principio queda "Sin evidencia", no "No cumple".
- Los requisitos son verificables y no prescriben la implementación.
