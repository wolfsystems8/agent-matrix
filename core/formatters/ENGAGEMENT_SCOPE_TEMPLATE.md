# Alcance y autorización del engagement

> Completar antes de ejecutar cualquier prueba dinámica. Sin este archivo, la
> Fase 2 está bloqueada.

## 1. Identificación

| Campo | Valor |
|-------|-------|
| Proyecto / repositorio | |
| Propietario del sistema | |
| Responsable de la auditoría | |
| Fecha de autorización | |
| Ventana de pruebas | |
| Contacto de emergencia | |

## 2. Autorización

Declaración (marcar y firmar):

- [ ] Confirmo que soy propietario del sistema o tengo autorización escrita para
      auditarlo.
- [ ] Las pruebas se limitarán al entorno de sandbox definido en
      `docker-compose.sandbox.yml`.
- [ ] No se probarán sistemas, dominios ni IPs de terceros.
- [ ] No se realizarán pruebas destructivas ni de denegación de servicio.
- [ ] Los datos y secretos encontrados se tratarán de forma confidencial.

Firma / registro: ______________________________________________

## 3. Alcance técnico

| Elemento | Incluido | Notas |
|----------|----------|-------|
| Código fuente (SAST) | Sí | |
| Aplicación web (DAST) | Sí | |
| APIs REST/GraphQL | Sí | |
| Red y servicios del sandbox | Sí | |
| Infraestructura cloud | No | |
| Ingeniería social | No | |
| DoS / fuerza bruta | No | Prohibido |

## 4. Objetivos y exclusiones

- Objetivo principal:
- Componentes críticos:
- Excluidos explícitamente:

## 5. Datos de prueba

- Cuentas de prueba:
- Datos sintéticos permitidos:
- Prohibido: datos reales de clientes, PII, secretos de producción.

## 6. Criterios de parada

- Detección de tráfico fuera de `sandbox_net`.
- Indisponibilidad del objetivo.
- Acceso accidental a datos reales.
- Cualquier acción que pueda tener impacto fuera del sandbox.
