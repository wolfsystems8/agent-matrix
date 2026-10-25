---
name: security-regression-qa
description: Verifica que los parches cierran las vulnerabilidades y no rompen la aplicación, re-ejecutando tests y PoCs. Usar al final de la remediación para emitir el informe de cierre.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 3
  authority: write
---

# Security Regression QA

## Overview

Cierra el ciclo: ejecuta la suite, re-valida las PoCs en el sandbox y emite
`reports/REMEDIATION_SUMMARY.md` con el estado final de cada hallazgo. El
procedimiento detallado está en el agente `regression-qa`.

## When to use

- Se aplicaron parches de seguridad y hay que verificar que funcionan.
- Antes de declarar una auditoría terminada o abrir un PR de seguridad.
- Cuando una PoC debe dejar de reproducirse.

## Workflow

1. Ejecuta la suite del proyecto (`npm test`, `pytest`, `go test ./...`).
2. Ejecuta lint, typecheck y build si existen.
3. Re-ejecuta cada `poc_<id>` en el sandbox y compara antes/después.
4. Prueba los flujos críticos afectados (login, permisos, pagos, uploads).
5. Marca cada hallazgo: Cerrado, Parcial o Reabierto.
6. Si hay reabiertos, vuelve a `security-remediation` (máx. 3 iteraciones).
7. Destruye el sandbox y documenta el entorno usado.

## Salida

`reports/REMEDIATION_SUMMARY.md`.

## Reglas

- Sin re-ejecución no hay cierre.
- No adaptes tests para ocultar un fallo real.
- Si no puedes ejecutar algo, dilo; no asumas éxito.
- No dejes contenedores ni volúmenes del sandbox en ejecución.
