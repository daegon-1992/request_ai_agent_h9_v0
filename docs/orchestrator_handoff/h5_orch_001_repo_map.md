# 단계 정보

- 단계 ID: `H5-ORCH-001`
- 단계명: 저장소·실행 구조 조사
- Roadmap 버전: `0.3`
- 작업 상태: 완료
- 조사 기준일: 2026-07-31 (Asia/Seoul)
- 프로젝트 루트: `G:\Tech\00_Agent\01_Agent_Code\request_ai_agent_h5_v0`
- Git 기준: `ed6c2af` — `build: add H5 orchestrator runner` (2026-07-31T14:45:35+09:00)
- 앱 버전 상수: `h5_v0-stage09-condition-state-progress-20260630`

# 이번 단계 목표

h5_v0 CAE 의뢰서 웹앱의 실제 프로젝트 경계, 런타임, 모듈 경계, API/UI 연결, 테스트 경로를 다음 단계가 재조사 없이 시작할 수 있게 기록한다.

# 실제 수행 내용

## 프로젝트 경계·버전

- 실제 루트는 상위 작업공간이 아니라 자체 `.git`를 가진 `request_ai_agent_h5_v0`이다. 상위 `G:\\Tech\\00_Agent\\01_Agent_Code`는 Git 저장소가 아니다.
- 최상위 구성: `AGENTS.md`, `Request_AI_Agent_h5_v0.py`, `request_ai_agent_h5_v0/`, `docs/`, `tools/`.
- 최상위 `README`, 의존성 manifest (`pyproject.toml`, `requirements*.txt`, `package.json`), pytest 설정(`pytest.ini`, `tox.ini`, `setup.cfg`, `conftest.py`)은 발견되지 않았다.

## 런타임·진입점

| 구분 | 위치 | 역할 |
|---|---|---|
| 실행점 | `Request_AI_Agent_h5_v0.py` | `load_local_env()` 후 패키지 `create_app()`을 만들고 Flask 서버를 실행한다. 기본값은 `0.0.0.0:8503`; `FLASK_HOST`, `FLASK_PORT`, `FLASK_DEBUG`로 조정한다. |
| 패키지 진입점 | `request_ai_agent_h5_v0/__init__.py` | `create_app`과 `APP_VERSION`을 노출한다. |
| API 진입점 | `request_ai_agent_h5_v0/app.py`의 `create_app()` | Flask 인스턴스, `/` 및 `/api/*` 라우팅, 상위 모듈 조합을 담당한다. |
| UI | `request_ai_agent_h5_v0/ui.py`의 `HTML_TEMPLATE` | HTML/CSS/JavaScript가 내장되어 `/`에서 제공된다. 별도 프런트엔드 번들/개발 서버는 확인되지 않았다. |

환경 파일 값은 읽지 않았다. 코드에는 로컬 환경 파일 탐색, LLM·임베딩·벡터 경로/활성화 플래그가 있으나 실제 값과 설치 패키지는 manifest 부재로 확정할 수 없다.

## 모듈 지도

| 영역 | 위치 | 상위 책임 |
|---|---|---|
| Request 작성·상태 | `state.py`, `schema.py`, `draft_pipeline.py`, `app.py` | Request 초기화·정규화·스키마·초안 생성·API 조합 |
| Agent/대화/RAG | `llm_client.py`, `chat_patch.py`, `analysis_type_recommender.py`, `rag_qa.py`, `rag_search.py`, `rag_bridge.py`, `embedding_runtime.py` | LLM 상태·제안·질의응답·검색/임베딩 연결. 별도 Agent 서비스/프로세스는 확인되지 않음 |
| Validation/규칙 | `validator.py`, `condition_engine.py`, `condition_fields.py`, `condition_fieldsets.py`, `case_matrix.py`, `review_pipeline.py` | 필수/조건부 입력, 케이스 행렬, 최종 검토 |
| 출력 | `preview_document.py`, `word_export.py`, `export_contract.py` | 미리보기와 Word 출력 계약/생성 |
| 저장소 보조 | `product_hierarchy.py`, `normalized_product_hierarchy.py`, `demo_db_store.py`, `demo_analysis_type.py` | 제품 계층과 데모 저장/해석유형 보조. 실제 DB·데이터 내용은 미조사 |
| 테스트 | `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py` | 현재 확인된 최소 회귀 테스트 |
| 오케스트레이터 | `docs/orchestrator_handoff/`, `tools/orchestrator_runner/` | 단계 문서와 Runner 추적 파일. Runner 동작은 미검증 |

## API/UI 연결

`app.py`의 `index()`가 `HTML_TEMPLATE`에 버전을 치환해 `/`으로 반환하고, `ui.py`의 JavaScript가 같은 origin의 `fetch()`/POST JSON으로 Flask API를 호출한다. 현재 경계는 **내장 UI → Flask `/api/*` → 동일 패키지 도메인 모듈**이다.

| API 그룹 | 확인된 경로 |
|---|---|
| 기본·초기화 | `GET /`, `GET /api/health`, `GET /api/bootstrap`, `POST /api/request/new` |
| Request·입력 | `POST /api/request-context/confirm`, `POST /api/request-context/fieldset`, `POST /api/input/save`, `POST /api/preview`, `POST /api/document-preview` |
| 해석·조건 | `GET /api/product-hierarchy`, `POST /api/analysis-type/recommend`, `POST /api/analysis-type/select`, `GET /api/analysis-type-guidance`, `POST /api/conditions/recommend` |
| 초안·검토·출력 | `POST /api/draft`, `POST /api/review`, `POST /api/submit`, `POST /api/export/word` |
| 대화·RAG | `GET /api/llm/status`, `GET /api/rag/status`, `POST /api/chat/instant`, `POST /api/chat/propose`, `POST /api/chat/apply`, `POST /api/chat/reject`, `POST /api/rag/qa`, `POST /api/chat/send` |

각 API의 payload 계약, Request 내부 상태, Proposal 승인 안전성은 002 이후 범위로 남긴다.

## 테스트·환경

- 확인된 테스트: `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`
- 설정 파일이 없으므로 pytest 기본 discovery를 전제로 한 대상 실행 명령은 다음과 같다.

```powershell
python -m pytest request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py
```

- Python/pytest 및 Flask 등 import 의존성의 설치 출처는 dependency manifest 부재로 확인 불가다.
- 앱 실행, 테스트 실행, 네트워크 호출, DB 마이그레이션은 수행하지 않았다.

## Git 상태

- Git 사용: 예. 기준 HEAD는 `ed6c2af`이다.
- 조사 시작 시 미추적: `automation_runner.lock`, `automation_state.json`, `docs/orchestrator_handoff/runs/` 실행 산출물, 패키지/테스트의 `__pycache__/`.
- 이를 읽거나 변경하지 않았으며, 이번 단계는 문서 두 파일만 변경한다.

# 변경 파일

| 파일 | 변경 내용 |
|---|---|
| `docs/orchestrator_handoff/h5_orch_001_repo_map.md` | 이 저장소 지도 |
| `docs/orchestrator_handoff/orchestrator_roadmap.md` | 001 완료 상태 갱신 |

# 신규 또는 변경된 데이터 구조

없음. 애플리케이션 코드·설정·테스트·데이터는 변경하지 않았다.

# 신규 또는 변경된 API

없음.

# 중요 설계 결정

- 오케스트레이터 후속 설계는 `app.py`의 API와 `ui.py`의 내장 JavaScript를 함께 고려한다.
- Agent/Validation/출력은 같은 Python 패키지의 모듈 조합이며, 상태·Proposal 계약은 추정하지 않고 002에서 조사한다.

# 수행하지 않은 작업

- 대용량 데이터, 모델, 벡터 DB, DB 파일, 생성 산출물, 실행 로그와 `runs/` 내용은 읽지 않았다.
- 비밀값·환경 파일 내용은 읽거나 기록하지 않았다.
- API 세부 payload, Validation 규칙, LLM/RAG 동작, Runner 동작은 조사하지 않았다.

# 최소 검증

| 검증 항목 | 결과 |
|---|---|
| 프로젝트 루트/Git | `.git`, `git rev-parse --show-toplevel`, `git log -1`로 독립 루트와 `ed6c2af` 확인 |
| 실행점 | launcher의 `create_app()` 및 `__main__` Flask 실행 확인 |
| 라우팅 | `app.py`의 `create_app()`과 `/`, `/api/*` 데코레이터 확인 |
| UI 연결 | `ui.py`의 `HTML_TEMPLATE`와 `/api/*` `fetch()` 호출 확인 |
| 테스트 | 실제 테스트 파일 및 `test_*` 함수 확인 |
| 설정 | manifest/pytest 설정 파일 부재 확인 |

# 알려진 문제와 제한사항

- 기존 Roadmap의 Runner “미구축” 기록과 달리 현재 HEAD에는 `tools/orchestrator_runner/` 추적 파일이 있다. 동작 검증은 하지 않았다.
- 미추적 자동화 실행 산출물과 Python 캐시가 문서 작성 전부터 존재한다. 본 단계 변경과 분리해 관리해야 한다.
- README/의존성 manifest 부재로 신규 환경의 정확한 설치 절차와 전체 테스트 명령은 확정할 수 없다.

# 다음 단계에서 반드시 참고할 내용

- 002: `state.py`, `schema.py`, `app.py` 중심으로 Request State와 Proposal 경로 조사.
- 003: `validator.py`, 조건/fieldset, `review_pipeline.py`, 출력 모듈 중심으로 규칙·출력 조사.
- 004: LLM/대화/RAG 모듈과 `ui.py` 호출 흐름 조사.

# 다음 단계 수정이 예상되는 파일

후속 단계에서 결정한다. 이번 단계는 문서 두 파일 외 수정하지 않는다.

# 후속 개선 후보

- 비밀값 비포함 의존성·개발/테스트 실행 문서의 추가 여부.
- `runs/`, 캐시, lock/state의 Git 추적/무시 정책 정리 여부.
