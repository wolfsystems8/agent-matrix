---
name: crypto-review
description: Reviews symmetric and asymmetric cryptography, password hashing, randomness, JWT, TLS and key management in code, with the exact line and the secure alternative. Use when the code encrypts, signs, hashes or generates tokens.
license: MIT
compatibility: codex, claude-code, cursor, opencode
metadata:
  phase: 1
  authority: read-only
---

# Cryptography review

## Overview

Applies cryptography fundamentals to real code: right primitive, right
configuration and protected keys. Run by `crypto-reviewer` →
`reports/CRYPTO_REVIEW.md`.

## When to use

- The code uses `cipher`, `encrypt`, `sign`, `hash`, `jwt`, `random`, `ssl`.
- Passwords are stored or tokens are generated.
- Secrets and key management are under review.

## Workflow

1. Inventory every cryptographic use with file:line.
2. **Symmetric:** AEAD (AES-GCM, ChaCha20-Poly1305), unique nonce, KDF-derived
   keys; detect ECB, CBC without MAC, fixed IV, obsolete algorithms.
3. **Asymmetric:** RSA ≥ 2048 with OAEP/PSS, ECDSA/Ed25519, certificate
   validation; detect PKCS#1 v1.5, `verify=False`, versioned private keys.
4. **Hashing:** Argon2id/bcrypt/scrypt for passwords; no MD5/SHA-1.
5. **Randomness:** CSPRNG for tokens and sessions.
6. **JWT and TLS:** pinned algorithm, `alg: none` rejected, TLS 1.2+.
7. **Keys:** source, rotation, per-environment separation; mask secrets.

## Rules

- Never copy keys or secrets into the report.
- Recommend maintained libraries, never home-made cryptography.
- Read-only; write only to `reports/`.
