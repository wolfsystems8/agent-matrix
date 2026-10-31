---
name: crypto-review
description: "Revisa criptografía simétrica y asimétrica, hashing de contraseñas, aleatoriedad, JWT, TLS y gestión de claves en el código, con la línea exacta y la alternativa segura. Usar cuando el código cifra, firma, hashea o genera tokens."
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Revisión criptográfica

## Overview

Aplica los fundamentos de criptografía al código real: primitivo correcto,
configuración correcta y claves protegidas. Lo ejecuta `crypto-reviewer` →
`reports/CRYPTO_REVIEW.md`.

## When to use

- El código usa `cipher`, `encrypt`, `sign`, `hash`, `jwt`, `random`, `ssl`.
- Se almacenan contraseñas o se generan tokens.
- Se revisa la gestión de secretos y claves.

## Workflow

1. Inventaría cada uso criptográfico con archivo:línea.
2. **Simétrica:** AEAD (AES-GCM, ChaCha20-Poly1305), nonce único, claves de
   KDF; detecta ECB, CBC sin MAC, IV fijo, algoritmos obsoletos.
3. **Asimétrica:** RSA ≥ 2048 con OAEP/PSS, ECDSA/Ed25519, validación de
   certificados; detecta PKCS#1 v1.5, `verify=False`, claves privadas
   versionadas.
4. **Hashing:** Argon2id/bcrypt/scrypt para contraseñas; nada de MD5/SHA-1.
5. **Aleatoriedad:** CSPRNG para tokens y sesiones.
6. **JWT y TLS:** algoritmo fijado, `alg: none` rechazado, TLS 1.2+.
7. **Claves:** origen, rotación, separación por entorno; enmascara secretos.

## Reglas

- No copies claves ni secretos al reporte.
- Recomienda librerías mantenidas, nunca criptografía propia.
- Solo lectura; escribe únicamente en `reports/`.
