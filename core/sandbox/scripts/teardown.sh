#!/usr/bin/env sh
# Cierre obligatorio del sandbox al terminar una fase o el pipeline.
#
# Uso (desde el host, con Docker disponible):
#   sh core/sandbox/scripts/teardown.sh
#
# Deja el entorno como estaba: sin contenedores, redes ni volúmenes del
# proyecto, y sin imágenes/contenedores temporales de PoC. Las PoC deben
# nombrarse `secmatrix-poc-*` para que este script las recoja.
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COMPOSE_FILE=${COMPOSE_FILE:-"$HERE/../docker-compose.sandbox.yml"}
PROJECT=${COMPOSE_PROJECT_NAME:-sec-agent-matrix}

if ! command -v docker >/dev/null 2>&1; then
  echo "teardown: docker no disponible; nada que cerrar" >&2
  exit 0
fi

echo "== bajando el stack (contenedores, redes y volúmenes) =="
docker compose -f "$COMPOSE_FILE" down -v --remove-orphans

echo "== contenedores temporales de PoC =="
ids=$(docker ps -aq --filter "name=secmatrix-poc-" || true)
if [ -n "$ids" ]; then
  # shellcheck disable=SC2086
  docker rm -f $ids
else
  echo "ninguno"
fi

echo "== imágenes temporales de PoC =="
images=$(docker images -q --filter "reference=secmatrix-poc-*" || true)
if [ -n "$images" ]; then
  # shellcheck disable=SC2086
  docker rmi -f $images
else
  echo "ninguna"
fi

echo "== verificación =="
remaining=$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT" | wc -l | tr -d ' ')
if [ "$remaining" != "0" ]; then
  echo "teardown: quedan $remaining contenedor(es) del proyecto" >&2
  exit 1
fi
if docker network inspect "${PROJECT}_sandbox_net" >/dev/null 2>&1; then
  echo "teardown: la red ${PROJECT}_sandbox_net sigue existiendo" >&2
  exit 1
fi

echo "teardown: OK — stack, volúmenes, redes y PoC temporales eliminados"
