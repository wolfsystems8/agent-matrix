# AGENTS.md

Guía para agentes que trabajan **sobre este repositorio** (no para los agentes de
seguridad que genera el toolkit).

## Qué es este repositorio

`sec-agent-matrix` empaqueta 9 agentes y 9 skills de auditoría de seguridad y
genera adaptadores nativos para Claude Code, Cursor, Codex y OpenCode. La fuente
única está en `core/`; los directorios de herramientas son artefactos generados.

## Comandos

```bash
make build      # regenera adaptadores y manifiesto
make validate   # estructura + drift
make test       # unittest (stdlib)
make check      # build + validate + test
make doctor     # comprueba docker/git/adaptadores
```

## Estructura

- `core/agents/<fase>/` — agentes (frontmatter plano).
- `core/skills/<id>/SKILL.md` — skills portables.
- `core/commands/` — comandos `/sec-*`.
- `core/ethics/` — guardrails globales (autoridad superior).
- `core/pipeline/` — orquestador de fases.
- `core/formatters/` — plantillas de reportes.
- `core/sandbox/` — compose, Dockerfile del runner y scripts.
- `tools/secmatrix.py` — build/validate/install/list/doctor/clean.
- `tests/` — unittest sin dependencias.
- `.claude/`, `.cursor/`, `.codex/`, `.agents/`, `.opencode/` — **generados**.

## Reglas

- **Nunca** edites los adaptadores generados. Edita `core/` y ejecuta `make
  build`.
- Mantén la construcción determinista: sin timestamps ni rutas absolutas.
- No añadas dependencias Python externas.
- No cambies el esquema de frontmatter sin actualizar
  `docs/ARCHITECTURE.md`, `tools/secmatrix.py` y los tests.
- No debilites los guardrails ni los permisos sin justificarlo en el PR.
- No incluyas exploits armados, payloads destructivos ni instrucciones para
  atacar sistemas de terceros.
- Ejecuta `make check` antes de terminar cualquier cambio.

## Al añadir artefactos

1. Agente: `core/agents/<fase>/<orden>-<id>.md` + test + README.
2. Skill: `core/skills/<id>/SKILL.md` + test si cambia el conteo.
3. Comando: `core/commands/<nombre>.md` + equivalente en skill para Codex.
4. Host nuevo: `render_agent_<host>` + rutas en `build_files` + docs + test.

## Criterio de done

- `make check` en verde.
- `git status` limpio después de `build` (adaptadores incluidos).
- Documentación actualizada.
- Sin secretos, PII ni rutas de máquina en el diff.
- Cierre y alcance: se cumplen las 7 condiciones de
  `core/pipeline/PIPELINE_ORCHESTRATOR.md` (IDs con estado final, remediación
  re-verificada, suite verde, dependencias escaneadas, `teardown: OK`, estado
  persistido y repo limpio). Un análisis terminado no genera trabajo nuevo: no
  se reabren fases, no se convierten observaciones en tareas, no se aplican
  cambios "de paso" ni se proponen "próximos pasos". Ampliar alcance exige
  petición explícita del usuario, registro en `PIPELINE_STATUS.md` y un gate
  nuevo.
