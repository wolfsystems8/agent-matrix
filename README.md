<div align="center">

# 🛡️ sec-agent-matrix

**Skills y agentes de seguridad para agentes de código con IA.**
Clónalo una vez y úsalo en **Claude Code, OpenCode, Codex y Cursor**.

![Versión](https://img.shields.io/badge/versión-0.1.0-6f42c1)
![Licencia](https://img.shields.io/badge/licencia-MIT-green)
![Python](https://img.shields.io/badge/python-3.9%2B-3776ab)
![Dependencias](https://img.shields.io/badge/dependencias-0-brightgreen)
![Agentes](https://img.shields.io/badge/agentes-21-blue)
![Skills](https://img.shields.io/badge/skills-19-orange)

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
│ ción      │    │ CIA·S&S      │    │ DAST web/API  │     │ mínimos      │    │ Teardown  │
│           │    │ SQUARE/STRIDE│    │ PoCs éticas   │     │ Regresión QA │    │ Repo      │
│           │───▶│ SQLi·XSS·CSRF│─◆─▶│ Confirmación  │─ ◆ ─▶│ Re-PoC       │───▶│ limpio    │
│ reports/  │    │ Cripto·CSP   │GATE│ Logs sandbox  │ GATE │              │    │           │
│           │    │ Logs·ITIL 4  │ 1  │               │  2   │              │    │           │
│           │    │ Riesgos 27005│    │               │      │              │    │           │
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

Los agentes se eligen de dos formas:

- **Por tarea:** `security-task-router` convierte una petición puntual
  (*"¿hay SQLi en la búsqueda?"*) en los agentes justos y sus dependencias.
- **Por proyecto:** en una auditoría completa, `audit-program-lead` arma el mapa
  de cobertura según lo que contiene el repositorio.

---

## ✨ Por qué existe

| | |
|---|---|
| 🧩 **Una fuente, cuatro hosts** | Editas `core/` una vez; `secmatrix build` genera el formato nativo de cada herramienta. |
| 🔒 **Guardrails reales** | Red Docker `internal: true`, `cap_drop: ALL`, rootfs de solo lectura y fases con autoridad limitada. |
| 🚦 **Humano en el circuito** | Dos gates obligatorios y reglas de parada (egreso abierto, Docker ausente, sin autorización). |
| 📦 **Drop-in** | Los adaptadores están versionados: clonas, abres el repo y ya funciona. |
| 🌐 **Cualquier modelo, cualquier idioma** | Agentes, skills y orquestador definidos en inglés para que cualquier modelo los ejecute; los reportes salen en el idioma del usuario. |
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

`sec-agent-matrix install` copia automáticamente esa plantilla en el destino
(`reports/ENGAGEMENT_SCOPE.md`). Sin alcance escrito ningún agente ejecuta
pruebas dinámicas.

### 3. Lanza la auditoría

| Herramienta | Invocación |
|-------------|------------|
| **Claude Code** | `/sec-task` · `/sec-iso-audit` · `/sec-sdlc` · `/sec-audit` · `/sec-pentest` · `/sec-fix` · `/sec-pipeline` |
| **OpenCode** | `/sec-task` · `/sec-iso-audit` · `/sec-sdlc` · `/sec-audit` · `/sec-pentest` · `/sec-fix` · `/sec-pipeline` |
| **Codex** | `Usa la skill $security-task-router` · `$iso-audit-lifecycle` · `$sdlc-security` · `$security-audit-pipeline` |
| **Cursor** | `/sec-task` · `/sec-iso-audit` · `/sec-sdlc` · `/sec-audit` · `/threat-modeler` |

| Ciclo | Comando | Qué hace |
|-------|---------|----------|
| Tarea puntual | `/sec-task <petición>` | Ejecuta solo los agentes que la petición necesita (p. ej. *"revisa XSS en el login"*) y termina en el gate sí/no |
| Auditoría de sistemas | `/sec-iso-audit` | ISO 19011 de inicio a seguimiento, riesgos ISO 27005 ordenados por severidad, procesos ITIL 4 |
| Seguridad en el SDLC | `/sec-sdlc` | CIA, Saltzer & Schroeder, SQUARE/STRIDE, SQLi, XSS, fuerza bruta, path traversal, CSRF, cripto, encoding/CSP, logs |
| Completo | `/sec-pipeline` | Ambos ciclos + pentest en sandbox + gate "¿corregir? sí/no" |

El entregable final de cada auditoría es el **informe unificado**
`reports/AUDIT_UNIFIED_REPORT.md`: consolida todos los hallazgos, los falsos
positivos descartados, las recomendaciones y el registro de riesgos. Los
artefactos por fase son documentos internos de trabajo.

### Dependencia y entregable

La fase 1 incluye un paso de escaneo de dependencias que escribe
`reports/DEPENDENCY_SCAN.md` (fecha, herramienta, versión y hallazgos). La
condición de cierre exige ese escaneo junto con el resto de las condiciones.

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

Carga las 19 skills en cualquier proyecto desde
`~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["~/sec-agent-matrix/core/skills"]
}
```

Los agentes y comandos siguen siendo por proyecto, porque referencian `core/...`
y `reports/` del repositorio auditado.

En OpenCode, los comandos `/sec-*` generados se enlazan con el subagente
orquestador mediante frontmatter `agent: <orquestador>` + `subagent: true`, y
el orquestador recibe permisos `subagent` para lanzar a los especialistas. En
Claude Code los comandos se ejecutan como slash commands con delegación a los
subagentes; en Codex no existen comandos y se usan las skills.

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
| 1 | `sdlc-security-lead` | read-only | `SDLC_SECURITY_REVIEW.md` (CIA, Saltzer & Schroeder) |
| 1 | `square-requirements` | read-only | `SECURITY_REQUIREMENTS.md` (SQUARE) |
| 1 | `threat-modeler` | read-only | `THREAT_MODEL.md` (STRIDE) |
| 1 | `attack-surface-mapper` | read-only | `ATTACK_SURFACE.md` (vectores de ataque) |
| 1 | `sast-auditor` | read-only | `SAST_RAW_FINDINGS.md` |
| 1 | `sqli-analyst` | read-only | `SQLI_FINDINGS.md` (union, error, boolean, time) |
| 1 | `xss-analyst` | read-only | `XSS_FINDINGS.md` (reflected, stored, DOM) |
| 1 | `web-vuln-analyst` | read-only | `WEB_VULN_FINDINGS.md` (fuerza bruta, path traversal, CSRF) |
| 1 | `crypto-reviewer` | read-only | `CRYPTO_REVIEW.md` (simétrica, asimétrica) |
| 1 | `output-encoding-csp-reviewer` | read-only | `ENCODING_CSP_REVIEW.md` (5 contextos, CSP None/Low/Medium/Strict) |
| 1 | `log-auditor` | read-only | `LOG_AUDIT.md` (auth, app, red, web, SO) |
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
| `security-task-router` | Enruta una petición puntual a los agentes justos |
| `iso-audit-lifecycle` | Auditoría de sistemas ISO 19011 de inicio a seguimiento |
| `risk-assessment-iso27005` | Tabla de riesgos ordenada por severidad y tratamiento |
| `itil-process-audit` | Madurez de prácticas ITIL 4 (cambios, despliegue, incidentes…) |
| `sdlc-security` | CIA, Saltzer & Schroeder, SQUARE o STRIDE, riesgo por fase del SDLC |
| `injection-xss-analysis` | SQLi y XSS por tipo, con línea exacta y evaluación de filtros ante evasión |
| `web-vuln-identification` | Vectores de ataque y exposición a XSS, SQLi, fuerza bruta, path traversal, CSRF |
| `crypto-review` | Criptografía simétrica y asimétrica, hashing, RNG, JWT, claves |
| `output-encoding-csp` | Encoding en HTML, script, JSON, URL y CSS; CSP en 4 niveles (None, Low, Medium, Strict) |
| `security-log-analysis` | Logs de autenticación, aplicación, red, servidor web y SO |
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
El código se monta en `pentest-runner` como `/src` de **solo lectura**
(`SOURCE_DIR`, por defecto la raíz del proyecto): no se copia y ninguna
herramienta del sandbox puede modificarlo.

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
│   ├── agents/                 ← 21 agentes (00-audit-program, 01-ssdlc, 02-pentest, 03-remediation)
│   ├── skills/                 ← 19 skills portables
│   ├── commands/               ← 7 comandos /sec-*
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
