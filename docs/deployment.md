# Production Deployment Guide: Enterprise IT Support Agent

This guide outlines containerized deployment strategies, production security hardening, and a reference deployment architecture using container orchestration services.

---

## 1. Local Container Deployment (Docker & Compose)

### 1.1 Building the Hardened Image

The `Dockerfile` employs multi-stage layer caching, pinned base images, and executes under an unprivileged user (`appuser`, UID 1000):

```bash
docker build -t enterprise-it-support-agent:latest .
```

### 1.2 Running via Docker CLI

```bash
docker run -d \
  --name it-support-agent \
  -p 8000:8000 \
  -e APP_ENV=production \
  -e OPENAI_API_KEY="sk-your-openai-api-key" \
  -e OPENAI_MODEL="gpt-5.6-luna" \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  enterprise-it-support-agent:latest
```

### 1.3 Running via Docker Compose

For local development or single-host deployments:

```bash
# Start container in background
docker compose up --build -d

# Check service logs
docker compose logs -f

# Verify container health
docker compose ps
```

---

## 2. Production Security Hardening

When deploying to production (`APP_ENV=production`), adhere to the following controls:

1. **Mandatory Authentication**: In production mode, the API gateway strictly rejects requests lacking valid `X-API-Key` or `Authorization: Bearer` credentials with `401 Unauthorized`.
2. **Non-Root Execution**: The container user is pinned to `USER appuser` (UID 1000) with write permissions restricted strictly to `/app/data` and `/app/logs`.
3. **Secrets Management**: Never inject raw API keys via command-line arguments or `.env` files committed to source control. Inject secrets as runtime environment variables sourced from AWS Secrets Manager, HashiCorp Vault, or Kubernetes Secrets.
4. **Health Check Probes**:
   * **Liveness Probe**: `GET /health/live` (Checks process health)
   * **Readiness Probe**: `GET /health/ready` (Validates database connectivity and retrieval index files before routing incoming traffic)

---

## 3. Realistic Cloud Deployment: AWS ECS / Fargate

Below is a reference production architecture utilizing AWS serverless container infrastructure:

```text
                               +-----------------------------+
                               |     Internet / Corporate    |
                               |           Network           |
                               +-----------------------------+
                                              |
                                              v
                               +-----------------------------+
                               | Application Load Balancer   |
                               | (ALB with TLS 1.3 Termination|
                               |  Health Path: /health/ready)|
                               +-----------------------------+
                                              |
                       +----------------------+----------------------+
                       |                                             |
                       v                                             v
        +-----------------------------+               +-----------------------------+
        |   ECS Fargate Task 1        |               |   ECS Fargate Task 2        |
        | - 1 vCPU, 2 GB RAM          |               | - 1 vCPU, 2 GB RAM          |
        | - appuser (non-root)        |               | - appuser (non-root)        |
        | - Local Cross-Encoder Cache |               | - Local Cross-Encoder Cache |
        +-----------------------------+               +-----------------------------+
                       |                                             |
                       +----------------------+----------------------+
                                              |
                                              v
                               +-----------------------------+
                               | Persistent Data Layer       |
                               | - Amazon EFS (Indexes & DB) |
                               | - AWS Secrets Manager (Keys)|
                               +-----------------------------+
```

### Step 1: Push Container to Amazon ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com
docker tag enterprise-it-support-agent:latest <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/it-support-agent:latest
docker push <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/it-support-agent:latest
```

### Step 2: Task Sizing & Resource Allocation
* **CPU Allocation**: Minimum 1.0 vCPU (required for fast vector and Cross-Encoder scoring).
* **Memory Allocation**: Minimum 2.0 GB (allows in-memory Sentence-Transformers model weights and FAISS vector index caching without swapping).
* **Storage**: Amazon EFS volume mounted at `/app/data` to ensure persistent storage for database records and pre-built retrieval indexes across task restarts.

### Step 3: Load Balancer Health Checking
Configure the Application Load Balancer (ALB) target group:
* **Protocol**: HTTP (port 8000)
* **Health Check Path**: `/health/ready`
* **Healthy Threshold**: 2 checks
* **Interval**: 15 seconds
* **Timeout**: 5 seconds

---

## 4. Telemetry & Production Monitoring

* **Prometheus Scraping**: Configure Prometheus or AWS OpenTelemetry Collector to scrape `http://<task-ip>:8000/metrics` every 15 seconds.
* **Log Ingestion**: Forward `/app/logs/observability.jsonl` to Amazon CloudWatch Logs, Datadog, or Elasticsearch via fluent-bit sidecar container.
* **Alerting Policies**:
  * Alert if `http_requests_total{status_code="500"}` exceeds 1% of total traffic.
  * Alert if `http_request_duration_seconds{quantile="0.95"}` exceeds 10.0 seconds.
  * Alert if `/health/ready` returns HTTP 503 for more than 2 consecutive intervals.
