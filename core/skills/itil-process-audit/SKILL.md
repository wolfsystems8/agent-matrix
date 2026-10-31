---
name: itil-process-audit
description: Audita prácticas operativas de ITIL 4 (cambios, despliegue, configuración, activos, incidentes, monitorización, accesos, continuidad) con evidencia del repositorio y nivel de madurez. Usar cuando hay CI/CD, IaC o documentación operativa.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Auditoría de procesos con ITIL 4

## Overview

Evalúa si las prácticas de gestión de servicios que protegen la tríada CIA
están implementadas, con un nivel de madurez de 1 a 5 y hallazgos `P-NN`. El
detalle operativo está en el agente `itil-process-auditor`.

## When to use

- El repositorio tiene pipelines, IaC, contenedores o documentación operativa.
- El usuario pregunta por gestión de cambios, despliegues, incidentes o
  continuidad dentro de una auditoría.
- No usar para buscar vulnerabilidades en el código (usa `sast-code-audit`).

## Workflow

1. Localiza la evidencia: workflows de CI, `CODEOWNERS`, IaC, `Dockerfile`,
   lockfiles, `SECURITY.md`, `CHANGELOG`, runbooks, configuración de logs.
2. Recorre las prácticas: habilitación del cambio, entrega y despliegue,
   configuración, activos de TI, incidentes, problemas, monitorización y
   eventos, seguridad de la información, accesos y continuidad.
3. Asigna madurez (1 inicial · 2 repetible · 3 definida · 4 gestionada ·
   5 optimizada) con archivo y línea como evidencia.
4. Emite un `P-NN` por práctica con madurez ≤ 2 o con un control de seguridad
   ausente, con su impacto CIA y una recomendación concreta.
5. Escribe `reports/ITIL_PROCESS_AUDIT.md`.

## Reglas

- Lo que no está en el repositorio se marca "sin evidencia", no "incumple".
- No modifiques pipelines ni configuración.
- Escribe únicamente en `reports/`.
