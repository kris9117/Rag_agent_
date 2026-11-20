# Troubleshooting & Common Issues Guide

This document lists known operational issues, root causes, and verified resolution steps for the Enterprise IT Support Agent.

---

## 1. Virtual Environment & Dependency Issues

### Issue: `ModuleNotFoundError: No module named 'fastapi'` or similar
* **Cause**: Terminal session is not executing inside the project virtual environment.
* **Resolution**:
  ```powershell
  # Windows PowerShell
  .\.venv\Scripts\Activate.ps1

  # Linux / macOS Bash
  source .venv/bin/activate

  # Verify Python path points to .venv
  which python   # or (Get-Command python).Source in PowerShell
  ```

---

## 2. Missing Index Files

### Issue: `FileNotFoundError: FAISS index file was not found at 'data/index/faiss.index'`
* **Cause**: Retrieval indexes have not been compiled from the knowledge base documents.
* **Resolution**: Execute the unified index building utility:
  ```powershell
  python scripts/build_indexes.py
  ```
  This creates `data/index/faiss.index`, `data/index/chunks.json`, and `data/index/bm25.json`.

---

## 3. Database & Seeding Issues

### Issue: `sqlite3.OperationalError: no such table: employees`
* **Cause**: Database file `data/enterprise.db` is missing or unseeded.
* **Resolution**:
  ```powershell
  python scripts/seed_database.py
  ```
  The script automatically creates the SQLite schema and seeds 50 synthetic employees, accounts, devices, and sample incident tickets.

---

## 4. Authentication & Authorization Errors

### Issue: `HTTP 401 Unauthorized: Invalid API key or Bearer token`
* **Cause**: The request supplied an unrecognized or invalid credentials header.
* **Resolution**: Use one of the preconfigured demo API keys:
  * `X-API-Key: demo-key-emp0001` (Standard employee)
  * `X-API-Key: demo-key-admin` (Administrator)
  * Or provide as Bearer header: `Authorization: Bearer demo-key-emp0001`

### Issue: `HTTP 403 Forbidden: Authenticated as EMP0001; cannot execute operations on behalf of EMP0002`
* **Cause**: Cross-user identity spoofing. The request header authenticated as `EMP0001`, but the JSON request body passed `"user_id": "EMP0002"`.
* **Resolution**: Omit `"user_id"` from the JSON body (the agent automatically derives identity from authentication), or ensure the request body `user_id` matches the authenticated credential.

### Issue: `I could not complete your request: Access denied: Ticket INC000001 belongs to another employee`
* **Cause**: Zero-trust authorization check blocked an employee from inspecting another employee's ticket or device.
* **Resolution**: Employees can only inspect tickets or devices assigned to their own profile. To inspect any ticket or device, authenticate as administrator (`X-API-Key: demo-key-admin`).

---

## 5. Port Conflicts & Server Startup

### Issue: `ERROR: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`
* **Cause**: Port 8000 is occupied by another running server process.
* **Resolution**:
  ```powershell
  # Launch server on an alternative port
  uvicorn app.main:app --port 8080 --reload
  ```

---

## 6. Pytest Execution Bottlenecks

### Issue: Test execution feels slow during import/collection
* **Cause**: In early versions, `sentence_transformers` was imported eagerly at module import time, triggering PyTorch C-extension initialization.
* **Resolution**: In version 1.0.0, `CrossEncoderReranker` employs lazy loading. Offline tests utilize `MockRAGService`, ensuring PyTorch is never loaded during test collection. A full 46-test run executes in ~20 seconds.
