# Sandbox de verificación

Este directorio contiene el entorno aislado de la Fase 2.

## Arranque

```bash
docker compose -f core/sandbox/docker-compose.sandbox.yml up -d --build
docker compose -f core/sandbox/docker-compose.sandbox.yml \
  exec -T pentest-runner sh -lc '/scripts/wait_for_target.sh'
```

## Verificación de aislamiento

```bash
docker network inspect sec-agent-matrix_sandbox_net --format '{{.Internal}}'  # true
docker compose -f core/sandbox/docker-compose.sandbox.yml \
  exec -T pentest-runner sh -lc '/scripts/smoke_test.sh'
```

El script falla si hay egreso a Internet.

## Variables

| Variable | Default | Uso |
|----------|---------|-----|
| `TARGET_CONTEXT` | `../..` | Contexto de build de la app auditada |
| `TARGET_DOCKERFILE` | `Dockerfile` | Dockerfile de la app |
| `TARGET_PORT` | `8080` | Puerto publicado solo en `127.0.0.1` |
| `REPORTS_DIR` | `../../reports` | Volumen de reportes |

> En una instalación (`secmatrix install`), el instalador crea un `.env` en este
> directorio con `TARGET_CONTEXT=../../..` y `REPORTS_DIR=../../../reports`, que
> son las rutas correctas desde `.sec-agent-matrix/core/sandbox/` hasta la raíz
> del proyecto auditado. Compose carga ese `.env` automáticamente.

## Limpieza

```bash
docker compose -f core/sandbox/docker-compose.sandbox.yml down -v
```

## Límites

- La red `sandbox_net` es `internal: true`: sin salida a Internet.
- No uses `--privileged` ni montes `/var/run/docker.sock`.
- El puerto del objetivo se publica solo en loopback.
- Si tu app escucha en otro puerto, ajusta el mapeo y la URL base de los agentes.
