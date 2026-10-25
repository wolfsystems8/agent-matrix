# Plantilla Estándar de Reporte de Vulnerabilidades (CVSS v3.1)

## Tabla de hallazgos

| ID | Metodología / Módulo | Componente / Línea | Vulnerabilidad (CWE) | Vector STRIDE | CVSS v3.1 | Severidad | Estado Sandbox |
|---|---|---|---|---|---|---|---|
| V-01 | SAST | `src/auth.js:42` | SQL Injection (CWE-89) | Tampering | 9.8 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | 🔴 Crítica | Pendiente |
| V-02 | DAST | `GET /api/users/1` | BOLA / IDOR (CWE-639) | Elevation of Privilege | 8.1 `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` | 🟠 Alta | Confirmado |

## Escala de severidad

| CVSS v3.1 | Severidad | SLA sugerido |
|-----------|-----------|--------------|
| 9.0 – 10.0 | 🔴 Crítica | 24 h |
| 7.0 – 8.9 | 🟠 Alta | 7 días |
| 4.0 – 6.9 | 🟡 Media | 30 días |
| 0.1 – 3.9 | 🔵 Baja | 90 días |
| 0.0 | ⚪ Informativa | Backlog |

## Detalle técnico (repetir por hallazgo)

### V-01 — SQL Injection en autenticación

- **Ubicación:** `src/auth.js:42`
- **CWE / Categoría:** CWE-89 — Improper Neutralization of Special Elements used in an SQL Command
- **Vector STRIDE:** Tampering
- **CVSS v3.1:** `9.8` — `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
- **Descripción:** La consulta se construye por concatenación con el parámetro
  `email`, lo que permite alterar la cláusula `WHERE` y autenticarse sin
  credenciales válidas.
- **Evidencia:** request/respuesta sanitizada o fragmento de código.
- **Impacto:** lectura/escritura no autorizada en la base de datos.
- **Remediación sugerida:** usar consultas preparadas con parámetros
  vinculados; validar el esquema de entrada con Zod/Joi.
- **Estado sandbox:** Pendiente / Confirmado / Mitigado / Falso positivo.
- **Referencias:** OWASP ASVS 5.3.4, OWASP Top 10 A03:2021.

## Reglas de redacción

1. Un hallazgo por sección, con ID estable (`V-01`, `V-02`, …).
2. No incluir secretos reales ni datos personales; enmascarar.
3. Todo hallazgo Confirmado debe incluir una PoC reproducible o evidencia.
4. Todo hallazgo debe incluir una remediación concreta y verificable.
5. Los falsos positivos se documentan y se justifican, no se eliminan sin rastro.
