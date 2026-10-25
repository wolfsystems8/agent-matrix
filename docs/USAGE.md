# Guía de uso

## 1. Preparar el alcance (Fase 0)

Copia la plantilla y complétala:

```bash
cp core/formatters/ENGAGEMENT_SCOPE_TEMPLATE.md reports/ENGAGEMENT_SCOPE.md
```

Debe incluir: propietario, repositorio, entorno, ventana de pruebas, contacto y
una frase explícita de autorización. Sin este archivo, ningún agente ejecuta
pruebas dinámicas.

Crea también el estado del pipeline:

```bash
cp core/formatters/PIPELINE_STATUS_TEMPLATE.md reports/PIPELINE_STATUS.md
```

## 2. Fase 1 — Análisis estático

### Claude Code / Cursor / OpenCode

```text
/sec-audit
```

o, paso a paso:

```text
Usa el subagente threat-modeler sobre este repositorio.
Usa el subagente sast-auditor y limita el análisis a src/ y api/.
Usa el subagente triage-master para consolidar los dos reportes.
```

### Codex

```text
Usa la skill $security-audit-pipeline limitada a la Fase 0 y Fase 1.
Lanza el subagente threat-modeler, luego sast-auditor y luego triage-master.
```

### Resultado esperado

- `reports/THREAT_MODEL.md`
- `reports/SAST_RAW_FINDINGS.md`
- `reports/AUDIT_REPORT.md`

**Gate 1:** revisa el conteo por severidad y los 5 hallazgos principales. No
continúes sin aprobar.

## 3. Fase 2 — Sandbox

### Requisitos

- Docker + Compose v2.
- Opcional: la app auditada con `Dockerfile` y escuchando en `:8080` (o ajusta
  `TARGET_PORT` y la URL base de los agentes). Sin `TARGET_CONTEXT` se usa
  `demo-target`, el objetivo vulnerable de demostración incluido en el sandbox.

### Ejecución

```text
/sec-pentest
```

El flujo es:

1. `sandbox-manager`: `up -d --build`, verifica `Internal: true` y
   `EGRESS_BLOCKED`.
2. `network-auditor`: puertos, servicios, TLS, certificados.
3. `web-dast-tester`: cabeceras, CORS, cookies, rutas, BOLA, mass assignment.
4. `exploit-tester`: PoCs mínimas y estado por hallazgo.

**Gate 2:** revisa `PENTEST_VERIFICATION.md`. Solo los hallazgos `Confirmado`
pasan a la Fase 3.

### Prueba manual del aislamiento

```bash
docker network inspect sec-agent-matrix_sandbox_net --format '{{.Internal}}'
docker compose -f core/sandbox/docker-compose.sandbox.yml \
  exec -T pentest-runner sh -lc '/scripts/smoke_test.sh'
```

Si `smoke_test.sh` imprime `EGRESS_OPEN`, destruye el entorno y no continúes.

## 4. Fase 3 — Remediación

```text
/sec-fix
```

O por hallazgo:

```text
Usa secfix-patcher para corregir V-01 y V-03. Añade un test de regresión por cada uno.
Después usa regression-qa y re-ejecuta las PoCs en el sandbox.
```

### Criterios de cierre

- Tests, lint, typecheck y build en verde.
- Cada PoC confirmada deja de reproducirse.
- `REMEDIATION_SUMMARY.md` marca Cerrado / Parcial / Reabierto con evidencia.
- Sandbox cerrado: `sh core/sandbox/scripts/teardown.sh` imprime
  `teardown: OK` (sin contenedores, redes, volúmenes ni PoC temporales).

## 5. Pipeline completo

```text
/sec-pipeline
```

Respeta los dos gates. Si una condición de parada se cumple (egreso, Docker
ausente, falta de autorización), el orquestador se detiene y lo explica.

## 6. Prompts útiles

```text
# Acotar el SAST
Usa sast-auditor solo en src/auth/ y src/api/. No analices node_modules.

# Priorizar
Usa triage-master y ordéname los hallazgos por CVSS y facilidad de explotación.

# DAST dirigido
Usa web-dast-tester para comprobar BOLA en /api/orders/{id} con las cuentas de prueba.

# Parche mínimo
Usa secfix-patcher para V-02. No cambies el contrato de la API.

# Verificación
Usa regression-qa. Si una PoC sigue pasando, reabre el hallazgo y explica por qué.
```

## 7. Solución de problemas

| Síntoma | Causa probable | Acción |
|---------|----------------|--------|
| Un agente no aparece | Adaptadores no regenerados | `python3 tools/secmatrix.py build` y reinicia el host si hace falta |
| Codex no ve la skill | Ruta incorrecta | Debe estar en `.agents/skills/<id>/SKILL.md` |
| OpenCode no aplica permisos | Regla de ruta no coincide | Ajusta `reports/**` al cwd real |
| `validate` falla por drift | Editaste un adaptador | Edita `core/` y ejecuta `build` |
| Fase 2 bloqueada | Docker ausente o egreso abierto | Instala Docker / corrige la red; no improvises |
| El puerto 8080 está ocupado | Otro servicio local | Cambia `TARGET_PORT` y la URL base de los agentes |

## 8. Buenas prácticas

- Ejecuta cada fase en una rama o worktree distinto.
- Revisa el diff de la Fase 3 antes de hacer commit.
- No pegues secretos reales en los reportes.
- Conserva los reportes como evidencia de la auditoría.
- Revisa la directiva ética antes de cada engagement.
