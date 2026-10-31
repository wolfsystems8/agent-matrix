---
name: web-vuln-identification
description: "Identifica los vectores de ataque y a qué vulnerabilidades web está expuesto el software (XSS, SQLi, fuerza bruta, path traversal, CSRF), con los fundamentos de cada una y la línea exacta. Usar para una clasificación completa de la exposición web."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Identificación de vulnerabilidades web

## Overview

Responde "¿a qué está expuesta esta aplicación web?" con técnicas de
identificación sobre el código: inventario de vectores, rastreo fuente → sink y
clasificación por tipo. Lo ejecutan `attack-surface-mapper` y
`web-vuln-analyst`; SQLi y XSS se delegan a `injection-xss-analysis`.

## When to use

- Antes de un pentest web, para dirigirlo.
- Cuando el usuario pide "qué vulnerabilidades tiene esta web/API".
- Al revisar autenticación, descarga/subida de ficheros o formularios.

## Workflow

1. **Vectores de ataque** (`attack-surface-mapper`):

   | Categoría | Ejemplos |
   |-----------|----------|
   | Entradas de usuario | Formularios, búsquedas, perfiles |
   | Parámetros HTTP | Query, cuerpo, path, cabeceras, cookies |
   | Vectores de carga | Uploads, multipart, comprimidos |
   | APIs | REST, GraphQL, WebSocket, webhooks |
   | Datos estructurados | JSON, XML, YAML, CSV, objetos serializados |

2. **Técnicas de identificación:** búsqueda de sinks peligrosos, rastreo
   fuente → sink, revisión de validación (servidor vs. solo cliente),
   comparación con requisitos (`SR-NN`) y con OWASP ASVS.
3. **Clasificación de exposición** por vector: XSS, SQLi, fuerza bruta, path
   traversal, CSRF u otros.
4. **Fundamentos por tipo** (`web-vuln-analyst` → `reports/WEB_VULN_FINDINGS.md`):

   | Tipo | Causa raíz | Control correcto |
   |------|-----------|------------------|
   | Fuerza bruta | Intentos ilimitados, errores distinguibles | Rate limiting, bloqueo, MFA, hash lento |
   | Path traversal | Ruta construida con datos del usuario | Ruta canónica bajo directorio base, allowlist |
   | CSRF | Estado cambiado con cookie sin prueba de intención | Token, `SameSite`, verificación de `Origin` |
   | SQLi | Concatenación en SQL | Consultas parametrizadas |
   | XSS | Salida sin codificación por contexto | Autoescape, codificación por contexto, CSP |

## Reglas

- Solo lectura; escribe únicamente en `reports/`.
- Un vector sin sink identificado es un supuesto, no un hallazgo.
- Cada hallazgo indica archivo:línea, vector, CWE y corrección.
