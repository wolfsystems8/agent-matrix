---
name: web-api-dast
description: Prueba dinámicamente cabeceras HTTP, CORS, cookies y APIs REST/GraphQL (BOLA, rate limiting, mass assignment). Usar con la aplicación ejecutándose en el sandbox y autorización vigente.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 2
  authority: sandbox
---

# Web & API DAST

## Overview

Auditoría dinámica desde la perspectiva de un navegador o cliente HTTP. Genera
`reports/WEB_DAST_REPORT.md` con hallazgos reproducibles. El checklist completo
está en el agente `web-dast-tester`.

## When to use

- La app está levantada en el sandbox y responde en `http://target-app:8080`.
- Hay que validar cabeceras, CORS, cookies o endpoints de API.
- Se sospecha BOLA/IDOR, abuso de rate limiting o mass assignment.

## Workflow

1. Comprueba `SANDBOX_STATUS.md` y define la URL base interna.
2. Revisa cabeceras de seguridad y su valor real (CSP, HSTS, XFO, nosniff,
   Referrer-Policy, Permissions-Policy).
3. Analiza cookies (`HttpOnly`, `Secure`, `SameSite`) y CORS con un `Origin`
   no confiable.
4. Sondea rutas sensibles (`.git`, `.env`, backups, Swagger/OpenAPI, actuator)
   y confirma el contenido antes de reportar.
5. Prueba APIs: BOLA con dos cuentas, auth/rate limiting, límites de paginación
   y subida, mass assignment, introspección GraphQL.
6. Registra cada hallazgo `W-NN` con request/response sanitizados y remediación.

## Salida

`reports/WEB_DAST_REPORT.md`.

## Reglas

- Solo `target-app` dentro de `sandbox_net`; sin scanners masivos ni DoS.
- Máximo 20 req/s y timeouts explícitos.
- No alteres datos de forma persistente; usa cuentas y datos de prueba.
- Sanitiza tokens, cookies y PII en la evidencia.
