# Contribuir

## Antes de empezar

- Lee [`SPEC.md`](SPEC.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) y la
  [directiva ética](core/ethics/ETHICAL_DIRECTIVE.md).
- Busca issues o PRs abiertos para evitar duplicados.
- Para cambios de seguridad, sigue [`SECURITY.md`](SECURITY.md).

## Flujo

```bash
git checkout -b feat/mi-cambio
# editar core/ (nunca los adaptadores)
make check
git add core tools tests docs
git commit -m "feat: ..."
```

`make check` ejecuta `build`, `validate` y los tests. Si `build` modifica
adaptadores, inclúyelos en el commit: CI verifica que no haya deriva.

## Reglas

1. **Fuente única.** Edita `core/`; los directorios `.claude/`, `.cursor/`,
   `.codex/`, `.agents/` y `.opencode/` son generados.
2. **Frontmatter.** Los agentes usan solo campos planos (`id`, `description`,
   `phase`, `authority`, `tools`, `order`). No añadas mapas anidados.
3. **Sin dependencias.** El toolchain y los tests usan solo la stdlib.
4. **Determinismo.** No añadas timestamps, rutas absolutas ni orden aleatorio a
   los artefactos generados.
5. **Seguridad.** No incluyas exploits armados, payloads destructivos ni
   instrucciones para atacar sistemas de terceros.
6. **Idioma.** Documentación y prompts en español; identificadores en inglés.

## Añadir un agente

1. Crea `core/agents/<fase>/<orden>-<id>.md`.
2. Añade el frontmatter:

   ```yaml
   ---
   id: mi-agente
   description: "Qué hace y cuándo usarlo."
   phase: 2
   authority: sandbox
   tools: [read, search, write, shell]
   order: 50
   ---
   ```

3. Escribe el cuerpo con: asignación, entradas, procedimiento, formato de salida
   y límites.
4. Añade el id a `tests/test_secmatrix.py` y al README.
5. Ejecuta `make check`.

## Añadir una skill

1. Crea `core/skills/<id>/SKILL.md`.
2. `name` debe coincidir con el directorio; incluye una `description` con
   triggers claros.
3. Documenta workflow, salida y reglas. Usa `{{CORE}}` para rutas de la fuente.
4. Ejecuta `make check`.

## Añadir un comando

1. Crea `core/commands/<nombre>.md` con `name`, `description` y `phase`.
2. Usa `$ARGUMENTS` para el objetivo.
3. Recuerda: Codex no genera comandos; el flujo debe existir también como skill.

## Revisión de PR

- El diff no debe tocar adaptadores a mano.
- `make check` debe pasar.
- Los cambios de comportamiento deben actualizar docs y tests.
- Los cambios de permisos o del sandbox requieren revisión explícita.
