---
description: "Auditoría de sistemas ISO 19011 con riesgos ISO 27005, procesos ITIL 4 y subagentes elegidos en automático."
argument-hint: "[target]"
---

# /sec-iso-audit — Auditoría de sistemas (ISO 19011)

Objetivo: `$ARGUMENTS` (por defecto, el repositorio actual).

Sigue la skill `iso-audit-lifecycle`:

1. Exige `reports/ENGAGEMENT_SCOPE.md`. Si el alcance no está claro, pregunta
   antes de continuar.
2. Delega en `audit-program-lead` → `reports/AUDIT_PLAN.md` con el mapa de
   cobertura.
3. Ejecuta en automático los agentes de Fase 1 marcados `Sí` y marca el resto
   `skipped` con su motivo en `reports/PIPELINE_STATUS.md`.
4. Delega en `risk-assessor` → `reports/RISK_REGISTER.md` ordenado por
   severidad.
5. Presenta el conteo por nivel y el top 5 de riesgos y **detente**: pide
   aprobación para la Fase 2 si el plan la requiere.

No modifiques código fuente ni lo copies. La corrección solo ocurre tras un
"sí" explícito en el gate de remediación.
