# Arquitectura

## Principios

1. **Fuente única.** Todo el contenido vive en `core/`. Los directorios
   `.claude/`, `.cursor/`, `.codex/`, `.agents/` y `.opencode/` son artefactos
   generados y no se editan a mano.
2. **Formato nativo, no lowest-common-denominator.** Cada host recibe su formato
   real: YAML + Markdown para Claude/Cursor/OpenCode, TOML para los subagentes de
   Codex, `SKILL.md` estándar para las skills.
3. **Construcción determinista.** Sin timestamps ni orden no determinista. Los
   mismos fuentes producen exactamente los mismos bytes y hashes.
4. **Instalación segura.** El instalador no pisa archivos del usuario sin
   `--force`, usa un manifiesto para distinguir lo generado y reescribe las rutas
   de `core/` al prefijo instalado.
5. **Defensa en profundidad.** Los permisos del host son la primera barrera; la
   directiva ética, el aislamiento de red y los gates humanos son las siguientes.

## Modelo de datos

### Agente

```yaml
---
id: network-auditor              # único, kebab-case, nombre del archivo .md generado
description: "..."              # se usa para delegación automática; corta y específica
phase: 2                        # 1 | 2 | 3
authority: sandbox              # read-only | sandbox | write
tools: [read, search, write, shell]  # read, search, write, edit, shell
order: 20                       # orden dentro de la fase
---
```

`authority` determina los permisos generados:

| authority | Claude | OpenCode | Cursor | Codex |
|-----------|--------|----------|--------|-------|
| `read-only` | sin `Edit` | `edit` deny + `reports/**` allow | instrucciones | instrucciones |
| `sandbox` | sin `Edit` | `edit` deny + `reports/**` allow | instrucciones | instrucciones |
| `write` | con `Edit` | `edit` allow | instrucciones | instrucciones |

En los tres casos se deniega `webfetch`, `websearch` y `external_directory` en
OpenCode, y se añade al cuerpo la referencia a la directiva ética.

### Skill

```yaml
---
name: web-api-dast              # debe coincidir con el directorio
description: "..."              # trigger + scope
metadata:
  phase: 2
  authority: sandbox
---
```

Se genera el mismo `SKILL.md` en las cuatro ubicaciones; el token `{{CORE}}` del
cuerpo se sustituye por el prefijo correspondiente.

### Comando

```yaml
---
name: sec-audit
description: "..."
phase: 1
---
# cuerpo con $ARGUMENTS
```

Se genera para Claude (con `argument-hint`), OpenCode (con `description`) y
Cursor (Markdown plano). Codex no tiene comandos de proyecto: se usa la skill.

## Mapeo de rutas

| Artefacto | Claude Code | Cursor | Codex | OpenCode |
|-----------|-------------|--------|-------|----------|
| Agentes | `.claude/agents/*.md` | `.cursor/agents/*.md` | `.codex/agents/*.toml` | `.opencode/agents/*.md` |
| Skills | `.claude/skills/<id>/SKILL.md` | `.cursor/skills/<id>/SKILL.md` | `.agents/skills/<id>/SKILL.md` | `.opencode/skills/<id>/SKILL.md` |
| Comandos | `.claude/commands/*.md` | `.cursor/commands/*.md` | — | `.opencode/commands/*.md` |
| Reglas | `CLAUDE.md` + `AGENTS.md` | `.cursor/rules/*.mdc` | `AGENTS.md` | `AGENTS.md` |

Cursor y OpenCode también leen `.agents/skills/`, por lo que las skills de Codex
sirven como respaldo compartido.

## Flujo de generación

```text
load_agents() ─┐
load_skills() ─┼─→ build_files(prefix, tools) ─→ dict[path] = content
load_commands()┘                                      │
                                                      ├─→ write_files(out, files)
                                                      │     ├─ compara bytes (idempotente)
                                                      │     ├─ poda obsoletos (--prune)
                                                      │     └─ escribe manifiesto
                                                      └─→ manifest {path: sha256}
```

`validate` recalcula `build_files("core", TOOLS)` y compara con el disco. Si algo
difiere, falla con el archivo exacto. CI ejecuta `build` y comprueba que
`git status` queda limpio.

## Instalación

`install --target <dir>`:

1. Copia `core/` a `<dir>/.sec-agent-matrix/core/`.
2. Genera adaptadores con prefijo `.sec-agent-matrix/core`.
3. Detecta conflictos: si un archivo existe y no está en el manifiesto previo,
   exige `--force`.
4. Crea `reports/` y su README.
5. Fusiona un bloque marcado en `AGENTS.md` (y `CLAUDE.md` si no existe, con
   `@AGENTS.md`). La fusión es idempotente: reemplaza entre marcadores.

### Por qué no symlinks

Los symlinks fallan en Windows, en algunos modos de Cursor/Codex y al copiar el
proyecto a un contenedor. Copiar + manifiesto es portable y auditable.

### Por qué no un único `.agents/`

Cada host tiene su propio formato de subagente. Forzar un formato común obliga a
renunciar a TOML en Codex o a los permisos por ruta de OpenCode. La generación
mantiene la riqueza de cada host con una sola fuente.

## Extender a una herramienta nueva

1. Añade su nombre a `TOOLS`.
2. Implementa `render_agent_<tool>`, `render_skill` (si comparte `SKILL.md`) y
   `render_command_<tool>`.
3. Añade las rutas en `build_files`.
4. Añade el chequeo en `doctor` y la documentación en `docs/COMPATIBILITY.md`.
5. Añade un test de formato (por ejemplo, parsear el TOML con `tomllib`).

## Seguridad del propio toolchain

- Solo escribe dentro de `ROOT` (build/clean) o del `--target` indicado.
- La escritura es atómica (`os.replace`) y no sigue symlinks: un enlace
  plantado en el destino se sustituye, no se escribe a través de él.
- `install` rechaza instalar sobre el propio toolkit y aborta si encuentra
  symlinks en `.sec-agent-matrix`.
- `clean` solo borra las rutas del manifiesto, validadas con `safe_join`.
- No ejecuta código de los agentes; solo transforma Markdown/TOML.
- No hace peticiones de red.
- Los tests cubren conflictos, idempotencia, `--dry-run`, symlinks y rutas que
  escapan del proyecto.
