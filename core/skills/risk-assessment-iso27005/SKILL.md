---
name: risk-assessment-iso27005
description: Identifica, analiza, evalúa y propone tratamiento de riesgos según ISO/IEC 27005 y genera una tabla de riesgos ordenada por severidad con recomendaciones. Usar tras un SAST/pentest o cuando el usuario pide una matriz o registro de riesgos.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Evaluación y tratamiento de riesgos (ISO/IEC 27005)

## Overview

Convierte hallazgos técnicos (`V-NN`, `W-NN`, `N-NN`) y de proceso (`P-NN`) en
riesgos `R-NN` con probabilidad, impacto, nivel, opción de tratamiento y
recomendación. El detalle operativo está en el agente `risk-assessor`.

## When to use

- Hay reportes de auditoría y hace falta priorizarlos por riesgo de negocio.
- El usuario pide "matriz de riesgos", "registro de riesgos", "tratamiento de
  riesgos" o "ISO 27005".
- Antes de decidir qué corregir primero.

## Workflow

1. **Contexto.** Define activos (datos, credenciales, servicios, disponibilidad)
   y criterios de aceptación: `Bajo` se puede retener; el resto se trata o se
   acepta de forma explícita.
2. **Identificación.** Para cada hallazgo construye el escenario
   activo → amenaza → vulnerabilidad → consecuencia y marca la dimensión CIA.
   Agrupa los hallazgos que materializan el mismo escenario en un solo riesgo.
3. **Análisis.** Probabilidad e impacto de 1 a 5, cada uno con su justificación.
   Un hallazgo confirmado en sandbox sube la probabilidad un nivel.
4. **Evaluación.** Puntuación = P × I. Crítico 20–25 · Alto 12–19 ·
   Medio 6–11 · Bajo 1–5.
5. **Tratamiento.** Modificar, Retener, Evitar o Compartir, con el control de
   ISO/IEC 27001:2022 Anexo A y el riesgo residual esperado.
6. **Ordena** de mayor a menor puntuación y escribe `reports/RISK_REGISTER.md`
   con matriz de calor, registro y recomendaciones agrupadas por nivel.

## Ejemplo de fila

```markdown
| R-01 | Exfiltración de la BD por SQLi | Datos de clientes | C, I | V-02, W-01 | 5 | 5 | 25 | Crítico | Modificar | A.8.28 Codificación segura | Bajo | Confirmado |
```

## Reglas

- Sin evidencia no hay riesgo: una hipótesis se registra como tal.
- No apliques tratamientos; solo recomiéndalos. La decisión es del usuario.
- Escribe únicamente en `reports/`.
