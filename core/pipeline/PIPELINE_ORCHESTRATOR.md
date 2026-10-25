# Master Pipeline Orchestrator

## 🎯 Objetivo

Coordinar la secuencia de auditoría estática, verificación dinámica y
remediación de código en tres fases aisladas, con puntos de control humanos
entre fases. Ninguna fase se salta y ninguna fase escribe fuera de su autoridad.

## 📋 Artefactos por fase

| Fase | Agentes | Artefactos de salida | Autoridad |
|------|---------|----------------------|-----------|
| 1 — SSDLC | `threat-modeler` → `sast-auditor` → `triage-master` | `THREAT_MODEL.md`, `SAST_RAW_FINDINGS.md`, `AUDIT_REPORT.md` | Solo lectura + `reports/` |
| 2 — Pentest | `sandbox-manager` → `network-auditor` → `web-dast-tester` → `exploit-tester` | `SANDBOX_STATUS.md`, `NETWORK_AUDIT.md`, `WEB_DAST_REPORT.md`, `PENTEST_VERIFICATION.md` | Solo lectura + `reports/` + scripts de sandbox |
| 3 — Remediación | `secfix-patcher` → `regression-qa` | Código parcheado, `REMEDIATION_SUMMARY.md` | Escritura de código |

## 🔄 Flujo de Trabajo Secuencial

### FASE 0: Alcance y autorización (obligatoria)

1. Confirmar con el usuario: repositorio, propietario, entorno y ventana.
2. Crear `reports/ENGAGEMENT_SCOPE.md` con el alcance autorizado y la
   declaración de que no se probarán sistemas de terceros.
3. Verificar que existe `core/ethics/ETHICAL_DIRECTIVE.md` y que se ha leído.
4. **Gate:** sin alcance escrito no se avanza.

### FASE 1: Análisis Estático y Modelo de Amenazas (Solo Lectura)

1. Invocar `threat-modeler` ➔ genera `reports/THREAT_MODEL.md`.
2. Invocar `sast-auditor` ➔ genera `reports/SAST_RAW_FINDINGS.md`.
3. Invocar `triage-master` ➔ consolida `reports/AUDIT_REPORT.md` con CVSS v3.1.
4. **Punto de Control:** presentar el resumen ejecutivo (conteo por severidad y
   top 5 hallazgos) y requerir aprobación del usuario antes de la Fase 2.

### FASE 2: Verificación Dinámica en Sandbox (Entorno Aislado)

1. Invocar `sandbox-manager` ➔ despliega `docker-compose.sandbox.yml`, verifica
   aislamiento de red y genera `reports/SANDBOX_STATUS.md`.
2. Invocar `network-auditor` ➔ escanea puertos, servicios y TLS ➔ genera
   `reports/NETWORK_AUDIT.md`.
3. Invocar `web-dast-tester` ➔ audita cabeceras, CORS, cookies y endpoints API
   ➔ genera `reports/WEB_DAST_REPORT.md`.
4. Invocar `exploit-tester` ➔ ejecuta PoCs mínimas para validar los hallazgos
   del SAST, la red y el DAST ➔ consolida `reports/PENTEST_VERIFICATION.md`.
5. **Punto de Control:** mostrar hallazgos confirmados y solicitar autorización
   explícita para parchear.

### FASE 3: Remediación y QA (Escritura Habilitada)

1. Invocar `secfix-patcher` ➔ aplica correcciones mínimas sobre los hallazgos
   confirmados y registra cada cambio.
2. Invocar `regression-qa` ➔ ejecuta pruebas unitarias/integración y re-ejecuta
   las PoCs ➔ emite `reports/REMEDIATION_SUMMARY.md`.
3. Si una PoC sigue pasando, reabrir el hallazgo y volver al paso 1 (máximo 3
   iteraciones antes de escalar al usuario).

## 🛑 Reglas de Parada

- Objetivo fuera de `sandbox_net` o IP pública resuelta ➔ detener y registrar.
- Docker no disponible ➔ detener la Fase 2, no improvisar pruebas locales.
- Falta de autorización en un gate ➔ detener la fase siguiente.
- Cualquier intento de escritura en código durante Fase 1/2 ➔ bloquear.
- Resultado destructivo o pérdida de datos ➔ detener todo y reportar.

## 📊 Estado del pipeline

Mantener `reports/PIPELINE_STATUS.md` con una tabla:

| Fase | Agente | Estado | Artefacto | Timestamp |
|------|--------|--------|-----------|-----------|
| 1 | threat-modeler | ✅ done | `reports/THREAT_MODEL.md` | 2026-01-01T10:00Z |

Estados permitidos: `pending`, `running`, `blocked`, `done`, `failed`.
