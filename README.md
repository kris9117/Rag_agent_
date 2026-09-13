# Enterprise IT Support Agent

A production-style GenAI application that processes enterprise IT support requests using LLM-based request understanding, intelligent routing, hybrid retrieval, reranking, and grounded response generation.

## Features

- LLM-based request understanding
- Intent classification
- Intelligent request routing
- Retrieval-Augmented Generation
- Hybrid FAISS + BM25 retrieval
- Reciprocal Rank Fusion
- Cross-encoder reranking
- OpenAI embeddings
- OpenAI Responses API
- Escalation detection
- Structured logging
- FastAPI REST API
- Automated Pytest test suite

## Architecture

```text
User Request
    |
    v
FastAPI API
    |
    v
Request Understanding
    |
    v
Intent Classification
    |
    v
Routing
    |
    v
Hybrid Retrieval
    |
    +----------------+
    |                |
    v                v
  FAISS            BM25
    |                |
    +-------+--------+
            |
            v
    Reciprocal Rank Fusion
            |
            v
    Cross-Encoder Reranking
            |
            v
    LLM Response Generation
            |
            v
    Escalation Detection
            |
            v
    JSON API Response