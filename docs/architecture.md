# Enterprise IT Support Agent Architecture

## 1. Overview

The Enterprise IT Support Agent is a FastAPI-based GenAI application for processing enterprise IT support requests.

The system combines:

- LLM-based request understanding
- Intent classification
- Rule-based routing
- Retrieval-Augmented Generation
- FAISS semantic retrieval
- BM25 lexical retrieval
- Reciprocal Rank Fusion
- Cross-encoder reranking
- Grounded response generation
- Escalation detection
- Structured logging
- Automated testing

## 2. High-Level Flow

```text
User Request
    |
    v
FastAPI Endpoint
    |
    v
Request Validation
    |
    v
LLM Request Understanding
    |
    v
Intent Classification
    |
    v
Routing Decision
    |
    v
RAG Tool
    |
    v
Hybrid Retrieval
    |
    +------------------+
    |                  |
    v                  v
FAISS Retrieval   BM25 Retrieval
    |                  |
    +--------+---------+
             |
             v
Reciprocal Rank Fusion
             |
             v
Cross-Encoder Reranking
             |
             v
Top-K Retrieved Context
             |
             v
LLM Response Generation
             |
             v
Escalation Detection
             |
             v
Structured API Response