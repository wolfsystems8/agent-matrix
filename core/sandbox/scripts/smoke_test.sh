#!/usr/bin/env sh
# Comprobación de humo del aislamiento. Se ejecuta DENTRO de pentest-runner.
set -eu

echo "== interfaces =="
ip -o -f inet addr show

echo "== resolución interna =="
getent hosts target-app target-db

echo "== egreso a Internet (debe fallar) =="
if curl -sS --max-time 4 -o /dev/null https://example.com; then
  echo "EGRESS_OPEN" >&2
  exit 1
else
  echo "EGRESS_BLOCKED"
fi

echo "== objetivo =="
curl -sS -D - -o /dev/null --max-time 5 http://target-app:8080/ | head -n 20
