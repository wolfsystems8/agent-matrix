---
name: threat-modeling
description: "Construye un modelo de amenazas STRIDE con fronteras de confianza, activos y amenazas priorizadas. Usar al diseñar un sistema, antes de un SAST o al revisar la arquitectura de autenticación y datos."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Threat Modeling (STRIDE)

## Overview

Produce `reports/THREAT_MODEL.md` a partir de la arquitectura real del
repositorio, aplicando STRIDE a cada flujo y priorizando por probabilidad e
impacto. El detalle operativo está en el agente `threat-modeler`.

## When to use

- Antes de una auditoría de código o de un pentest.
- Al diseñar un endpoint, flujo de autenticación o integración nueva.
- Cuando el usuario pregunta "¿qué puede salir mal?" o pide revisar fronteras de
  confianza.

## Workflow

1. Localiza puntos de entrada y activos: rutas, handlers, colas, cron, CLI,
   bases de datos, almacenamiento y terceros.
2. Dibuja un diagrama Mermaid con actores, componentes y fronteras de confianza.
3. Para cada flujo, recorre las seis categorías: Spoofing, Tampering,
   Repudiation, Information Disclosure, Denial of Service, Elevation of
   Privilege.
4. Registra para cada amenaza: control actual, control ausente, probabilidad,
   impacto y propuesta.
5. Marca explícitamente los supuestos y los vacíos de información; no inventes
   endpoints.

## Salida

`reports/THREAT_MODEL.md` con resumen, diagrama, matriz STRIDE, top amenazas y
supuestos.

## Reglas

- Solo lectura: no modifiques código ni configuración.
- No ejecutes pruebas dinámicas.
- Una amenaza sin evidencia se marca como hipótesis, no como hallazgo.
