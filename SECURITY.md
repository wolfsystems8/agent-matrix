# Seguridad y uso responsable

## Uso autorizado

`sec-agent-matrix` es una herramienta de auditoría defensiva. Solo debe usarse
sobre:

- Sistemas propios.
- Sistemas para los que exista autorización escrita del propietario.
- Entornos de laboratorio o sandbox bajo tu control.

El uso contra sistemas de terceros sin autorización puede ser ilegal y está
explícitamente prohibido por la [directiva ética](core/ethics/ETHICAL_DIRECTIVE.md).

## Modelo de seguridad

| Capa | Control |
|------|---------|
| Alcance | `reports/ENGAGEMENT_SCOPE.md` obligatorio antes de la Fase 2 |
| Red | `sandbox_net` con `internal: true`; sin egreso a Internet |
| Exposición | Puerto del objetivo solo en `127.0.0.1` |
| Contenedores | `no-new-privileges`; `cap_drop: ALL` + `NET_RAW` en el runner |
| Escritura | Fases 1 y 2 limitadas a `reports/` (OpenCode lo aplica por ruta) |
| Destrucción | Prohibidos DoS, fuerza bruta, borrado y exfiltración |
| Datos | Secretos y PII enmascarados en los reportes |
| Gates | Aprobación humana entre fases |
| Trazabilidad | IDs estables y evidencia por hallazgo |

## Límites que el toolkit **no** puede garantizar

- Que el usuario tenga autorización real.
- Que el código auditado sea seguro por el hecho de ejecutar el pipeline.
- Aislamiento absoluto si el host Docker está comprometido.
- Que un LLM no alucine un hallazgo: por eso todo hallazgo confirmado requiere
  PoC o evidencia reproducible.

## Reportar una vulnerabilidad del toolkit

Si encuentras un fallo en el generador, el instalador o el sandbox:

1. No lo explotes fuera de un entorno propio.
2. Abre un issue privado o contacta al mantenedor.
3. Incluye versión, comando, salida y un caso mínimo de reproducción.
4. No publiques detalles explotables hasta que exista un parche.

## Checklist antes de un engagement

- [ ] Tengo autorización escrita.
- [ ] El alcance está en `reports/ENGAGEMENT_SCOPE.md`.
- [ ] Docker está instalado y actualizado.
- [ ] La red del sandbox es interna y el egreso está bloqueado.
- [ ] No hay datos reales en el entorno de pruebas.
- [ ] He leído la directiva ética.
