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
| Cierre | orchestrator | `PIPELINE_STATUS.md` actualizado, entorno destruido | Solo lectura + `reports/` |

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

### FASE FINAL: Cierre del entorno (obligatoria)

1. Ejecutar `sh core/sandbox/scripts/teardown.sh` desde el host.
2. Exigir la línea `teardown: OK`: sin contenedores, redes ni volúmenes del
   proyecto, y sin contenedores/imágenes temporales `secmatrix-poc-*`.
3. Borrar los artefactos temporales de PoC que no gestione el script
   (`/tmp/opencode/*`, copias parcheadas, imágenes ad hoc).
4. Actualizar `reports/PIPELINE_STATUS.md` con el cierre y las rutas de los
   reportes.
5. **Gate:** sin este paso el pipeline queda `blocked`; nunca `done`.

## 🔒 Regla de cierre y control de alcance

Un análisis termina cuando se cumplen **todas** las condiciones de cierre. No
existe un "casi listo": o se cumplen, o el pipeline queda `blocked`.

### Condiciones de cierre verificables

| # | Condición | Verificación |
|---|-----------|--------------|
| 1 | Todos los IDs del alcance tienen estado final | `AUDIT_REPORT.md`: cada `V-NN`/`N-NN`/`W-NN` en `Mitigado`, `Aceptado` o `Falso positivo`; ninguno en `Pendiente` |
| 2 | Remediación re-verificada | `REMEDIATION_SUMMARY.md`: cada ID en `Cerrado`, `Parcial` o `Reabierto` con PoC o test re-ejecutado |
| 3 | Suite verde | `make check` (o el equivalente del proyecto) sin fallos ni tests omitidos |
| 4 | Dependencias escaneadas | `DEPENDENCY_SCAN.md` con fecha, herramienta y versión; 0 críticas o cada una justificada |
| 5 | Entorno destruido | `teardown.sh` imprime `teardown: OK`; 0 contenedores, 0 redes y 0 volúmenes del proyecto |
| 6 | Estado persistido | `PIPELINE_STATUS.md` con todas las filas en `done` o `skipped` con motivo |
| 7 | Repo limpio | `git status` sin cambios sin commitear y sin artefactos temporales de PoC |

Si una condición falla, el estado es `blocked` y se reporta la condición
concreta. No se declara `done` por aproximación.

### Prohibiciones al cerrar

- **No reabrir fases cerradas** sin un hallazgo nuevo reproducible y aprobación
  explícita. "Revisar por si acaso" no es un motivo.
- **No convertir observaciones en tareas.** Una nota, un falso positivo o un
  riesgo residual se documenta en el informe; no genera un TODO, un issue ni una
  fase nueva.
- **No aplicar cambios "de paso"** (refactors, renombres, estilo, bumps no
  relacionados) después de declarar el cierre. El alcance es el aprobado.
- **No proponer trabajo futuro como parte de la entrega.** Lo que quede fuera se
  registra como `Riesgo residual` o `Fuera de alcance` y se para ahí; no se
  presenta como "siguiente paso" ni como pregunta abierta.
- **No re-ejecutar el pipeline** para "confirmar" lo ya confirmado: la evidencia
  ya está en los reportes.

### Ampliación de alcance (excepción)

Solo si el usuario lo pide de forma explícita:

1. Registrar en `PIPELINE_STATUS.md` la petición, la fecha y el motivo.
2. Abrir un gate nuevo; sin aprobación, no se ejecuta.
3. Volver a la fase correspondiente y poner esa fila en `running`.
4. Al terminar, repetir las condiciones 1–7.

Un hallazgo nuevo descubierto durante el cierre **no** amplía el alcance por sí
solo: se documenta y se espera decisión.

### Formato de respuesta al cerrar

```text
Estado: done | blocked
Alcance: <IDs cubiertos>
Evidencia: <rutas a reportes + comando de verificación>
Cierre: teardown: OK (0 contenedores / 0 redes / 0 volúmenes)
Fuera de alcance: <nada | lista>
```

Sin secciones de "próximos pasos" ni preguntas que impliquen trabajo nuevo.

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
