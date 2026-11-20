# Architecture Specification: Enterprise IT Support & Resolution Agent

**Document Version:** 1.0.0  
**Status:** Verified Architecture  
**Target Runtime:** Python 3.12, FastAPI, LangGraph, SQLite, FAISS, Sentence-Transformers  

---

## 1. Overview & Core Purpose

The **Enterprise IT Support & Resolution Agent** is an automated Tier-1 technical support system designed to handle internal IT requests—such as VPN connection failures, password reset procedures, account lockout status inquiries, device connectivity verification, and incident ticket creation—while enforcing strict deterministic routing, cross-user authorization, grounded knowledge retrieval, and human escalation boundaries.

### Key Architectural Tenets
1. **Deterministic Guardrails Over Raw LLM Generation**: Critical security events (credential compromise, phishing), escalation triggers (persistent troubleshooting failures), and state changes (ticket submission) are governed by deterministic validation and graph routing rules rather than unconstrained model predictions.
2. **Zero-Trust Identity & Authorization**: User identity is derived strictly from verified credentials (API key or Bearer token). The application enforces data ownership boundaries, prohibiting cross-user ticket lookups, device status queries, or account modifications.
3. **Hybrid RAG with Re-ranking**: Combines dense vector retrieval (FAISS with OpenAI embeddings) and sparse lexical retrieval (BM25Okapi) using Reciprocal Rank Fusion (RRF), followed by a local Cross-Encoder re-ranker to maximize contextual precision.
4. **Observable & Non-Masked Execution**: Comprehensive end-to-end telemetry (JSONL events, Prometheus exposition, latency histograms, token accounting) ensures that tool-level business failures are never masked as workflow successes.

---

## 2. High-Level Architecture (HLD)

```text
                                  +---------------------------------------+
                                  |     Authenticated Client / Frontend   |
                                  +---------------------------------------+
                                                      |
                                                      | HTTP POST /api/v1/support
                                                      | (X-API-Key / Authorization Bearer)
                                                      v
                                  +---------------------------------------+
                                  |         FastAPI REST Gateway          |
                                  | - Request ID & Metrics Initialization |
                                  | - Token & Identity Verification       |
                                  +---------------------------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |     LangGraph State Machine Engine    |
                                  +---------------------------------------+
                                                      |
                                                      v
                                            [understand_request]
                                      (OpenAI Structured Output + Rules)
                                                      |
                                                      v
                                               [route_request]
                                        (Deterministic Edge Evaluator)
                                                      |
         +-------------------+-----------------+------+----------------+--------------------+
         |                   |                 |                       |                    |
         v                   v                 v                       v                    v
  [knowledge_node]    [rag_tool_node]     [tool_node]            [action_node]      [escalation_node]
   (General KB)       (Troubleshooting)  (Read-Only DB)         (State Mutation)     (Deterministic)
         |                   |                 |                       |                    |
         +---------+---------+                 |                       |                    |
                   |                           |                       |                    |
                   v                           v                       v                    v
         +-------------------+       +-------------------+   +------------------+   +---------------+
         |  Hybrid RAG Engine|       | Enterprise Tools  |   | SQLite Database  |   | Support Team  |
         | - FAISS Dense     |       | - ACCOUNT_STATUS  |   | (Employees,      |   | Notification  |
         | - BM25 Sparse     |       | - DEVICE_STATUS   |   |  Accounts,       |   | & Escalation  |
         | - RRF Fusion      |       | - TICKET_LOOKUP   |   |  Devices,        |   | Flagging      |
         | - Cross-Encoder   |       | - PASSWORD_RESET  |   |  Tickets)        |   +---------------+
         +-------------------+       +-------------------+   +------------------+           |
                   |                           |                       |                    |
                   +---------------------------+-----------------------+                    |
                                               |                                            |
                                               v                                            |
                                     [Response Synthesis]                                   |
                                 (Grounded Citations & Error Handling)                      |
                                               |                                            |
                                               +--------------------------------------------+
                                               |
                                               v
                                   [JSON API Response Payload]
```

---

## 3. Low-Level Design (LLD)

### 3.1 LangGraph State & Execution Flow

The workflow state is defined by the `AgentState` TypedDict (`app/agent/state.py`):

```python
class AgentState(TypedDict, total=False):
    request_id: str                   # Correlated request identifier (REQ-...)
    user_id: str | None               # Verified identity from authentication
    query: str                        # Raw incoming user request
    intent: str | None                # Classified intent (e.g., VPN_TROUBLESHOOTING)
    entities: dict[str, Any]          # Extracted parameters (ticket_id, category, etc.)
    route: str | None                 # Selected routing branch
    retrieved_context: list[dict]     # Formatted RAG evidence chunks with metadata
    tool_calls: list[dict]            # History of executed tool calls
    tool_results: list[dict]          # Tool execution responses and statuses
    validation_errors: list[str]      # Parameter or business validation issues
    retry_count: int                  # Retries consumed during execution
    response: str | None              # User-facing synthesized answer
    status: str | None                # Terminal or intermediate workflow status
    escalation_required: bool         # Boolean flag indicating human Tier-2 requirement
```

#### Node Graph Construction
1. `understand_request`: Invokes OpenAI structured response parsing combined with post-processing pattern matching. Ensures queries with ticket IDs route to lookup, creation verbs route to ticket creation, and security risks flag escalation.
2. `route_request`: Maps the classified intent and query attributes to an explicit graph node:
   * `KNOWLEDGE` -> `knowledge_node`
   * `VPN_TROUBLESHOOTING` -> `rag_tool_node`
   * `PASSWORD_RESET` -> `rag_tool_node`
   * `ACCOUNT_STATUS`, `DEVICE_STATUS`, `TICKET_LOOKUP` -> `tool_node`
   * `CREATE_TICKET` -> `action_node`
   * `ESCALATION` -> `escalation_node`
   * `CLARIFICATION` / Fallback -> `clarification_node`
3. `tool_node`: Executes read-only enterprise tools with cross-user ownership verification.
4. `action_node`: Validates input parameters (`user_id`, `category`, `priority`, `description`), normalizes category and priority enums, executes ticket creation in SQLite, and returns `ACTION_FAILED` if insertion fails.
5. `escalation_node`: Deterministically marks the workflow as escalated and logs an audit record.
6. `clarification_node`: Outlines specific missing parameters to guide user clarification.

---

### 3.2 Hybrid Retrieval-Augmented Generation (RAG) Pipeline

The RAG subsystem (`app/rag/`) enforces high-precision grounding over local markdown documentation:

```text
Query: "How do I connect to the corporate VPN?"
  |
  +---> Dense Retrieval (FAISS) 
  |     - Query embedded via text-embedding-3-small (1536 dim)
  |     - L2 normalized inner-product search (top-10 candidates)
  |
  +---> Sparse Retrieval (BM25)
  |     - Regex alphanumeric tokenization
  |     - BM25Okapi scoring over chunk tokens (top-10 candidates)
  |
  +---> Reciprocal Rank Fusion (RRF)
  |     - Formula: RRF_score(d) = SUM( 1 / (60 + rank_i(d)) )
  |     - Merges vector similarity with keyword matches (top-10 fused)
  |
  +---> Cross-Encoder Re-ranking
  |     - Pre-trained cross-encoder/ms-marco-MiniLM-L-6-v2
  |     - Joint query-document attention scoring
  |     - Produces final Top-5 reranked chunks with source citations
  |
  v
Grounded Context Injection with Source Attribution -> LLM Response Synthesis
```

---

### 3.3 Data Layer & Entity Relationships

The relational data model is maintained in SQLite (`app/models/database_models.py`):

```text
 +-----------------------------------+
 |             employees             |
 +-----------------------------------+
 | user_id (PK, String(20))          | <------+ (1:1)
 | name (String(100))                |        |
 | email (String(150), Unique)       |        |
 | department (String(100))          |        |
 | role (String(100))                |        |
 | status (String(30))               |        |
 | device_id (FK -> devices)         |        |
 +-----------------------------------+        |
        |                         |           |
        | (1:N)                   | (1:1)     |
        v                         v           |
 +-------------------+    +----------------+  |
 |      tickets      |    |    accounts    |  |
 +-------------------+    +----------------+  |
 | ticket_id (PK)    |    | user_id (PK,FK)|--+
 | user_id (FK)      |    | status         |
 | category          |    | locked (Bool)  |
 | priority          |    | mfa_enabled    |
 | description       |    | failed_attempts|
 | status            |    | password_change|
 | created_at        |    +----------------+
 | updated_at        |
 +-------------------+
```

---

### 3.4 Observability Architecture

Observability is instrumented throughout the application lifecycle:
* **Request Lifecycle Correlator**: Each API invocation receives a unique `REQ-[12 HEX]` identifier recorded across all log events, Prometheus measurements, and response headers.
* **Structured Event Logging**: Synchronous rotating JSONL log files (`logs/observability.jsonl`) capture payloads, tokens, latencies, and tool outcomes with sensitive credential redaction.
* **Prometheus Metrics Engine**:
  * Counters: `http_requests_total`, `llm_calls_total`, `tool_calls_total`, `llm_tokens_total`.
  * Histograms: `http_request_duration_seconds`, `agent_node_duration_seconds`, `retrieval_duration_seconds`, `llm_call_duration_seconds`, `tool_call_duration_seconds`.
* **In-Memory Analytics Aggregator**: In-memory statistics (`/api/v1/metrics`) providing rolling mean, min, max, P50, P90, P95, and P99 metrics for dashboard integration.
