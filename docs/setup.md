# Local Setup & Verification Guide

This guide provides step-by-step instructions to clone, configure, build retrieval indexes, seed demo data, run tests offline, and start the Enterprise IT Support Agent locally.

---

## 1. Prerequisites

* **Operating System**: Linux, macOS, or Windows 10/11
* **Python Runtime**: Python 3.12 or newer
* **Package Manager**: `pip` (bundled with Python)
* **Git**: Installed and available in PATH
* **OpenAI API Key**: (Optional for tests/offline evaluation; required only for live model runs)

---

## 2. Clone & Environment Setup

### Step 1: Clone Repository
```powershell
git clone https://github.com/kris9117/Rag_agent_.git enterprise-it-support-agent
cd enterprise-it-support-agent
```

### Step 2: Create and Activate Virtual Environment
```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS (Bash)
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Pinned Dependencies
```powershell
# Install core runtime dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install testing and linting tools
pip install -r requirements-dev.txt
```

---

## 3. Configuration & Environment Variables

Create your local `.env` configuration file from the template:

```powershell
# Windows
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

### Configuration Variables Breakdown

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | `sk-...` | OpenAI API credential. Can be left empty for offline tests and mock evaluation. |
| `OPENAI_MODEL` | `gpt-5.6-luna` | Configured chat model (e.g. `gpt-4o-mini`, `gpt-4o`, `gpt-5.6-luna`). |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Dense embedding model used for FAISS vector search. |
| `APP_ENV` | `development` | Environment mode (`development`, `test`, `production`). In production, auth headers are strictly required. |
| `LOG_LEVEL` | `INFO` | Console and file logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `LANGSMITH_TRACING` | `false` | Enable LangChain / LangSmith trace export (optional). |
| `LANGSMITH_API_KEY` | *(None)* | LangSmith API key (optional). |
| `LANGSMITH_PROJECT` | `enterprise-it-support-agent` | LangSmith project namespace. |

---

## 4. Initialize Database & Seed Demo Data

The application uses an embedded SQLite database populated with synthetic employees, accounts, laptops, and sample tickets:

```powershell
python scripts/seed_database.py
```

* Output location: `data/enterprise.db`
* Seed contents: 50 synthetic enterprise employees (`EMP0001` - `EMP0050`), corporate devices (`DEV0001` - `DEV0050`), security accounts with MFA settings, and initial tickets.

---

## 5. Build Knowledge Retrieval Indexes

Before running RAG queries or the application, compile the markdown policies (`data/knowledge_base/`) into the dense vector index and sparse lexical index:

```powershell
# Build both FAISS and BM25 indexes with a single command
python scripts/build_indexes.py
```

* **Dense FAISS index**: `data/index/faiss.index` (1536-dimensional L2-normalized vectors)
* **Chunk metadata**: `data/index/chunks.json`
* **Sparse BM25 index**: `data/index/bm25.json`

*(Note: Pre-built demo index files are included in the repository so you can start querying immediately without rebuilding unless you modify the knowledge base).*

---

## 6. Running Tests & Coverage

The test suite runs **100% offline** by default using test doubles, in-memory SQLite isolation, and network guards that block accidental OpenAI API calls:

```powershell
# Run the complete test suite (46 tests)
pytest -v

# Run with test coverage measurement
pytest -v --cov=app --cov-report=term-missing
```

---

## 7. Running Evaluation & Benchmarks

### Offline Evaluation (Zero API Cost)
Run all 12 support scenarios through the agent workflow:

```powershell
# Execute offline evaluation
python evaluation/run_evaluation.py --mode mock

# Calculate accuracy, routing, and recall metrics
python evaluation/calculate_metrics.py
```

### Reproducible Performance Benchmark
```powershell
# Run benchmark in safe mock mode (1 cold + 5 warm iterations)
python evaluation/run_performance_benchmark.py --mode mock --iterations 5
```

---

## 8. Starting the Web API

Launch the FastAPI application using Uvicorn:

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Once running:
* **Interactive OpenAPI Documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Interface**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **Liveness Probe**: [http://127.0.0.1:8000/health/live](http://127.0.0.1:8000/health/live)
* **Readiness Probe**: [http://127.0.0.1:8000/health/ready](http://127.0.0.1:8000/health/ready)
* **Prometheus Metrics**: [http://127.0.0.1:8000/metrics](http://127.0.0.1:8000/metrics)
