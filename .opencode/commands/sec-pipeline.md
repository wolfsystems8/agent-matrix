---
description: "Ejecuta el pipeline completo de auditoría con gates humanos entre las tres fases."
---

# /sec-pipeline — Auditoría completa con gates

Objetivo: `$ARGUMENTS` (por defecto, el repositorio actual).

Ejecuta `security-audit-pipeline` de principio a fin, respetando los gates:

1. **Fase 0:** alcance y autorización en `reports/ENGAGEMENT_SCOPE.md`.
2. **Fase 1:** `threat-modeler` → `sast-auditor` → `triage-master`.
   **GATE 1:** pide aprobación.
3. **Fase 2:** `sandbox-manager` → `network-auditor` → `web-dast-tester` →
   `exploit-tester`.
   **GATE 2:** pide autorización para parchear.
4. **Fase 3:** `secfix-patcher` → `regression-qa`.
5. **Cierre:** ejecuta `sh core/sandbox/scripts/teardown.sh` (exige
   `teardown: OK`: sin contenedores, redes, volúmenes ni PoC temporales), resume
   hallazgos cerrados/parciales/reabiertos y enlaza todos los reportes.

No avances de fase sin aprobación explícita. Si detectas una condición de parada
del orquestador, detente y explícala.
