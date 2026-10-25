# Sandbox de verificación

Este directorio contiene el entorno aislado de la Fase 2.

## Arranque

```bash
docker compose -f core/sandbox/docker-compose.sandbox.yml up -d --build
docker compose -f core/sandbox/docker-compose.sandbox.yml \
  exec -T pentest-runner sh -lc '/scripts/wait_for_target.sh'
```

Sin configuración adicional se levanta `demo-target`, un objetivo de
demostración con vulnerabilidades intencionadas (SQLi, XSS reflejado, IDOR,
fuga de configuración, errores verbosos). Sirve para validar el pipeline y
para que los agentes tengan material real; **no lo uses como base de nada
productivo**.

### Auditar una app propia

Crea `core/sandbox/.env` (o exporta las variables) apuntando a tu proyecto:

```ini
TARGET_CONTEXT=/ruta/a/mi-app
TARGET_DOCKERFILE=Dockerfile
TARGET_PORT=8080
```

La app debe escuchar en `0.0.0.0:8080` dentro del contenedor. Si usa otro
puerto, ajusta el mapeo en el compose y la URL base de los agentes.

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
| `TARGET_CONTEXT` | `./demo-target` | Contexto de build de la app auditada |
| `TARGET_DOCKERFILE` | `Dockerfile` | Dockerfile de la app |
| `TARGET_PORT` | `8080` | Puerto publicado solo en `127.0.0.1` |
| `REPORTS_DIR` | `../../reports` | Volumen de reportes |

> En una instalación (`secmatrix install`), el instalador crea un `.env` en este
> directorio con `REPORTS_DIR=../../../reports`, que es la ruta correcta desde
> `.sec-agent-matrix/core/sandbox/` hasta los reportes del proyecto. Si el
> proyecto auditado tiene un `Dockerfile` en su raíz, añade también
> `TARGET_CONTEXT=../../..`. Compose carga ese `.env` automáticamente.

## Limpieza

```bash
docker compose -f core/sandbox/docker-compose.sandbox.yml down -v
```

## Límites

- La red `sandbox_net` es `internal: true`: sin salida a Internet.
- El objetivo no publica puertos directamente (Docker no mapea puertos de
  contenedores conectados solo a una red interna). El servicio `target-edge`
  (socat) escucha en `127.0.0.1:$TARGET_PORT` y solo reenvía a
  `target-app:8080`, así que el objetivo sigue sin ruta a Internet.
- No uses `--privileged` ni montes `/var/run/docker.sock`.
- Si tu app escucha en otro puerto, ajusta el mapeo y la URL base de los agentes.
