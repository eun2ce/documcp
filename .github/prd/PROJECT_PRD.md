# DocuMCP – **Backend PRD**

## 1 · Overview

Provide a **FastAPI monolith** that accepts project descriptions, routes them through templates, runs generation with **LM Studio integration**, and returns Markdown documents: PRD, What-is-this, README.

## 2 · Goals

- ≤ 5 s p95 latency for single document generation  
- Generate at least 3 document types consistently  
- Modular template router to extend to new formats  
- Seamless LM Studio integration for local LLM usage

## 3 · System Context

Client (IDE/CLI) ──> FastAPI API
│
├─ LM Studio (Local LLM Server)
├─ Template Router (PRD, What-is-this, README)
└─ Concurrent Document Generation

## 4 · Functional Requirements

### 4.1 API

| Method  | Path                  | Desc                                   |
| ------- | --------------------- | -------------------------------------- |
| `POST`  | `/api/v1/generate`    | Generate document set from input text  |
| `GET`   | `/api/v1/health`      | Health check                          |
| `GET`   | `/api/v1/metrics`     | Prometheus metrics                    |

### 4.2 Templates

- **What-is-this** → Overview (vision, core value, use cases)  
- **PRD** → Goals, system context, requirements, risks  
- **README** → Install, Run, API usage  

### 4.3 LM Studio Integration

- **Connection Management** → Auto-detect available models
- **API Communication** → OpenAI-compatible API calls
- **Error Handling** → Graceful fallback on connection issues
- **Model Selection** → Dynamic model selection from available models

---

## 5 · Non-Functional

| Aspect        | Requirement                                             |
| ------------- | ------------------------------------------------------- |
| Security      | Basic validation, rate limiting (optional)              |
| Scalability   | Horizontal scaling with Uvicorn workers                 |
| Reliability   | Deterministic prompts, retry on LM Studio timeout       |
| Observability | `/metrics` Prometheus exporter, structured logging      |
| Performance   | Concurrent document generation, async processing        |

---

## 6 · Deployment

- **Monorepo structure**: `features/` shared kernel + infra, `projects/documcp-backend` service  
- **Docker** build & run with LM Studio dependency  
- **Local Development** → LM Studio running on localhost:1234
- **Production** → Containerized with external LM Studio instance

---

## 7 · Extensibility

- Add new document types with template classes  
- Support multiple LLM backends (OpenAI, Anthropic, etc.)  
- Configurable prompt templates per document type
- Plugin system for custom document generators

---

## 8 · Risks

| Risk                     | Prob·Impact | Mitigation                       |
| ------------------------ | ----------- | -------------------------------- |
| LM Studio connection fail| H/H         | Connection retry, health checks  |
| LLM output inconsistent  | M/M         | Prompt engineering, validation   |
| Template drift           | M/H         | Versioned templates, tests       |
| Latency spikes           | M/M         | Async processing, timeouts       |

---

_Last updated: 2025-09-10_