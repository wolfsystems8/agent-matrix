# sec-agent-matrix

Matriz de agentes y skills de seguridad ofensiva **defensiva** para ejecutar un
pipeline SSDLC → Pentest en sandbox → Remediación, con el mismo contenido en
**Claude Code, Cursor, Codex y OpenCode**.

- **9 agentes especializados** (threat modeling, SAST, triage CVSS, sandbox,
  red/TLS, DAST web/API, explotación ética, parcheo y QA).
- **9 skills portables** que orquestan el flujo y funcionan en cualquiera de las
  cuatro herramientas.
- **Fuente única** en `core/`: editas una vez y `secmatrix build` genera los
  formatos nativos de cada host.
- **Guardrails reales**: sandbox Docker con red interna, gates humanos y fases de
  solo lectura.

> ⚠️ **Uso autorizado únicamente.** Este proyecto está diseñado para auditar
> sistemas propios o con autorización escrita, dentro de un sandbox aislado.
> Lee [`core/ethics/ETHICAL_DIRECTIVE.md`](core/ethics/ETHICAL_DIRECTIVE.md).

---

## Índice

1. [Arquitectura](#arquitectura)
2. [Requisitos](#requisitos)
3. [Inicio rápido](#inicio-rápido)
4. [Instalar en otro proyecto](#instalar-en-otro-proyecto)
5. [Uso por herramienta](#uso-por-herramienta)
6. [Pipeline](#pipeline)
7. [Agentes](#agentes)
8. [Skills](#skills)
9. [Sandbox](#sandbox)
10. [Toolchain](#toolchain)
11. [Estructura del repositorio](#estructura-del-repositorio)
12. [Desarrollo](#desarrollo)
13. [Limitaciones conocidas](#limitaciones-conocidas)
14. [Licencia](#licencia)

---

## Arquitectura

```text
core/                        ← fuente única (editar aquí)
├── agents/                  ← 9 agentes con frontmatter neutro
├── skills/                  ← 9 skills (SKILL.md estándar)
├── commands/                ← 4 comandos /sec-*
├── ethics/                  ← guardrails globales
├── pipeline/                ← orquestador de 3 fases
├── formatters/              ← plantillas de reportes
└── sandbox/                 ← docker-compose + runner + scripts

tools/secmatrix.py           ← build / validate / install / doctor
        │
        ├── .claude/agents/*.md          + .claude/skills/ + .claude/commands/
        ├── .cursor/agents/*.md          + .cursor/skills/ + .cursor/commands/ + .cursor/rules/
        ├── .codex/agents/*.toml         + .agents/skills/  (Codex)
        └── .opencode/agents/*.md        + .opencode/skills/ + .opencode/commands/
```

Los adaptadores se versionan para que el repositorio sea *drop-in*: copiarlo (o
instalarlo) ya deja las cuatro herramientas configuradas. El manifiesto
`.secmatrix-manifest.json` guarda hashes para detectar ediciones manuales y
deriva.

## Requisitos

| Componente | Versión | Uso |
|------------|---------|-----|
| Python | 3.9+ (3.11+ para tests) | Toolchain |
| Git | cualquiera | Versionado |
| Docker + Compose v2 | reciente | **Solo Fase 2** (sandbox) |
| Claude Code / Cursor / Codex / OpenCode | recientes | Host del agente |

Sin Docker puedes ejecutar las Fases 1 y 3; la Fase 2 se bloquea de forma
explícita (no se improvisan pruebas fuera del sandbox).

## Inicio rápido

```bash
cd sec-agent-matrix

# 1. Verifica el entorno
python3 tools/secmatrix.py doctor

# 2. Regenera y valida los adaptadores
python3 tools/secmatrix.py build
python3 tools/secmatrix.py validate

# 3. Abre el repositorio con tu herramienta y lanza:
#    Claude Code / Cursor / OpenCode → /sec-audit
#    Codex → "usa la skill $security-audit-pipeline en modo Fase 1"
```

Antes de la primera ejecución crea el alcance:

```bash
cp core/formatters/ENGAGEMENT_SCOPE_TEMPLATE.md reports/ENGAGEMENT_SCOPE.md
```

## Instalar en otro proyecto

```bash
python3 tools/secmatrix.py install --target ../mi-app
```

El instalador:

1. Copia la fuente canónica a `../mi-app/.sec-agent-matrix/core/`.
2. Genera los adaptadores nativos con las rutas reescritas.
3. Crea `reports/` con su README.
4. Añade un bloque gestionado a `AGENTS.md` y `CLAUDE.md` (idempotente).

Opciones:

```bash
--tools claude,cursor          # instalar solo algunos hosts
--dry-run                      # ver qué se escribiría
--force                        # sobrescribir archivos no gestionados
--prune                        # borrar adaptadores obsoletos
--no-rules                     # no tocar AGENTS.md / CLAUDE.md
```

Ejemplo de prompt tras instalar en Claude Code:

```text
/sec-audit
```

## Uso por herramienta

| Herramienta | Agentes | Skills | Comandos | Invocación |
|-------------|---------|--------|----------|------------|
| **Claude Code** | `.claude/agents/*.md` | `.claude/skills/` | `.claude/commands/` | `/sec-audit`, delegación automática por `description` |
| **Cursor** | `.cursor/agents/*.md` | `.cursor/skills/` + `.agents/skills/` | `.cursor/commands/` | `/sec-audit`, `/threat-modeler` |
| **Codex** | `.codex/agents/*.toml` | `.agents/skills/` | — (usar skills) | `$security-audit-pipeline`, pedir subagente `threat-modeler` |
| **OpenCode** | `.opencode/agents/*.md` | `.opencode/skills/` + `.claude/skills/` + `.agents/skills/` | `.opencode/commands/` | `/sec-audit`, `@security-audit-pipeline` |

Detalles, formatos y limitaciones: [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md).

## Pipeline

| Fase | Agentes | Salidas | Escritura |
|------|---------|---------|-----------|
| **0. Alcance** | Orquestador | `ENGAGEMENT_SCOPE.md`, `PIPELINE_STATUS.md` | `reports/` |
| **1. SSDLC** | `threat-modeler` → `sast-auditor` → `triage-master` | `THREAT_MODEL.md`, `SAST_RAW_FINDINGS.md`, `AUDIT_REPORT.md` | Solo `reports/` |
| **2. Pentest** | `sandbox-manager` → `network-auditor` → `web-dast-tester` → `exploit-tester` | `SANDBOX_STATUS.md`, `NETWORK_AUDIT.md`, `WEB_DAST_REPORT.md`, `PENTEST_VERIFICATION.md` | Solo `reports/` + scripts sandbox |
| **3. Remediación** | `secfix-patcher` → `regression-qa` | Código parcheado, `REMEDIATION_SUMMARY.md` | Código permitido |

Gates obligatorios:

- **Gate 1:** aprobación tras el informe de la Fase 1.
- **Gate 2:** autorización explícita para parchear tras la Fase 2.

Reglas de parada y condiciones de bloqueo:
[`core/pipeline/PIPELINE_ORCHESTRATOR.md`](core/pipeline/PIPELINE_ORCHESTRATOR.md).

## Agentes

| ID | Fase | Autoridad | Salida |
|----|------|-----------|--------|
| `threat-modeler` | 1 | read-only | `THREAT_MODEL.md` |
| `sast-auditor` | 1 | read-only | `SAST_RAW_FINDINGS.md` |
| `triage-master` | 1 | read-only | `AUDIT_REPORT.md` |
| `sandbox-manager` | 2 | sandbox | `SANDBOX_STATUS.md` |
| `network-auditor` | 2 | sandbox | `NETWORK_AUDIT.md` |
| `web-dast-tester` | 2 | sandbox | `WEB_DAST_REPORT.md` |
| `exploit-tester` | 2 | sandbox | `PENTEST_VERIFICATION.md` |
| `secfix-patcher` | 3 | write | Código + cambios |
| `regression-qa` | 3 | write | `REMEDIATION_SUMMARY.md` |

`read-only` y `sandbox` solo pueden escribir en `reports/`; `write` puede editar
código. En OpenCode esto se aplica con permisos por acción y ruta; en Claude con
la lista `tools`; en Cursor y Codex con instrucciones y el gate humano.

## Skills

| Skill | Cuándo usarla |
|-------|---------------|
| `security-audit-pipeline` | Auditoría completa con gates |
| `threat-modeling` | STRIDE sobre arquitectura |
| `sast-code-audit` | Revisión estática con CWE/ASVS |
| `vulnerability-triage` | Consolidar y puntuar CVSS v3.1 |
| `sandbox-pentest` | Fase 2 completa |
| `network-tls-audit` | Puertos, servicios, TLS |
| `web-api-dast` | Cabeceras, CORS, cookies, API |
| `security-remediation` | Parches mínimos |
| `security-regression-qa` | Tests + re-PoC + cierre |

## Sandbox

```bash
# Arrancar: por defecto levanta demo-target (app vulnerable de demostración)
docker compose -f core/sandbox/docker-compose.sandbox.yml up -d --build

# Verificar aislamiento
docker network inspect sec-agent-matrix_sandbox_net --format '{{.Internal}}'   # true
docker compose -f core/sandbox/docker-compose.sandbox.yml \
  exec -T pentest-runner sh -lc '/scripts/smoke_test.sh'                      # EGRESS_BLOCKED

# Destruir
docker compose -f core/sandbox/docker-compose.sandbox.yml down -v
```

Para auditar una app propia, define `TARGET_CONTEXT` (y `TARGET_DOCKERFILE` /
`TARGET_PORT` si aplica) en `core/sandbox/.env`: la app debe exponer `:8080`.

Características: red `internal: true`, objetivo expuesto solo en `127.0.0.1` a
través del proxy `target-edge` (socat), `no-new-privileges`, `cap_drop: ALL` +
`NET_RAW` solo en el runner, y un `Dockerfile.pentest` con `nmap`, `sslyze`,
`curl`, `openssl` y `nc`.

Variables: `TARGET_CONTEXT` (default `./demo-target`), `TARGET_DOCKERFILE`,
`TARGET_PORT`, `REPORTS_DIR`. Ver
[`core/sandbox/README.md`](core/sandbox/README.md).

## Toolchain

```bash
python3 tools/secmatrix.py build      # genera adaptadores + manifiesto
python3 tools/secmatrix.py validate   # estructura, duplicados, drift
python3 tools/secmatrix.py install --target ../proyecto
python3 tools/secmatrix.py list       # agentes y skills
python3 tools/secmatrix.py doctor     # docker, git, adaptadores
python3 tools/secmatrix.py clean      # elimina adaptadores generados
```

`build` es determinista: mismos fuentes → mismos bytes → mismo hash. CI falla si
hay deriva.

## Estructura del repositorio

```text
sec-agent-matrix/
├── core/                       ← fuente única
│   ├── agents/01-ssdlc/        ← 3 agentes
│   ├── agents/02-pentest/      ← 4 agentes
│   ├── agents/03-remediation/  ← 2 agentes
│   ├── skills/                 ← 9 skills portables
│   ├── commands/               ← 4 comandos
│   ├── ethics/                 ← directiva global
│   ├── pipeline/               ← orquestador
│   ├── formatters/             ← plantillas
│   └── sandbox/                ← compose, runner, scripts
├── tools/secmatrix.py          ← generador/instalador/validador
├── tests/                      ← unittest (sin dependencias)
├── docs/                       ← arquitectura, compatibilidad, uso
├── reports/                    ← salida de auditorías
├── .claude/ .cursor/ .codex/ .agents/ .opencode/   ← generados
├── AGENTS.md CLAUDE.md
└── .github/workflows/ci.yml
```

## Desarrollo

```bash
make check     # build + validate + tests
make test
```

Reglas:

- Edita **solo** `core/`; nunca los adaptadores generados.
- Añadir un agente: crea `core/agents/<fase>/<orden>-<id>.md` con el frontmatter
  (`id`, `description`, `phase`, `authority`, `tools`, `order`) y ejecuta
  `build`.
- Añadir una skill: `core/skills/<id>/SKILL.md` con `name` igual al directorio.
- Añadir un comando: `core/commands/<nombre>.md` con `description` y `phase`.
- Actualiza los tests si cambia el número de artefactos.

Más detalle: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) y
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Limitaciones conocidas

1. **Docker no está instalado en este entorno de desarrollo.** El sandbox está
   completo pero la Fase 2 no se puede ejecutar hasta instalarlo.
2. **Cursor no permite restringir escrituras por ruta** en subagentes; el límite
   de `reports/` es instruccional y se refuerza con el gate humano.
3. **OpenCode** aplica permisos de edición por ruta (`reports/**`), pero el
   `shell` sigue siendo potente: la directiva ética y el aislamiento de red son
   la última línea de defensa.
4. **Codex** usa TOML para subagentes y no tiene comandos slash de proyecto; los
   flujos se invocan como skills (`$security-audit-pipeline`).
5. Los formatos de configuración de las herramientas cambian; revisa
   [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md) y regenera tras actualizar.

## Licencia

MIT. Ver [`LICENSE`](LICENSE).
