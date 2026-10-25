---
description: "Ejecuta la Fase 3: parchea hallazgos confirmados y valida con tests y PoCs."
---

# /sec-fix — Remediación y QA

Objetivo: `$ARGUMENTS` (por defecto, los hallazgos confirmados del informe).

Precondición: `reports/PENTEST_VERIFICATION.md` con hallazgos **Confirmado** y
autorización explícita para modificar código. Si no existe, detente.

Sigue las skills `security-remediation` y `security-regression-qa`:

1. `secfix-patcher` aplica parches mínimos por hallazgo confirmado.
2. Añade/actualiza un test de regresión por hallazgo.
3. Ejecuta tests, lint, typecheck y build.
4. `regression-qa` re-ejecuta las PoCs en el sandbox y emite
   `reports/REMEDIATION_SUMMARY.md`.
5. Si un hallazgo se reabre, itera (máx. 3) o escala al usuario.

No toques código no relacionado. No silencies analizadores ni elimines tests.
