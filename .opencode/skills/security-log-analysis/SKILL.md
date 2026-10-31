---
name: security-log-analysis
description: "Evalúa la cobertura de logs de autenticación, aplicación, red, servidor web y sistema operativo, su calidad (sin datos sensibles ni inyección) y detecta indicadores de ataque en logs del alcance. Usar en análisis de seguridad y detección."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Análisis de seguridad de logs

## Overview

Comprueba que el sistema puede detectar e investigar un ataque y, si hay logs
disponibles, busca indicadores. Lo ejecuta `log-auditor` →
`reports/LOG_AUDIT.md`.

## When to use

- En una auditoría que evalúa detección y respuesta.
- Tras la Fase 2, con los logs del sandbox exportados a `reports/logs/`.
- Cuando el usuario aporta logs dentro del alcance autorizado.

## Workflow

1. **Cobertura** por fuente: autenticación, aplicación, red, servidor web y
   sistema operativo.
2. **Calidad:** formato estructurado, marcas de tiempo, correlación, sin
   secretos ni PII (CWE-532), sin inyección de logs (CWE-117), retención.
3. **Indicadores:** fuerza bruta, escaneo, SQLi/XSS en URLs, path traversal,
   escalada en el SO; cada uno con la línea del log como evidencia.
4. Relaciona cada indicador con los hallazgos `V-NN`/`W-NN` existentes.

## Reglas

- Solo logs dentro del alcance; enmascara datos personales.
- Solo lectura; escribe únicamente en `reports/`.
