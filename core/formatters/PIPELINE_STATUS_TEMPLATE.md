# Estado del pipeline

| Fase | Agente | Estado | Artefacto | Timestamp | Notas |
|------|--------|--------|-----------|-----------|-------|
| 0 | orchestrator | pending | `reports/ENGAGEMENT_SCOPE.md` | | |
| 1 | audit-program-lead | pending | `reports/AUDIT_PLAN.md` | | |
| 1 | threat-modeler | pending | `reports/THREAT_MODEL.md` | | |
| 1 | sast-auditor | pending | `reports/SAST_RAW_FINDINGS.md` | | |
| 1 | triage-master | pending | `reports/AUDIT_REPORT.md` | | |
| 1 | itil-process-auditor | pending | `reports/ITIL_PROCESS_AUDIT.md` | | |
| 1 | risk-assessor | pending | `reports/RISK_REGISTER.md` | | |
| — | **GATE 1** | pending | Aprobación del usuario | | |
| 2 | sandbox-manager | pending | `reports/SANDBOX_STATUS.md` | | |
| 2 | network-auditor | pending | `reports/NETWORK_AUDIT.md` | | |
| 2 | web-dast-tester | pending | `reports/WEB_DAST_REPORT.md` | | |
| 2 | exploit-tester | pending | `reports/PENTEST_VERIFICATION.md` | | |
| — | audit-program-lead | pending | `reports/ISO19011_AUDIT_REPORT.md` | | |
| — | **GATE 2** | pending | ¿Corregir? sí/no + IDs | | |
| 3 | secfix-patcher | pending | Código modificado | | |
| 3 | regression-qa | pending | `reports/REMEDIATION_SUMMARY.md` | | |

Estados: `pending`, `running`, `blocked`, `done`, `failed`, `skipped` (con motivo).

## Bloqueos y decisiones

| Fecha | Fase | Motivo | Decisión |
|-------|------|--------|----------|
| | | | |
