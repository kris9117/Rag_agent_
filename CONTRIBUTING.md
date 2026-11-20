# Contributing Guidelines

Thank you for your interest in contributing to the **Enterprise IT Support & Resolution Agent**!

This project serves as a reference-quality GenAI engineering portfolio demonstrating LangGraph orchestration, hybrid RAG, observability, and deterministic security guardrails.

---

## 1. Development Standards & Guiding Principles

1. **Deterministic Reliability First**: Prefer explicit guardrails, validated Pydantic schemas, and deterministic routing over unconstrained model instructions for critical security or database operations.
2. **Offline Test Reproducibility**: All ordinary tests must pass 100% offline without requiring external network connectivity, OpenAI API keys, or paid cloud services.
3. **Database Invariance**: Tests must never write to or modify `data/enterprise.db`. Always use isolated temporary SQLite engines during test execution.
4. **No Fluff or Overstatements**: Documentation and code comments must remain honest, evidence-based, and free of exaggerated claims (e.g. avoid phrases like "state-of-the-art" or "flawless").

---

## 2. Local Setup Workflow

### Step 1: Fork & Clone
```bash
git clone https://github.com/kris9117/Rag_agent_.git
cd Rag_agent_
```

### Step 2: Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Step 3: Run Validation Suite
Before submitting changes, ensure all verification steps pass locally:

```bash
# 1. Code Style & Syntax Inspection
flake8 . --count --max-line-length=120 --statistics --exclude=.venv,__pycache__

# 2. Pytest Test Suite & Coverage
pytest -v --cov=app --cov-report=term-missing

# 3. Offline Evaluation Run
python evaluation/run_evaluation.py --mode mock
python evaluation/calculate_metrics.py
```

---

## 3. Pull Request Guidelines

1. **Create a Topic Branch**: Use a descriptive branch name (e.g., `feat/add-slack-tool`, `fix/ticket-category-normalization`).
2. **Include Unit Tests**: Any new graph node, tool, or service method must be accompanied by offline unit tests in `tests/`.
3. **Clean Git History**: Ensure commits are organized with clear, descriptive commit messages. Do not commit temporary log files, `.env` files, or local benchmark outputs.
4. **CI Verification**: Ensure GitHub Actions checks pass on your pull request.
