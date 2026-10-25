# Reportes de auditoría

Este directorio es el único destino de escritura permitido para los agentes de
las Fases 1 y 2. Los archivos se generan durante el pipeline:

| Archivo | Fase | Agente |
|---------|------|--------|
| `ENGAGEMENT_SCOPE.md` | 0 | Orquestador |
| `THREAT_MODEL.md` | 1 | `threat-modeler` |
| `SAST_RAW_FINDINGS.md` | 1 | `sast-auditor` |
| `AUDIT_REPORT.md` | 1 | `triage-master` |
| `SANDBOX_STATUS.md` | 2 | `sandbox-manager` |
| `NETWORK_AUDIT.md` | 2 | `network-auditor` |
| `WEB_DAST_REPORT.md` | 2 | `web-dast-tester` |
| `PENTEST_VERIFICATION.md` | 2 | `exploit-tester` |
| `REMEDIATION_SUMMARY.md` | 3 | `regression-qa` |
| `PIPELINE_STATUS.md` | 0–3 | Orquestador |
| `GUARDRAIL_LOG.md` | 0–3 | Cualquier agente |

## Reglas

- No incluir secretos, tokens ni PII sin enmascarar.
- Un hallazgo por ID estable (`V-NN`, `N-NN`, `W-NN`).
- Todo hallazgo confirmado debe incluir evidencia reproducible.
- Los reportes no se sobrescriben entre ejecuciones: usa el estado del pipeline
  y conserva el histórico si es necesario.
