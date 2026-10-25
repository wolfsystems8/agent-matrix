---
name: sast-code-audit
description: Audita código fuente en busca de inyecciones, secretos, criptografía débil y fallos de autorización, con archivo y línea. Usar para revisar un repositorio sin ejecutarlo o antes de un pentest.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# SAST Code Audit

## Overview

Revisión estática guiada por OWASP Top 10, CWE y ASVS. Genera
`reports/SAST_RAW_FINDINGS.md` con evidencia verificable y remediación concreta.
El checklist completo vive en el agente `sast-auditor`.

## When to use

- El usuario pide "revisar el código en busca de vulnerabilidades".
- Hay que evaluar un PR o un módulo sensible (auth, pagos, uploads, SQL).
- Antes de la Fase 2 para dirigir las PoCs.

## Workflow

1. Identifica stack, framework y puntos de entrada.
2. Revisa en este orden: consultas a datos, ejecución de comandos, renderizado
   HTML, autenticación/sesión, autorización, uploads, criptografía y secretos.
3. Para cada candidato, traza el flujo source → sink y comprueba si existe
   validación o sanitización efectiva.
4. Ejecuta herramientas disponibles en modo lectura (`semgrep`, `bandit`,
   `npm audit`, `gosec`) y adjunta el comando.
5. Descarta falsos positivos con justificación; no los borres sin rastro.
6. Escribe la tabla de hallazgos con ID `S-NN`, CWE, confianza y remediación.

## Salida

`reports/SAST_RAW_FINDINGS.md`.

## Reglas

- No modifiques código ni ejecutes la aplicación.
- No reportes sin archivo y línea.
- Enmascara secretos; reporta ubicación, no valor.
- Un patrón peligroso sin flujo explotable se marca como "requiere revisión".
