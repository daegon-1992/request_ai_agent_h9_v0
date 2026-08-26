# 단계 정보

- 단계 ID: `H5-ORCH-015`
- 단계명: Intent Router
- 수행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: `69f9374` 및 H5-ORCH-006~014 작업 트리
- Roadmap 버전: `1.8` (2026-08-01)
- 작업 상태: 완료 후보 — Reviewer 검토 대기

# 이번 단계 목표

기존 `llm_client.extract_form_patch_with_llm()`의 다섯 structured-output intent를 보존하는 결정론적·read-only Router DTO를 추가했다. 기준 흐름은 `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply`이며 Router는 이 중 어느 State, Proposal, Workflow 경계도 실행하지 않는다.

# 사전 입력 문서

- `AGENTS.md`, 최신 Roadmap, 공통 단계 계약, 기준 카드, 수동 실행 절차
- `h5_orch_004_agent_ui_survey.md`, `h5_orch_012_workflow_machine.md`, `h5_orch_014_extraction_tool.md`

# 실제 수행 내용

- `orchestrator_intent_router.py`에 caller-provided intent, opaque LLM extraction payload/metadata, optional H5-ORCH-014 Tool result를 받는 frozen `IntentRouterInput`과 pure `route_intent()`를 추가했다.
- `patch`, `general_qa`, `rag_qa`, `current_input`, `needs_clarification`만 trim/lower 정규화 후 allowlist한다. missing/malformed intent는 stable clarification route, unknown intent도 stable clarification route로 반환한다.
- malformed Router input, payload/metadata 또는 Tool result는 `IntentRouterFailureDTO`로 반환한다. 빈 `candidates`, 빈/공백 no-candidate·failure code도 invalid Tool result다. Router는 payload의 operation/value/field를 해석하거나 생성하지 않는다.
- `patch`는 사전 계산된 Tool `candidates`/`no_candidate`/`failure`만 `patch_tool_outcome`과 stable code로 표시한다. candidate를 Proposal로 만들지 않는다. 나머지 intent는 기능 호출 없이 동일 이름의 route category만 반환한다.

# 변경 파일

- `request_ai_agent_h5_v0/orchestrator_intent_router.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_intent_router.py`
- `docs/orchestrator_handoff/h5_orch_015_intent_router.md`

# 신규 또는 변경된 데이터 구조

| DTO | authority / 내용 | mutation |
|---|---|---|
| `IntentRouterInput` | caller 제공 intent, opaque extraction payload/metadata, optional H5-ORCH-014 Tool result | 없음 |
| `IntentRouteDTO` | allowlisted route category, ordered stable reason, patch Tool decision metadata | 없음 |
| `IntentRouterFailureDTO` | invalid input/Tool의 stable failure code와 clarification category | 없음 |

`LLM_CHAT_INTENTS`는 기존 LLM prompt의 다섯 vocabulary만 가진다. Router는 payload의 `operations`를 읽지 않으며 client State/Proposal payload를 받거나 신뢰하지 않는다.

# 신규 또는 변경된 API

공개 HTTP API는 없다. 내부 pure surface는 `route_intent(input_dto)` 하나다.

# 중요 설계 결정

- intent는 explicit caller input이며, extraction payload와 metadata는 Router에 opaque snapshot으로 전달된다.
- H5-ORCH-014 Tool 계약을 호출하거나 변경하지 않고, 이미 얻은 `ExtractionCandidatesDTO` / `ExtractionNoCandidateDTO` / `ExtractionFailureDTO`의 kind/code만 read-only metadata로 연결한다.
- stable clarification은 intent 문제가 있을 때, stable failure DTO는 Router input/payload/metadata/Tool result 자체가 유효하지 않을 때 사용한다.
- Request State/version, Conversation, Proposal ledger 및 Workflow는 Router authority 밖이다. H5-ORCH-016만 최신 Request read/version 확인과 후속 경계 선택을 조합한다.

# 기존 기능 재사용 지점

- LLM intent vocabulary: `llm_client.extract_form_patch_with_llm()`.
- candidate/no-candidate/failure DTO contract: `orchestrator_extraction_tool.py` (H5-ORCH-014).
- sanitizer, geometry Adapter, Proposal/dry-run/approved apply은 기존 authority를 그대로 유지하며 Router는 호출하지 않는다.

# 수행하지 않은 작업

- LLM 호출, extraction Tool 호출, sanitizer/geometry/Field Registry 변경, Request latest-read, Conversation read, Workflow dispatch를 하지 않았다.
- Proposal 생성·승인·거절·만료·적용, persistence, public endpoint, UI, RAG/외부 DB, 실제 LLM network test를 추가하지 않았다.
- Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 수정하지 않았다.

# 최소 검증

다음 focused tests는 각 허용 intent의 deterministic route/reason order, missing/unknown/malformed intent, invalid payload/Tool result, Tool decision metadata, caller input isolation 및 Request/Conversation/Proposal/workflow/RAG/sanitizer 경계 inspection을 검증한다.

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_intent_router.py request_ai_agent_h5_v0/tests/test_orchestrator_extraction_tool.py request_ai_agent_h5_v0/tests/test_orchestrator_workflow_machine.py
python tools/check_encoding.py --changed
git diff --check
```

실행 결과: 보완 focused test 포함 `35 passed in 0.15s`; `python tools/check_encoding.py --changed`는 `Encoding check passed`, `git diff --check`는 성공(출력 없음)이었다. Reviewer는 실제 diff와 함께 이를 다시 확인해야 한다.

# 실패하거나 실행하지 못한 검증

실제 LLM/RAG/외부 DB 및 전체 E2E는 범위 밖이므로 실행하지 않는다.

# 알려진 문제와 제한사항

Router와 선행 Tool 및 Request/Conversation/Proposal 저장소는 runtime-only process-local 계약이다. restart, separate worker, scale-out에 shared durability, transaction, exactly-once semantics를 제공하지 않는다. Router는 최신 Request/version이나 Proposal terminal record를 읽지 않는다.

# 발견된 위험

후속 caller가 Router의 `patch_tool_outcome="candidates"`를 Proposal authorization 또는 apply 권한으로 오인하면 승인 전 변경 위험이 생긴다. 이는 H5-ORCH-016의 latest-read/version/Proposal lifecycle 경계에서 방지해야 한다.

# 다음 단계에서 반드시 참고할 내용

| 후속 단계 | 제공하는 model/test 계약 |
|---|---|
| H5-ORCH-016 | explicit intent와 read-only Tool decision을 받아 최신 Request/version을 별도로 읽고, candidate만 Proposal service에 전달한다. Router 결과로 dispatch/apply하지 않는다. |
| H5-ORCH-018~020 | UI/API는 route/failure를 표시할 수 있지만 client State/Proposal payload나 Router decision으로 optimistic mutation하지 않는다. |

# 다음 단계 수정이 예상되는 파일

- `orchestrator_service` 및 focused tests (H5-ORCH-016)
- API/UI integration files and tests (H5-ORCH-018~020)

# 후속 개선 후보

배포 topology가 확정된 뒤 durable Request/Conversation/Proposal storage, transaction, authorization, idempotency 및 audit을 별도 단계에서 설계한다.

# Roadmap 변경 필요 여부

없음. Worker는 Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 변경하지 않으며 Reviewer 검토 대기 상태로 남긴다.
