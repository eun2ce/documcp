# 📒 **DocuMCP** – Project Overview

_A document generation service that transforms project descriptions into comprehensive documentation using LM Studio integration._

---

## 1. Vision

Give developers a **seamless way to generate project documentation**:  
You provide a brief project description → the system generates **comprehensive, structured documents** including PRDs, project overviews, and README files.

> **One-liner**  
> "Describe it briefly, get it documented – your project documentation is ready."

---

## 2. Core Value (Why it matters)

| Pain we solve                           | DocuMCP answer                                              |
| --------------------------------------- | ----------------------------------------------------------- |
| 프로젝트 문서 작성에 시간이 많이 걸림   | 간단한 설명만으로 자동 문서 생성                            |
| 일관된 문서 형식 유지가 어려움          | 표준화된 템플릿으로 일관된 문서 생성                        |
| PRD, README 등 다양한 문서 타입 관리    | 한 번에 여러 문서 타입 동시 생성                            |
| 로컬 LLM 활용의 복잡함                  | LM Studio 연동으로 쉬운 로컬 AI 활용                        |

---

## 3. Key Features – MVP

| Category         | What users can do                                                               |
| ---------------- | ------------------------------------------------------------------------------- |
| **Generation API**| `POST /api/v1/generate` → 여러 문서 타입 동시 생성                             |
| **LLM Engine**   | LM Studio 연동으로 로컬 LLM 활용                                               |
| **Templates**    | PRD, What-is-this, README 문서 타입별 전용 템플릿                              |
| **Integration**  | REST API로 다양한 도구와 연동 가능                                             |

---

## 4. Who's it for?

| Persona             | How they'll use DocuMCP                                       |
| ------------------- | ------------------------------------------------------------- |
| **개발자 팀**       | 프로젝트 초기 단계에서 문서 템플릿 빠르게 생성                 |
| **프로덕트 매니저** | 간단한 아이디어를 완성된 PRD로 변환                           |
| **오픈소스 기여자** | 새로운 프로젝트의 README와 문서를 빠르게 작성                 |

---

## 5. Tech Snapshot

| Layer          | Choice                              | Note                               |
| -------------- | ----------------------------------- | ---------------------------------- |
| **Front-End**  | 없음 (API only)                     | REST API 중심 설계                 |
| **Back-End**   | FastAPI + Uvicorn                   | 고성능 비동기 API 서버              |
| **Model**      | LM Studio Integration                | 로컬 LLM 모델 활용                 |
| **Infra**      | Docker + Docker Compose             | 컨테이너 기반 배포                 |
| **Monitoring** | Prometheus metrics + Structured logs| 운영 모니터링 지원                 |

<details>
<summary>High-level flow</summary>

```
User → /api/v1/generate → DocuMCP(LM Studio)
                       ↘ PRD + What-is-this + README
```
</details>

---

## 6. Roadmap (tentative)

| Quarter  | Milestone                                           |
| -------- | --------------------------------------------------- |
| **Q3 '25** | MVP API 서버 완성, LM Studio 연동                  |
| **Q4 '25** | 추가 문서 타입 지원, 템플릿 커스터마이징           |
| **Q1 '26** | GitHub Actions 연동, CI/CD 문서 자동화             |
| **Q2 '26** | 다중 언어 지원, 고급 템플릿 기능                   |

---

## 7. Team & Roles _(가정)_

| Role             | Responsibility                          |
| ---------------- | -------------------------------------- |
| **Back-End Dev** | FastAPI 서버, LM Studio 연동 구현       |
| **Template Eng.**| 문서 템플릿 설계 및 최적화              |
| **Infra**        | Docker, 배포/모니터링                   |
| **Integration**  | 외부 도구 연동 개발                     |

---

## 8. Success Metrics _(MVP)_

* ✍️ **Document generation latency** ≤ 5 s @p95  
* ✅ **문서 품질 만족도** > 80% (사용자 피드백 기준)  
* 👥 주간 active users ≥ 50 (베타테스트 기준)  

---

## 9. Glossary

| Term            | Meaning                                      |
| --------------- | -------------------------------------------- |
| **LM Studio**   | 로컬 LLM 실행을 위한 데스크톱 애플리케이션    |
| **Generation**  | 프로젝트 설명 → 구조화된 문서 생성           |
| **Template**    | 문서 타입별 생성 템플릿                      |

---

## 10. How to Get Involved

* **Developers** – clone repo → `docker-compose up`  
* **Users** – REST API 호출로 문서 생성  
* **Contributors** – PR/Issue로 새로운 문서 템플릿 제안 환영  
