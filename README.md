<div align="center">

# 🛡️ sec-agent-matrix

**Skills y agentes de seguridad para agentes de código con IA.**
Clónalo una vez y úsalo en **Claude Code, OpenCode, Codex y Cursor**.

![Versión](https://img.shields.io/badge/versión-0.1.0-6f42c1)
![Licencia](https://img.shields.io/badge/licencia-MIT-green)
![Python](https://img.shields.io/badge/python-3.9%2B-3776ab)
![Dependencias](https://img.shields.io/badge/dependencias-0-brightgreen)
![Agentes](https://img.shields.io/badge/agentes-12-blue)
![Skills](https://img.shields.io/badge/skills-12-orange)

![Claude Code](https://img.shields.io/badge/Claude_Code-✓-d97757)
![OpenCode](https://img.shields.io/badge/OpenCode-✓-1f6feb)
![Codex](https://img.shields.io/badge/Codex-✓-10a37f)
![Cursor](https://img.shields.io/badge/Cursor-✓-555555)

</div>

Las skills codifican el flujo que seguiría un equipo de seguridad: modelar
amenazas, revisar el código, verificar en un sandbox aislado y parchear con
pruebas. Están empaquetadas para que el agente las siga igual en cada fase y
con **gates humanos** entre ellas.

> ⚠️ **Uso autorizado únicamente.** Audita sistemas propios o con autorización
> escrita, dentro de un sandbox aislado. Lee
> [`core/ethics/ETHICAL_DIRECTIVE.md`](core/ethics/ETHICAL_DIRECTIVE.md).

```text
   FASE 0           FASE 1              FASE 2                FASE 3              CIERRE
   ALCANCE          AUDITORÍA + SSDLC   PENTEST (sandbox)     REMEDIACIÓN         ENTORNO

┌───────────┐    ┌──────────────┐    ┌───────────────┐     ┌──────────────┐    ┌───────────┐
│ Scope     │    │ Plan 19011   │    │ Sandbox       │     │ Patcher      │    │ Informe   │
│ Autoriza- │    │ Mapa agentes │    │ Red / TLS     │     │ Parches      │    │ 19011     │
│ ción      │    │ STRIDE·SAST  │    │ DAST web/API  │     │ mínimos      │    │ Teardown  │
│           │───▶│ Triage CVSS  │─◆─▶│ PoCs éticas   │─ ◆ ─▶│ Regresión QA │───▶│ Repo      │
│ reports/  │    │ ITIL 4       │GATE│ Confirmación  │ GATE │ Re-PoC       │    │ limpio    │
│           │    │ Riesgos 27005│ 1  │               │  2   │              │    │           │
└───────────┘    └──────────────┘    └───────────────┘     └──────────────┘    └───────────┘
   escribe          solo lectura        solo lectura +        escribe código       solo lectura
   reports/         + reports/          reports/ + sandbox    (solo con "sí")
```

**◆ Gate 1:** revisas el registro de riesgos ordenado por severidad y apruebas
la Fase 2 (si el plan la requiere).
**◆ Gate 2:** ves las recomendaciones por severidad y respondes
*"¿Deseas corregir las vulnerabilidades halladas? (sí/no)"*. Con **no**, el
código no se toca.

El código auditado se analiza **en su sitio, sin copiarlo**, y el agente
`audit-program-lead` decide qué subagentes hacen falta: los necesarios se
ejecutan en automático y el resto se omite con motivo.

---

## ✨ Por qué existe

| | |
|---|---|
| 🧩 **Una fuente, cuatro hosts** | Editas `core/` una vez; `secmatrix build` genera el formato nativo de cada herramienta. |
| 🔒 **Guardrails reales** | Red Docker `internal: true`, `cap_drop: ALL`, rootfs de solo lectura y fases con autoridad limitada. |
| 🚦 **Humano en el circuito** | Dos gates obligatorios y reglas de parada (egreso abierto, Docker ausente, sin autorización). |
| 📦 **Drop-in** | Los adaptadores están versionados: clonas, abres el repo y ya funciona. |
| 🧪 **Determinista y sin dependencias** | Mismos fuentes → mismos bytes. Solo Python estándar; CI falla si hay deriva. |

## 🚀 Inicio rápido

### 1. Clona y abre con tu herramienta

```bash
git clone https://github.com/<usuario>/sec-agent-matrix.git
cd sec-agent-matrix
python3 tools/secmatrix.py doctor     # comprueba docker, git y adaptadores
```

Abre la carpeta con tu agente. No hay paso de instalación: los adaptadores ya
están en el repositorio.

### 2. Define el alcance

```bash
cp core/formatters/ENGAGEMENT_SCOPE_TEMPLATE.md reports/ENGAGEMENT_SCOPE.md
```

Sin alcance escrito ningún agente ejecuta pruebas dinámicas.

### 3. Lanza la auditoría

| Herramienta | Invocación |
|-------------|------------|
| **Claude Code** | `/sec-iso-audit` · `/sec-audit` · `/sec-pentest` · `/sec-fix` · `/sec-pipeline` |
| **OpenCode** | `/sec-iso-audit` · `/sec-audit` · `/sec-pentest` · `/sec-fix` · `/sec-pipeline` |
| **Codex** | `Usa la skill $iso-audit-lifecycle` · `Usa la skill $security-audit-pipeline` |
| **Cursor** | `/sec-iso-audit` · `/sec-audit` · `/threat-modeler` |

## 📥 Usarlo en otro proyecto

```bash
python3 tools/secmatrix.py install --target ../mi-app
```

Copia la fuente a `../mi-app/.sec-agent-matrix/core/`, genera los adaptadores con
las rutas reescritas, crea `reports/` y añade un bloque gestionado e idempotente
a `AGENTS.md` y `CLAUDE.md`.

```bash
--tools claude,opencode,codex  # instalar solo algunos hosts
--dry-run                      # ver qué se escribiría
--force                        # sobrescribir archivos no gestionados
--prune                        # borrar adaptadores obsoletos
--no-rules                     # no tocar AGENTS.md / CLAUDE.md
```

### Skills globales en OpenCode

Carga las 12 skills en cualquier proyecto desde
`~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["~/sec-agent-matrix/core/skills"]
}
```

Los agentes y comandos siguen siendo por proyecto, porque referencian `core/...`
y `reports/` del repositorio auditado.

## 🏗️ Arquitectura

```text
                          ┌──────────────────────────┐
                          │  core/   (fuente única)  │
                          │  agents · skills ·       │
                          │  commands · ethics ·     │
                          │  pipeline · sandbox      │
                          └────────────┬─────────────┘
                                       │
                          ┌────────────▼─────────────┐
                          │  tools/secmatrix.py      │
                          │  build · validate ·      │
                          │  install · doctor        │
                          └────────────┬─────────────┘
              ┌───────────────┬────────┴───────┬────────────────┐
              ▼               ▼                ▼                ▼
        .claude/         .opencode/      .codex/ + .agents/   .cursor/
        agents/*.md      agents/*.md     agents/*.toml        agents/*.md
        skills/          skills/         skills/              skills/
        commands/        commands/       (sin comandos)       commands/ rules/
```

El manifiesto `.secmatrix-manifest.json` guarda hashes para detectar ediciones
manuales y deriva. Nunca edites los directorios generados: cambia `core/` y
ejecuta `make build`.

| Artefacto | Claude Code | OpenCode | Codex | Cursor |
|-----------|-------------|----------|-------|--------|
| Agentes | `.claude/agents/*.md` | `.opencode/agents/*.md` | `.codex/agents/*.toml` | `.cursor/agents/*.md` |
| Skills | `.claude/skills/` | `.opencode/skills/` | `.agents/skills/` | `.cursor/skills/` |
| Comandos | `.claude/commands/` | `.opencode/commands/` | — (usar skills) | `.cursor/commands/` |

Detalles y limitaciones por host: [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md).
Modelo de datos: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## 🤖 Agentes

| Fase | ID | Autoridad | Salida |
|------|----|-----------|--------|
| 1 | `audit-program-lead` | read-only | `AUDIT_PLAN.md`, `ISO19011_AUDIT_REPORT.md` |
| 1 | `threat-modeler` | read-only | `THREAT_MODEL.md` |
| 1 | `sast-auditor` | read-only | `SAST_RAW_FINDINGS.md` |
| 1 | `triage-master` | read-only | `AUDIT_REPORT.md` |
| 1 | `itil-process-auditor` | read-only | `ITIL_PROCESS_AUDIT.md` |
| 1 | `risk-assessor` | read-only | `RISK_REGISTER.md` (ISO 27005) |
| 2 | `sandbox-manager` | sandbox | `SANDBOX_STATUS.md` |
| 2 | `network-auditor` | sandbox | `NETWORK_AUDIT.md` |
| 2 | `web-dast-tester` | sandbox | `WEB_DAST_REPORT.md` |
| 2 | `exploit-tester` | sandbox | `PENTEST_VERIFICATION.md` |
| 3 | `secfix-patcher` | write | Código + cambios |
| 3 | `regression-qa` | write | `REMEDIATION_SUMMARY.md` |

`read-only` y `sandbox` solo escriben en `reports/`; `write` puede editar código.
OpenCode lo aplica con permisos por acción y ruta, Claude con la lista `tools`, y
Cursor y Codex con instrucciones más el gate humano.

## 🧰 Skills

| Skill | Cuándo usarla |
|-------|---------------|
| `iso-audit-lifecycle` | Auditoría de sistemas ISO 19011 de inicio a seguimiento |
| `risk-assessment-iso27005` | Tabla de riesgos ordenada por severidad y tratamiento |
| `itil-process-audit` | Madurez de prácticas ITIL 4 (cambios, despliegue, incidentes…) |
| `security-audit-pipeline` | Auditoría completa con gates |
| `threat-modeling` | STRIDE sobre arquitectura |
| `sast-code-audit` | Revisión estática con CWE/ASVS |
| `vulnerability-triage` | Consolidar y puntuar CVSS v3.1 |
| `sandbox-pentest` | Fase 2 completa |
| `network-tls-audit` | Puertos, servicios, TLS |
| `web-api-dast` | Cabeceras, CORS, cookies, API |
| `security-remediation` | Parches mínimos |
| `security-regression-qa` | Tests + re-PoC + cierre |

## 🐳 Sandbox

Solo la Fase 2 necesita Docker + Compose v2. Sin Docker, las Fases 1 y 3 siguen
funcionando y la Fase 2 se bloquea de forma explícita.

```bash
# Arrancar (por defecto levanta demo-target, una app vulnerable de demostración)
docker compose -f core/sandbox/docker-compose.sandbox.yml up -d --build

# Verificar aislamiento
docker network inspect sec-agent-matrix_sandbox_net --format '{{.Internal}}'   # true
docker compose -f core/sandbox/docker-compose.sandbox.yml \
  exec -T pentest-runner sh -lc '/scripts/smoke_test.sh'                      # EGRESS_BLOCKED

# Destruir stack, volúmenes y PoC temporales
sh core/sandbox/scripts/teardown.sh                                           # teardown: OK
```

Para auditar una app propia define `TARGET_CONTEXT` (y `TARGET_DOCKERFILE` /
`TARGET_PORT` si aplica) en `core/sandbox/.env`; la app debe exponer `:8080`.

Detalle: [`core/sandbox/README.md`](core/sandbox/README.md).

## 🛠️ Desarrollo

```bash
make build      # regenera adaptadores y manifiesto
make validate   # estructura + drift
make test       # unittest (stdlib)
make check      # build + validate + test
make doctor     # docker / git / adaptadores
```

Para añadir contenido, edita solo `core/` y ejecuta `make check`:

- **Agente:** `core/agents/<fase>/<orden>-<id>.md` con frontmatter `id`,
  `description`, `phase`, `authority`, `tools`, `order`.
- **Skill:** `core/skills/<id>/SKILL.md` con `name` igual al directorio.
- **Comando:** `core/commands/<nombre>.md` con `description` y `phase`.

Guía completa: [`CONTRIBUTING.md`](CONTRIBUTING.md) · [`docs/USAGE.md`](docs/USAGE.md).

<details>
<summary><b>Estructura del repositorio</b></summary>

```text
sec-agent-matrix/
├── core/                       ← fuente única
│   ├── agents/                 ← 12 agentes (00-audit-program, 01-ssdlc, 02-pentest, 03-remediation)
│   ├── skills/                 ← 12 skills portables
│   ├── commands/               ← 5 comandos /sec-*
│   ├── ethics/                 ← directiva global
│   ├── pipeline/               ← orquestador
│   ├── formatters/             ← plantillas de reportes
│   └── sandbox/                ← compose, runner, scripts
├── tools/secmatrix.py          ← generador / instalador / validador
├── tests/                      ← unittest sin dependencias
├── docs/                       ← arquitectura, compatibilidad, uso
├── reports/                    ← salida de auditorías
├── .claude/ .opencode/ .codex/ .agents/ .cursor/   ← generados
└── AGENTS.md · CLAUDE.md
```

</details>

## ⚠️ Limitaciones conocidas

1. **Cursor** no restringe escrituras por ruta en subagentes: el límite de
   `reports/` es instruccional y se refuerza con el gate humano.
2. **OpenCode** aplica permisos de edición por ruta, pero el `shell` sigue siendo
   potente: la directiva ética y el aislamiento de red son la última defensa.
3. **Codex** usa TOML para subagentes y no tiene comandos slash de proyecto; los
   flujos se invocan como skills (`$security-audit-pipeline`).
4. Los formatos de configuración de cada herramienta cambian; revisa
   [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md) y regenera tras actualizar.

## 📄 Licencia

MIT. Ver [`LICENSE`](LICENSE).
