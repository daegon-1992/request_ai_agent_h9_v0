# 단계 정보

- 단계 ID: `H5-ORCH-014`
- 단계명: 자연어 추출 Tool Adapter
- 수행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: `69f9374` 및 H5-ORCH-006~013 작업 트리
- Roadmap 버전: `1.7` (2026-08-01)
- 작업 상태: 완료 후보 — Reviewer 검토 대기

# 이번 단계 목표

기존 LLM structured output과 `chat_patch.sanitize_external_operations()`을 그대로 재사용하여 Proposal 생성 전의 검증 가능한 read-only 후보 DTO를 제공한다. 기준선은 `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply`이며, Tool은 그 중 sanitizer 직후에서 멈춘다.

# 사전 입력 문서

`AGENTS.md`, 최신 Roadmap, 공통 단계 계약/기준 카드/수동 실행 문서, H5-ORCH-001~009 및 H5-ORCH-013 인수인계 문서를 확인했다.

# 실제 수행 내용

- `orchestrator_extraction_tool.py`에 caller snapshot, Registry metadata, geometry transport Adapter 및 injected/mockable extractor만 받는 `ExtractionToolInput`과 pure `extract_candidates()`를 추가했다.
- 기본 extractor는 기존 `llm_client.extract_form_patch_with_llm()`이다. tests/services는 같은 호출 형태의 mockable callable을 주입한다.
- raw structured operation은 기존 sanitizer를 단일 operation 단위로 호출한 결과만 후보로 투영한다. Tool은 regex/alias fallback, 값 추론, unit 변환, geometry/validation 규칙을 만들지 않는다.

# 변경 파일

- `request_ai_agent_h5_v0/orchestrator_extraction_tool.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_extraction_tool.py`
- `docs/orchestrator_handoff/h5_orch_014_extraction_tool.md`

# 신규 또는 변경된 데이터 구조

| DTO | authority / 내용 | mutation |
|---|---|---|
| `ExtractionToolInput` | caller 제공 message, state summary, `FieldRegistryDTO` tuple, `GeometryProductsAdapterDTO`, extractor | 없음 |
| `ExtractionCandidateDTO` | sanitized allowed op의 field_id, candidate value, confidence, evidence phrase, ambiguity, unit | 없음 |
| `ExtractionNoCandidateDTO` / `ExtractionFailureDTO` | 안정적인 no-candidate/failure code와 순서 보존 reason | 없음 |

geometry `products`는 `GeometryProductsAdapterDTO.transport_path`만 허용하며 sanitizer가 부여하는 기존 Adapter metadata를 후보 operation에 보존한다. canonical State에 직접 쓰지 않는다.

# 신규 또는 변경된 API

공개 HTTP API는 없다. 내부 호출 표면은 `extract_candidates(input_dto)` 하나이며 Proposal 생성/승인/적용을 하지 않는다.

# 중요 설계 결정

- sanitizer 통과 전후를 비교해 unknown/unsupported/malformed/missing value/ambiguous/missing unit을 후보가 아닌 안정 DTO로 돌려준다.
- unit metadata가 있는 Registry field는 output operation의 unit이 없으면 `missing_unit`이다. Tool은 Registry unit을 추론값으로 채우지 않는다.
- 동일 input·mock output은 operation 순서와 reason 순서를 유지한다. state summary는 입력 snapshot으로만 extractor에 전달된다.

# 기존 기능 재사용 지점

- LLM: `llm_client.extract_form_patch_with_llm()` structured output.
- allowlist/normalization: `chat_patch.sanitize_external_operations()`.
- geometry transport: `field_registry.get_geometry_products_adapter()`와 sanitizer의 existing Adapter contract.
- Proposal/dry-run/approved apply, Fieldset/normalizer/Validator/Case Matrix/Preview/Word는 호출하거나 복제하지 않는다.

# 수행하지 않은 작업

Request State/version mutation·persistence, Proposal ledger lifecycle, Conversation/workflow dispatch, public endpoint, intent router, UI, RAG/외부 DB/실제 LLM network test를 추가하지 않았다.

# 최소 검증

다음 focused test는 mocked structured output의 sanitizer projection, failure/no-candidate, Request/Conversation/Proposal 불변, deterministic ordering/isolation, 그리고 store/workflow/RAG 의존성 부재를 검증한다.

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_extraction_tool.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_field_registry.py
python tools/check_encoding.py --changed
git diff --check
```

실행 결과: `29 passed`.

보완 focused tests는 기본 extractor unavailable mock, invalid JSON/DTO/error 각각의 Request·Conversation·Proposal 불변, 그리고 candidate와 복수 reason의 입력 순서 보존을 직접 확인한다. extractor에는 state summary 복사본만 전달하므로 injected callable도 caller snapshot을 변경할 수 없다.

# 실패하거나 실행하지 못한 검증

전체 suite/E2E, 실제 LLM·RAG·외부 DB, durable multi-worker deployment는 범위 밖이라 실행하지 않는다.

# 알려진 문제와 제한사항

Tool과 기존 Request/Conversation/Proposal store는 runtime-only이며 Tool은 store를 소유하거나 최신-read를 보장하지 않는다. H5-ORCH-016 caller가 최신 Request/version snapshot을 읽고 후보를 Proposal 경로에 연결해야 한다. durable restart/multi-worker semantics는 제공하지 않는다.

# 발견된 위험

기존 LLM prompt가 evidence phrase/unit을 항상 요구하지 않으므로 unit-bearing field는 의도적으로 no-candidate가 될 수 있다. 이는 추론 보완 대신 명시 입력을 요구하는 계약이다.

# 다음 단계에서 반드시 참고할 내용

| 후속 단계 | 제공 model/test 계약 |
|---|---|
| H5-ORCH-016 | latest Request/Registry snapshot을 `ExtractionToolInput`에 넣고 candidate만 Proposal service에 전달한다; Tool result로 state/workflow를 직접 바꾸지 않는다. |
| H5-ORCH-018~020 | UI/API는 candidate/failure를 표시할 수 있으나 client state/Proposal payload를 authority로 삼거나 optimistic apply하지 않는다. |

# 다음 단계 수정이 예상되는 파일

- H5-ORCH-016 Orchestrator service 및 focused tests
- H5-ORCH-018~020 API/UI integration tests

# 후속 개선 후보

배포 topology가 승인되면 durable Request/Proposal storage와 transaction 경계를 별도 단계에서 설계한다. 이 Tool에는 storage나 fallback extraction을 추가하지 않는다.

# Roadmap 변경 필요 여부

없음. Worker는 Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 바꾸지 않고 Reviewer 검토 대기로 남긴다.
