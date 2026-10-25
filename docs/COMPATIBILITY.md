# Compatibilidad con Claude Code, Cursor, Codex y OpenCode

Verificado contra la documentación oficial en **octubre de 2026**. Los formatos
cambian con frecuencia: si algo no se carga, revisa la documentación enlazada y
regenera con `python3 tools/secmatrix.py build`.

## Resumen

| Capacidad | Claude Code | Cursor | Codex | OpenCode |
|-----------|-------------|--------|-------|----------|
| Subagentes Markdown | ✅ `.claude/agents/` | ✅ `.cursor/agents/` | ❌ (TOML) | ✅ `.opencode/agents/` |
| Subagentes TOML | ❌ | ❌ | ✅ `.codex/agents/` | ❌ |
| Skills `SKILL.md` | ✅ `.claude/skills/` | ✅ `.cursor/skills/` | ✅ `.agents/skills/` | ✅ `.opencode/skills/` |
| Comandos de proyecto | ✅ `.claude/commands/` | ✅ `.cursor/commands/` | ❌ (custom prompts deprecados) | ✅ `.opencode/commands/` |
| Reglas always-on | `CLAUDE.md` | `.cursor/rules/*.mdc` | `AGENTS.md` | `AGENTS.md` |
| Permisos por ruta | ❌ (solo tools) | ❌ | ❌ | ✅ |
| Aislamiento de escritura | `tools` sin `Edit` | ❌ (sin scoping; `readonly` bloquearía los reportes) | instrucciones | `permissions` |

## Claude Code

- **Subagentes:** `.claude/agents/<name>.md` con `name`, `description`, `tools`,
  `model` opcional. `name` es la identidad; el archivo puede llamarse distinto,
  pero aquí coinciden.
- **Skills:** `.claude/skills/<id>/SKILL.md` con `name` y `description`.
- **Comandos:** `.claude/commands/<name>.md`; el cuerpo usa `$ARGUMENTS`.
- **Instrucciones:** `CLAUDE.md` (soporta `@AGENTS.md` como import).
- **Invocación:** `/sec-audit`, o delegación automática por `description`
  (`"usa el subagente network-auditor"`).
- **Matiz:** los subagentes reciben solo su system prompt + entorno, no el system
  prompt de Claude Code. Por eso cada agente incluye su directiva ética.

## Cursor

- **Subagentes:** `.cursor/agents/<name>.md` con `name`, `description`, `model`,
  `readonly`, `is_background`. Cursor también lee `.claude/agents/` y
  `.codex/agents/` por compatibilidad; aquí generamos `.cursor/` para tener
  precedencia.
- **Skills:** `.cursor/skills/<id>/SKILL.md`; Cursor también carga
  `.agents/skills/` y `.claude/skills/`. `name` debe coincidir con el directorio.
- **Comandos:** `.cursor/commands/<name>.md` (Markdown plano).
- **Reglas:** `.cursor/rules/*.mdc` con `description`, `globs`, `alwaysApply`.
- **Invocación:** `/sec-audit`, `/threat-modeler`, o lenguaje natural.
- **Limitación:** `readonly: true` bloquea *toda* escritura, incluidos los
  reportes. Por eso no lo usamos y el límite `reports/` es instruccional.

## Codex

- **Subagentes:** `.codex/agents/<name>.toml` con `name`, `description` y
  `developer_instructions` obligatorios. Opcionales: `model`,
  `model_reasoning_effort`. Heredan permisos, proveedor y MCP del padre.
- **Skills:** `.agents/skills/<id>/SKILL.md` (estándar agentskills.io). También
  se leen desde `$HOME/.agents/skills` y `/etc/codex/skills`.
- **Comandos:** los *custom prompts* están deprecados; no generamos comandos.
  Usa la skill: `$security-audit-pipeline` o pide explícitamente el subagente.
- **Instrucciones:** `AGENTS.md` en la raíz y en subdirectorios.
- **Invocación:**
  ```text
  Usa la skill $security-audit-pipeline en Fase 1.
  Después lanza el subagente threat-modeler.
  ```

## OpenCode (V2)

- **Subagentes:** `.opencode/agents/<name>.md` con `description`, `mode:
  subagent`, `model` opcional y `permissions` (lista ordenada; gana la última
  regla que coincide). Los campos V1 (`tools`, `permission`, `maxSteps`) están
  deprecados.
- **Skills:** `.opencode/skills/<id>/SKILL.md`; también `.claude/skills/`,
  `.agents/skills/` y `~/.config/opencode/skills/`.
- **Comandos:** `.opencode/commands/<name>.md` (plural; el singular `command/`
  sigue leyéndose).
- **Instrucciones:** `AGENTS.md`.
- **Invocación:** `/sec-audit` o `@security-audit-pipeline`.
- **Skills globales:** añade la fuente canónica al `skills` de
  `~/.config/opencode/opencode.jsonc` para tenerlos en cualquier proyecto
  (`~/` se expande al home y la precedencia es mayor que los skills de proyecto
  descubiertos):

  ```jsonc
  {
    "$schema": "https://opencode.ai/config.json",
    "skills": ["~/sec-agent-matrix/core/skills"]
  }
  ```

  Los agentes y comandos no se globalizan: asumen `core/...` y `reports/` del
  proyecto auditado.
- **Permisos generados:**
  ```yaml
  permissions:
    - action: webfetch
      resource: "*"
      effect: deny
    - action: external_directory
      resource: "*"
      effect: deny
    - action: edit
      resource: "*"
      effect: deny
    - action: edit
      resource: "reports/**"
      effect: allow
    - action: shell
      resource: "*"
      effect: allow
  ```
  `reports/**` es relativo al directorio de trabajo. Si auditas desde una
  subcarpeta, ajusta la regla.

## Diferencias de comportamiento a tener en cuenta

| Tema | Implicación |
|------|-------------|
| Contexto de subagente | Los subagentes no ven la conversación previa: incluye el alcance y los IDs en el prompt de delegación. |
| Descripciones | Son el mecanismo de delegación automática; mantenlas cortas y con triggers claros. |
| Permisos | Solo OpenCode aplica rutas; en el resto, el gate humano y la revisión del diff son obligatorios. |
| Skills | La misma skill se copia en varias rutas; no las edites por separado. |
| Modelos | No fijamos modelo: cada host usa el suyo (`inherit`/por defecto). Así el toolkit no se rompe cuando cambian los IDs. |
| Codex TOML | Las instrucciones usan cadena literal `'''` para evitar escapes; no introduzcas `'''` en el cuerpo de un agente. |
| Cursor commands | No llevan frontmatter; el nombre del archivo define el comando. |

## Cómo re-verificar tras una actualización

1. Consulta la documentación oficial:
   - Claude Code: <https://code.claude.com/docs/en/sub-agents>
   - Cursor: <https://cursor.com/docs/subagents> y <https://cursor.com/docs/skills>
   - Codex: <https://learn.chatgpt.com/docs/agent-configuration/subagents> y
     <https://developers.openai.com/codex/build-skills>
   - OpenCode: <https://opencode.ai/v2/docs/agents> y
     <https://opencode.ai/v2/docs/skills>
2. Compara rutas y campos con `docs/ARCHITECTURE.md`.
3. Ajusta `tools/secmatrix.py` y los tests.
4. Ejecuta `make check` y prueba una invocación real en cada host.
