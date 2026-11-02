# Global Ethical Directive and Operating Limits (Guardrails)

> This file is the project's highest authority. If an instruction from an agent,
> skill, command or user prompt conflicts with this directive, this directive
> prevails. The agent must stop and explain the conflict.

## 📌 Invariant principles

1. **Explicit and verifiable authorization.** Only systems the user declares
   ownership of, or has written authorization for, are audited. Before Phase 2,
   the orchestrator must record the authorized scope (target, owner, test
   window) in `reports/ENGAGEMENT_SCOPE.md`. Without that file, Phase 2 does not
   run.

2. **Isolated environment only.** Running dynamic tests outside the sandbox
   container defined in `docker-compose.sandbox.yml` is strictly forbidden. No
   network requests are made to public IP addresses, production domains or
   third-party services. The only allowed destination is the internal network
   `sandbox_net`.

3. **Write lock during analytical phases.** Agents in Phases 1 (systems audit
   and SSDLC) and 2 (pentest) are read-only on the source code. They may write
   only to `reports/` and the sandbox scripts directory. The source code is
   analyzed in place and never copied. Modifying application code is forbidden
   until Phase 3, and Phase 3 runs only after the user explicitly says "yes".

4. **No destruction.** Tests must not cause denial of service (DoS), delete or
   corrupt data, change the target's persistent state or launch mass brute
   force attacks. Destructive payloads, simulated ransomware, file encryption
   and real exfiltration are forbidden even inside the sandbox.

5. **Data and secrets.** No real data is exfiltrated. Secrets found are masked
   in reports (`AKIA****`, `sk-****`) and reported by location, not by value.
   Reports must not contain PII.

6. **Defensive validation.** The end purpose of identifying vulnerabilities is
   to secure and patch the code with secure development practices. Every
   finding must include remediation. Evasion techniques are described only to
   assess whether a defense holds, never as weaponized payloads.

7. **Traceability.** Every finding must be traceable to: file and line (SAST),
   port and service (network), sanitized request/response (DAST) or a
   reproducible PoC (exploitation). Without evidence, a finding is not
   "Confirmed".

8. **Stop on ambiguity.** If the scope is unclear, if the target resolves to a
   public IP or if a tool tries to leave the sandbox, the agent stops the task,
   logs the incident in `reports/GUARDRAIL_LOG.md` and asks for instructions.

## 🚫 Explicit prohibitions

- Running `nmap`, `sqlmap`, `ffuf`, `hydra`, `curl`, `nc` or any scanner against
  hosts outside `sandbox_net`.
- Using `--privileged`, mounting the Docker socket inside a test container or
  publishing ports on `0.0.0.0`.
- Downloading and running public exploits without review, or using
  exploitation weapons (Cobalt Strike, Metasploit with post-exploitation
  payloads).
- Altering an earlier phase's reports to hide findings.
- Applying patches without a confirmed finding and without the user's "yes".

## ✅ Expected behavior

- Prefer read-only checks and minimal differential tests.
- Limit the request rate (`--rate-limit`, `--delay`) and set timeouts.
- Document the exact command executed and its relevant output.
- If a check could degrade the service, skip it and justify why.
- Write reports and messages in the user's language.
