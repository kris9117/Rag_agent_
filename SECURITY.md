# Security Policy & Threat Model

**Project:** Enterprise IT Support & Resolution Agent  
**Maintained By:** Open Source Portfolio Showcase  

---

## 1. Supported Versions

| Version | Supported | Description |
| :--- | :--- | :--- |
| `1.0.x` | Yes | Active portfolio baseline with zero-trust authorization |
| `< 1.0.0` | No | Legacy audit and prototype revisions |

---

## 2. Threat Model & Security Boundaries

The Enterprise IT Support Agent operates in a simulated corporate environment. The threat model addresses the following core risks:

### A. Identity Spoofing & Impersonation
* **Threat**: A malicious or unauthorized user attempts to perform IT actions (e.g., ticket creation, account inspection) on behalf of another employee by specifying an arbitrary `user_id`.
* **Mitigation**: The application derives effective identity strictly from verified credentials (`X-API-Key` or `Authorization: Bearer`). If an incoming payload attempts to specify an identity different from the verified credential, the API gateway immediately halts processing with `HTTP 403 Forbidden`.

### B. Cross-User Data Access (IDOR)
* **Threat**: An employee attempts to view ticket details or hardware status belonging to a coworker (Insecure Direct Object Reference).
* **Mitigation**: The service layer enforces strict ownership validation against the SQLite database. Employees may only retrieve tickets or query devices assigned to their own identity. IT administrators (`ADMIN001`) are granted authorized bypass for support triage.

### C. Prompt Injection & Unconstrained Model Hallucination
* **Threat**: An attacker attempts to inject instructions via support queries to bypass routing, reveal system prompts, or execute arbitrary tools.
* **Mitigation**:
  * Critical routing (escalation, ticket creation) is enforced by deterministic regex and keyword rule-checkers.
  * Structured output extraction (`RequestUnderstanding`) guarantees the LLM outputs strictly validated Pydantic models.
  * Tools are executed solely through a hardened, static `TOOL_REGISTRY`. The agent cannot invoke shell commands, arbitrary Python code, or arbitrary database queries.

### D. Accidental Data Leakage & External API Overuse
* **Threat**: Unit tests or local scripts accidentally leak production credentials or trigger expensive paid API calls.
* **Mitigation**:
  * All unit and integration tests run offline using test doubles and explicit network guards (`block_openai_call`) that raise exceptions if network access is attempted.
  * Rotating JSONL event logs redact sensitive authentication tokens and raw payloads.

---

## 3. Synthetic Data Notice

All names, email addresses, employee identifiers, device hostnames, incident descriptions, and account credentials stored in `data/enterprise.db` and the evaluation dataset are **100% synthetic**. Any resemblance to real persons, active accounts, or corporate entities is purely coincidental.

---

## 4. Reporting Security Vulnerabilities

If you discover a security vulnerability or architectural flaw:
1. Please do **not** open a public issue on GitHub.
2. Submit a detailed report via GitHub Security Advisories or email the repository maintainer.
3. Include reproducible steps, sample curl payloads, and the affected version.
4. Vulnerability reports will be acknowledged and reviewed promptly.
