---
name: injection-xss-analysis
description: Detecta SQLi (union, error, boolean blind, time based) y XSS (reflected, stored, DOM) en el código con la línea exacta, analiza patrones como concatenación o validación solo en cliente y evalúa filtros frente a técnicas de evasión. Usar cuando hay consultas SQL o salida HTML/JS.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Análisis de SQLi y XSS

## Overview

Encuentra inyecciones SQL y XSS rastreando cada dato no confiable desde su
fuente hasta el sink, con archivo y línea exacta, el tipo explotable y la
corrección. Lo ejecutan `attack-surface-mapper`, `sqli-analyst` y
`xss-analyst`.

## When to use

- El código construye consultas SQL o genera HTML/JS con datos de usuario.
- Un SAST genérico marcó inyecciones y hace falta clasificarlas por tipo.
- Se quiere saber si un filtro o WAF casero protege de verdad.

## Workflow

1. **Superficie.** `attack-surface-mapper` → `reports/ATTACK_SURFACE.md` con
   los vectores (entradas de usuario, parámetros HTTP, vectores de carga, APIs,
   datos estructurados) y su exposición.
2. **Patrones de riesgo** a buscar en cada flujo:
   - Concatenación de cadenas hacia SQL o HTML.
   - Falta de validación de entrada en el servidor.
   - Confianza en la validación del cliente.
   - Filtros por lista negra.
3. **SQLi.** `sqli-analyst` → `reports/SQLI_FINDINGS.md`:

   | Tipo | Se da cuando… |
   |------|---------------|
   | Union based | El resultado de la consulta se muestra |
   | Error based | Los errores del motor llegan al cliente |
   | Boolean blind | La respuesta cambia con verdadero/falso |
   | Time based | Solo el tiempo de respuesta varía |

4. **XSS.** `xss-analyst` → `reports/XSS_FINDINGS.md`:

   | Tipo | Flujo |
   |------|-------|
   | Reflected | Parámetro → misma respuesta |
   | Stored | Dato persistido → otra respuesta |
   | DOM based | Fuente del navegador → sink JS |

5. **Evasión.** Para cada filtro existente, evalúa si resiste las familias de
   evasión de OWASP (mayúsculas, codificaciones múltiples, comentarios,
   eliminación no recursiva, etiquetas/eventos alternativos, mXSS). Un filtro
   que no resiste es "No efectivo"; la corrección es parametrizar o codificar
   por contexto.

## Reglas

- Análisis estático y de solo lectura: la verificación dinámica es de
  `web-api-dast` en el sandbox.
- Se describen técnicas de evasión para evaluar defensas, sin payloads armados
  ni de extracción de datos.
- Cada hallazgo lleva archivo:línea, fragmento breve, tipo, CWE y corrección.
