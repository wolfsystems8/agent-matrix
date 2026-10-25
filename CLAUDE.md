# CLAUDE.md

@AGENTS.md

## Notas específicas de Claude Code

- Los agentes de seguridad están en `.claude/agents/` y las skills en
  `.claude/skills/`.
- Comandos disponibles: `/sec-audit`, `/sec-pentest`, `/sec-fix`, `/sec-pipeline`.
- No edites `.claude/` a mano: se genera desde `core/` con
  `python3 tools/secmatrix.py build`.
- Para una auditoría, empieza por `/sec-audit` y respeta el gate antes de la
  Fase 2.
