---
name: network-tls-audit
description: "Audita puertos, servicios, banners, protocolos TLS y certificados dentro del sandbox. Usar para revisar la superficie de red, servicios expuestos y fortaleza del cifrado."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 2
  authority: sandbox
---

# Network & TLS Audit

## Overview

Descubre la superficie de red del sandbox y evalúa servicios y transporte. El
detalle de comandos y el formato de reporte están en el agente
`network-auditor`.

## When to use

- La aplicación expone puertos o servicios de infraestructura.
- Hay que verificar TLS, certificados o servicios de datos accesibles.
- Antes de un DAST, para conocer los endpoints reales.

## Workflow

1. Resuelve hosts y subred desde `pentest-runner`; no salgas de `sandbox_net`.
2. Escanea TCP completo (`nmap -sT -sV -p-`) y UDP más comunes.
3. Identifica versiones/banners y servicios innecesarios u obsoletos.
4. Audita TLS (`ssl-enum-ciphers`, `sslyze`, `openssl`): protocolos obsoletos,
   suites débiles, validez y cadena del certificado.
5. Comprueba servicios de datos/colas expuestos sin autenticación usando solo
   comandos de lectura (`PING`, `nc -z`).
6. Documenta evidencia (comando + salida) y remediación por hallazgo `N-NN`.

## Salida

`reports/NETWORK_AUDIT.md`.

## Reglas

- Sin escaneos fuera de `sandbox_net`.
- Sin DoS, flood, brute force ni exploits.
- No cambies configuración de red ni del compose.
