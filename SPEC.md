# Spec: sec-agent-matrix

## Objective

Empaquetar un pipeline de auditoría de seguridad (SSDLC → pentest en sandbox →
remediación) como agentes y skills reutilizables, con una sola fuente de verdad
que funcione en Claude Code, Cursor, Codex y OpenCode.

**Éxito:** un usuario instala el toolkit en un repositorio, invoca un comando o
skill, y obtiene los reportes de cada fase sin editar archivos por herramienta.

## Requisitos funcionales

1. Nueve agentes: 3 de SSDLC, 4 de pentest y 2 de remediación.
2. Nueve skills portables que orquestan el flujo y las sub-tareas.
3. Cuatro comandos (`/sec-audit`, `/sec-pentest`, `/sec-fix`, `/sec-pipeline`).
4. Generación nativa por host:
   - Claude Code: `.claude/agents`, `.claude/skills`, `.claude/commands`.
   - Cursor: `.cursor/agents`, `.cursor/skills`, `.cursor/commands`, `.cursor/rules`.
   - Codex: `.codex/agents/*.toml`, `.agents/skills`.
   - OpenCode: `.opencode/agents`, `.opencode/skills`, `.opencode/commands`.
5. Instalador `--target` idempotente, con detección de conflictos y `--dry-run`.
6. Validador de estructura, duplicados y deriva entre fuente y adaptadores.
7. Sandbox Docker con red interna, sin egreso y sin privilegios.
8. Tests sin dependencias externas y CI que verifique la sincronización.

## No objetivos

- Ejecutar pruebas contra sistemas de terceros o producción.
- Sustituir a un pentest profesional con alcance legal.
- Incluir exploits armados, malware o post-explotación.
- Ser un escáner autónomo sin gates humanos.

## Estructura

```text
core/agents/<fase>/<orden>-<id>.md    # agentes
core/skills/<id>/SKILL.md             # skills
core/commands/<name>.md               # comandos
core/ethics/                          # guardrails
core/pipeline/                        # orquestador
core/formatters/                      # plantillas
core/sandbox/                         # compose + runner
tools/secmatrix.py                    # build/validate/install
tests/                                # unittest
```

## Comandos

```bash
make build      # python3 tools/secmatrix.py build
make validate   # estructura + drift
make test       # unittest
make check      # build + validate + test
make install TARGET=../mi-app
```

## Estilo

- Markdown en español, identificadores en inglés/kebab-case.
- Frontmatter plano (sin mapas anidados) para los agentes.
- Sin timestamps en artefactos generados.
- Sin dependencias Python externas.

## Testing

- Unitarios de parser, carga, generación determinista, TOML válido, permisos y
  manifiesto.
- Integración de `install` en directorio temporal: layout, idempotencia,
  conflictos y `--dry-run`.
- CI: `build` + `git diff --exit-code` + `validate` + tests + smoke install.

## Boundaries

- **Always:** editar `core/`; ejecutar `make check`; respetar la directiva ética.
- **Ask first:** añadir dependencias, cambiar el esquema de frontmatter, modificar
  el compose o el modelo de permisos.
- **Never:** commitear secretos; editar adaptadores generados; añadir pruebas
  dinámicas contra hosts no autorizados; silenciar tests.

## Criterios de aceptación

- [x] `build` produce 175 archivos deterministas.
- [x] `validate` pasa sin errores ni avisos.
- [x] Los 21 TOML de Codex parsean con `tomllib`.
- [x] `install` crea el layout esperado y es idempotente.
- [x] Un archivo conflictivo requiere `--force`.
- [x] `--dry-run` no escribe nada.
- [x] La documentación cubre las cuatro herramientas y sus límites.
- [ ] Prueba end-to-end de la Fase 2 en un host con Docker (pendiente: Docker no
      está instalado en el entorno de desarrollo).
