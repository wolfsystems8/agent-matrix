---
name: security-remediation
description: Aplica parches mínimos y seguros a hallazgos confirmados, con tests de regresión. Usar tras la autorización de la Fase 3 para corregir vulnerabilidades sin cambiar la funcionalidad.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 3
  authority: write
---

# Security Remediation

## Overview

Corrige vulnerabilidades confirmadas con el mínimo cambio necesario y evidencia
de que el comportamiento esperado se mantiene. El catálogo de patrones seguros
está en el agente `secfix-patcher`.

## When to use

- `PENTEST_VERIFICATION.md` contiene hallazgos **Confirmado**.
- El usuario autorizó explícitamente modificar código.
- No usar para refactors estéticos ni para hallazgos no verificados.

## Workflow

1. Selecciona solo hallazgos confirmados, ordenados por severidad.
2. Lee el flujo completo y localiza el test que cubre el comportamiento.
3. Aplica el patrón seguro correspondiente:
   - SQL/NoSQL → consultas preparadas.
   - Comandos → sin shell, allowlist de argumentos.
   - XSS → escape contextual + CSP.
   - Entradas → validación por esquema.
   - Secretos → variables de entorno + rotación.
   - Contraseñas → Argon2id/bcrypt.
   - Autorización → comprobar propiedad y rol en cada acceso.
   - Sesión → cookies seguras, JWT con algoritmo fijado.
4. Añade o actualiza un test que falle antes y pase después.
5. Ejecuta tests, lint, typecheck y build.
6. Registra el cambio en `reports/REMEDIATION_SUMMARY.md`.

## Salida

Código parcheado + tabla de cambios en `REMEDIATION_SUMMARY.md`.

## Reglas

- Un hallazgo por cambio, sin refactors no relacionados.
- No silencies analizadores (`@ts-ignore`, `# noqa`, `eslint-disable`).
- No elimines ni debilites tests.
- Si el parche cambia un contrato público, documenta la migración.
