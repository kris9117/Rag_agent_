# REST API Reference: Enterprise IT Support Agent

**Base URL:** `http://127.0.0.1:8000`  
**API Version:** `v1`  
**Data Format:** `application/json`  

---

## 1. Authentication & Security Headers

All requests to `/api/v1/support` require authentication via an enterprise API key or Bearer token header.

### Supported Headers
* `X-API-Key: <token>`
* `Authorization: Bearer <token>`

### Preconfigured Demo Identities
The repository provides static demo credentials mapped to synthetic employees in `data/enterprise.db`:

| API Key / Bearer Token | Employee Identity | Role | Department | Description |
| :--- | :--- | :--- | :--- | :--- |
| `demo-key-emp0001` | `EMP0001` | `employee` | Engineering | Standard employee |
| `demo-key-emp0002` | `EMP0002` | `employee` | Finance | Standard employee |
| `demo-key-emp0003` | `EMP0003` | `employee` | IT | Standard employee |
| `demo-key-admin` | `ADMIN001` | `admin` | IT | IT Administrator (cross-user access permitted) |

*(Note: In `APP_ENV=development` and `APP_ENV=test`, if no header is supplied, the agent gracefully defaults to `EMP0001` for quick local testing. In `APP_ENV=production`, missing credentials return `401 Unauthorized`).*

---

## 2. Support Agent Endpoint

### `POST /api/v1/support`
Submit an enterprise IT support request for automated classification, knowledge retrieval, database lookup, or ticket generation.

#### Request Schema
```json
{
  "query": "string (min 3, max 2000 characters, required)",
  "user_id": "string (optional; must match authenticated user identity unless admin)"
}
```

#### Response Schema
```json
{
  "request_id": "string (format: REQ-XXXXXXXXXXXX)",
  "user_id": "string (effective authenticated employee identity)",
  "intent": "string (classified intent, e.g., VPN_TROUBLESHOOTING)",
  "route": "string (selected graph branch, e.g., RAG_TOOL)",
  "status": "string (execution status, e.g., RAG_COMPLETED, TOOL_COMPLETED, ACTION_COMPLETED, ACTION_FAILED, ESCALATION_REQUIRED, CLARIFICATION_REQUIRED)",
  "response": "string (user-facing synthesized response with citations or instructions)",
  "escalation_required": "boolean (true if Tier-2 human escalation was triggered)"
}
```

---

## 3. End-to-End Examples

### Example 1: VPN Troubleshooting (Hybrid RAG)

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/support" \
  -H "X-API-Key: demo-key-emp0001" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I connect to the corporate VPN?"}'
```

**Response (HTTP 200 OK):**
```json
{
  "request_id": "REQ-1A4FD11D7969",
  "user_id": "EMP0001",
  "intent": "VPN_TROUBLESHOOTING",
  "route": "RAG_TOOL",
  "status": "RAG_COMPLETED",
  "response": "To connect to the corporate VPN:\n1. Launch the enterprise VPN client.\n2. Enter your standard corporate credentials.\n3. Approve the push notification on your enrolled MFA authenticator device.\n\n**Sources:**\n- Remote Access Policy (ID: vpn_remote_access_policy)",
  "escalation_required": false
}
```

---

### Example 2: Account Status Lookup (Enterprise Tool)

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/support" \
  -H "X-API-Key: demo-key-emp0001" \
  -H "Content-Type: application/json" \
  -d '{"query": "Is my account locked?"}'
```

**Response (HTTP 200 OK):**
```json
{
  "request_id": "REQ-8E62886B2176",
  "user_id": "EMP0001",
  "intent": "ACCOUNT_STATUS",
  "route": "TOOL",
  "status": "TOOL_COMPLETED",
  "response": "Your account (EMP0001) is currently active and unlocked. Zero failed login attempts are recorded.",
  "escalation_required": false
}
```

---

### Example 3: Ticket Creation (State Mutation)

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/support" \
  -H "X-API-Key: demo-key-emp0001" \
  -H "Content-Type: application/json" \
  -d '{"query": "Create a high priority software ticket. Outlook keeps crashing when I open it."}'
```

**Response (HTTP 200 OK):**
```json
{
  "request_id": "REQ-3F20A7B1C944",
  "user_id": "EMP0001",
  "intent": "CREATE_TICKET",
  "route": "ACTION",
  "status": "ACTION_COMPLETED",
  "response": "Support ticket INC000051 has been created with High priority under category 'Software'. An IT specialist will review your request shortly.",
  "escalation_required": false
}
```

---

### Example 4: Explicit Human Escalation

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/support" \
  -H "X-API-Key: demo-key-emp0001" \
  -H "Content-Type: application/json" \
  -d '{"query": "Please escalate this issue to IT support immediately. It is still failing after troubleshooting."}'
```

**Response (HTTP 200 OK):**
```json
{
  "request_id": "REQ-AC1AECE87979",
  "user_id": "EMP0001",
  "intent": "ESCALATION",
  "route": "ESCALATION",
  "status": "ESCALATION_REQUIRED",
  "response": "This request requires escalation to the IT support team. A Tier-2 technician has been notified.",
  "escalation_required": true
}
```

---

### Example 5: Cross-User Identity Spoofing Blocked (Security Boundary)

**Request (User authenticated as EMP0001 attempting to act as EMP0002):**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/support" \
  -H "X-API-Key: demo-key-emp0001" \
  -H "Content-Type: application/json" \
  -d '{"query": "Is my account locked?", "user_id": "EMP0002"}'
```

**Response (HTTP 403 Forbidden):**
```json
{
  "detail": "Forbidden: Authenticated as EMP0001; cannot execute operations on behalf of EMP0002."
}
```

---

## 4. Health, Readiness & Metrics Endpoints

### `GET /health`
Liveness summary and environment information.

### `GET /health/live`
Container orchestrator (Kubernetes) liveness probe.
```json
{
  "status": "alive"
}
```

### `GET /health/ready`
Readiness probe verifying SQLite database connection and retrieval index availability. Returns HTTP 200 when ready or HTTP 503 when degraded.
```json
{
  "status": "ready",
  "details": {
    "database": "connected",
    "indexes": "ready"
  }
}
```

### `GET /metrics`
Standard Prometheus exposition format tracking HTTP traffic, LLM token consumption, latencies, and node timings.

### `GET /api/v1/metrics`
In-memory JSON analytics report detailing aggregated P50, P90, P95, and P99 latency percentiles, error rates, and total token usage.
