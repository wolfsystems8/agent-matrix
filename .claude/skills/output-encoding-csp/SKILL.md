---
name: output-encoding-csp
description: "Verifica la codificación de salida específica por contexto (dentro de HTML, dentro de script, en JSON, en URL y en CSS) y clasifica la Content Security Policy en sus 4 niveles. Usar al revisar defensas contra XSS o cabeceras de seguridad."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Codificación por contexto y CSP

## Overview

Buenas prácticas operacionales contra XSS: cada salida se codifica según el
contexto que la interpreta, y la CSP limita el daño si algo se escapa. Lo
ejecuta `output-encoding-csp-reviewer` → `reports/ENCODING_CSP_REVIEW.md`.

## When to use

- Tras encontrar XSS, para definir la corrección exacta.
- Al revisar plantillas, serialización JSON o cabeceras HTTP.

## Workflow

1. **Codificación por contexto:**

   | Contexto | Regla |
   |----------|-------|
   | Dentro de HTML | Entidades HTML (autoescape) |
   | Atributo HTML | Codificación de atributo + comillas |
   | Dentro de script | No interpolar; pasar datos por JSON/`data-*` y `textContent` |
   | Respuesta JSON | `application/json`, serializador, sin JSONP; `<` si va embebido en HTML |
   | URL | `encodeURIComponent` del parámetro + allowlist de esquemas |
   | CSS | Escape hexadecimal CSS o no insertar datos |

2. **CSP en 4 niveles:**

   | Nivel | Descripción |
   |-------|-------------|
   | 0 | Ausente o solo `Report-Only` |
   | 1 | Allowlist de dominios con `unsafe-inline`/`unsafe-eval` |
   | 2 | Nonce o hash, sin `unsafe-inline` |
   | 3 | Estricta: nonce/hash + `strict-dynamic`, `object-src 'none'`, `base-uri 'none'`, Trusted Types |

3. Propón la política objetivo (nivel 3) adaptada a la aplicación.

## Reglas

- La CSP es defensa en profundidad: no cierra un XSS por sí sola.
- Solo lectura; escribe únicamente en `reports/`.
