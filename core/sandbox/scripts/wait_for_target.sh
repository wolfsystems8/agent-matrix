#!/usr/bin/env sh
# Espera a que target-app responda dentro de la red del sandbox.
set -eu

URL="${1:-http://target-app:8080}"
ATTEMPTS="${2:-30}"

i=1
while [ "$i" -le "$ATTEMPTS" ]; do
  if curl -fsS --max-time 3 -o /dev/null "$URL"; then
    echo "target ready: $URL"
    exit 0
  fi
  sleep 2
  i=$((i + 1))
done

echo "target NOT ready after $ATTEMPTS attempts: $URL" >&2
exit 1
