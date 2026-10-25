---
description: "Ejecuta la Fase 1 (SSDLC) sobre el repositorio: threat model, SAST y triage con CVSS."
argument-hint: "[target]"
---

# /sec-audit — Análisis estático y modelo de amenazas

Objetivo: `$ARGUMENTS` (por defecto, el repositorio actual).

Sigue la skill `security-audit-pipeline` limitada a la **Fase 0 y Fase 1**:

1. Crea `reports/ENGAGEMENT_SCOPE.md` si no existe. Si el alcance no está claro,
   pregunta antes de continuar.
2. Delega en `threat-modeler` → `reports/THREAT_MODEL.md`.
3. Delega en `sast-auditor` → `reports/SAST_RAW_FINDINGS.md`.
4. Delega en `triage-master` → `reports/AUDIT_REPORT.md` con CVSS v3.1.
5. Actualiza `reports/PIPELINE_STATUS.md`.

No modifiques código fuente. No ejecutes pruebas dinámicas. Al terminar,
presenta el conteo por severidad y los 5 hallazgos principales, y **detente**
pidiendo aprobación para la Fase 2.
