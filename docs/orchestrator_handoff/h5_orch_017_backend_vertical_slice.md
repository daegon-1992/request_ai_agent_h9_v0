# 단계 정보

- 단계 ID: `H5-ORCH-017`
- 단계명: Orchestrator API·백엔드 수직 흐름
- 수행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: `c1ab16f` 및 H5-ORCH-006~016 작업 트리
- Roadmap 버전: `2.0` (2026-08-01)
- 작업 상태: 완료 후보 — Worker는 Roadmap, 기준 카드, 다음 단계 프롬프트를 변경하지 않고 Reviewer 검토를 대기한다.

# 이번 단계 목표

H5-ORCH-016의 server-owned `OrchestratorService`를 얇은 Flask HTTP adapter로 연결하고, 실제 LLM/RAG/network 대신 app composition root에 주입한 mocked structured-output extractor로 server Request/Conversation 생성, 자연어 patch Proposal, 기존 승인 apply, latest Request/version 재조회, Planner 다음 field까지의 백엔드 수직 흐름을 검증한다.

기준선은 `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply`다. message endpoint는 approved apply를 소유하지 않으며, 승인 전 Request State/version은 불변이고 기존 `ProposalService.approve_proposal()` 성공만 version을 증가시킨다.

# 사전 입력 문서

- `AGENTS.md`
- 최신 `docs/orchestrator_handoff/orchestrator_roadmap.md`
- `docs/orchestrator_handoff/prompts/common_stage_contract.md`
- `docs/orchestrator_handoff/prompts/baseline_prompts.md`
- `docs/orchestrator_handoff/prompts/manual_stage_execution.md`
- `docs/orchestrator_handoff/h5_orch_004_agent_ui_survey.md`
- `docs/orchestrator_handoff/h5_orch_009_proposal_lifecycle.md`
- `docs/orchestrator_handoff/h5_orch_011_conversation_api.md`
- `docs/orchestrator_handoff/h5_orch_012_workflow_machine.md`
- `docs/orchestrator_handoff/h5_orch_013_next_field_planner.md`
- `docs/orchestrator_handoff/h5_orch_014_extraction_tool.md`
- `docs/orchestrator_handoff/h5_orch_015_intent_router.md`
- `docs/orchestrator_handoff/h5_orch_016_orchestrator_service.md`

# 실제 수행 내용

- `create_app(orchestrator_extractor=...)`에 optional injected extractor를 추가했다. 인자가 없으면 기존 H5-ORCH-014 default extractor 경계를 유지하고, focused test는 mock callable만 주입한다.
- app마다 하나의 process-local `RequestStateStore`, `ConversationStore`, `ProposalStore`/`ProposalService`, `ConversationWorkflowMachine`, `OrchestratorService`를 조합했다. 각 authority는 공유 runtime 안에서도 분리된다.
- additive `POST /api/orchestrator/messages`를 추가했다. endpoint는 strict allowlist body를 `OrchestratorMessageInput`으로 변환하고 `service.handle()` 결과만 stable JSON으로 투영한다.
- Proposal 생성 결과는 server `proposal_id`, status, bounded changed-path diff metadata만 반환한다. operations, Request State/version, Proposal base version/validation/result는 공개하지 않는다.
- read-only route는 ordered reasons와 optional Planner DTO를 반환한다. failure는 stable error/reasons와 deterministic HTTP status를 반환한다. 모든 message response는 `state_changed=false`이며 Proposal/read-only/failure payload는 `read_only=true`다.
- 승인·거절·만료 endpoint는 추가하지 않았다. focused vertical flow는 기존 `ProposalService.approve_proposal(proposal_id)`와 `ConversationWorkflowMachine.dispatch()`를 그대로 사용하고, 승인 직후 기존 versioned Request GET으로 server latest State/version을 다시 읽는다.
- 새 Conversation의 첫 patch candidate는 `OrchestratorService`가 client event 없이 server-owned `start -> proposal_created` existing transition sequence로 처리한다. `ConversationWorkflowMachine.dispatch_many()`는 모든 pure transition을 먼저 검증하고 Conversation record에는 최종 상태를 한 번만 저장한다.

## 백엔드 수직 흐름

1. 기존 `POST /api/request/versioned`와 `POST /api/conversations`가 server ID를 만든다.
2. first patch candidate에서는 service가 server-owned existing workflow `start` event를 포함해 Conversation을 `awaiting_proposal_approval`으로 전이한다. client message payload는 workflow event를 받지 않는다.
3. mocked extractor의 structured operation은 H5-ORCH-014 Tool의 sanitizer/geometry Adapter를 거쳐 candidate가 된다.
4. H5-ORCH-016 service가 latest Request/Registry를 읽고 H5-ORCH-009 `create_proposal()`을 호출한다.
5. HTTP response는 Proposal reference와 read-only diff만 반환한다. 이 시점 Request State/version은 생성 전과 같다.
6. 기존 lifecycle의 `approve_proposal(proposal_id)`만 recorded base version과 operations로 CAS apply한다.
7. 기존 Request GET이 증가한 version과 canonical State를 반환한다.
8. existing terminal/plan-next workflow event 뒤 no-candidate message가 latest Request/Registry 기반 Planner decision을 stable JSON으로 반환한다.

# 변경 파일

- `request_ai_agent_h5_v0/app.py`
- `request_ai_agent_h5_v0/orchestrator_service.py`
- `request_ai_agent_h5_v0/workflow_machine.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_backend_vertical_slice.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_service.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_workflow_machine.py`
- `docs/orchestrator_handoff/h5_orch_017_backend_vertical_slice.md`

# 신규 또는 변경된 데이터 구조

새 persistence record나 Request/Conversation/Proposal domain DTO는 추가하지 않았다.

| HTTP 구조 | 필드 | 권위와 제한 |
|---|---|---|
| message request | `conversation_id`, `message`, `intent`, optional opaque `extraction_payload`, `extraction_metadata` | `OrchestratorMessageInput`만 생성한다. unknown top-level field는 거절한다. |
| Proposal result | `kind`, `route_category`, ordered `reasons`, `proposal.proposal_id`, `proposal.status`, `proposal.diff`, `state_changed=false`, `read_only=true` | Proposal id/status/diff는 server ledger 재조회 결과다. operation/base version/Request data는 없다. |
| read-only result | `kind`, `route_category`, ordered `reasons`, optional `planner_decision`, `state_changed=false`, `read_only=true` | Q&A/RAG/current-input/clarification/no-candidate/Tool outcome을 mutation 없이 표현한다. |
| failure result | `ok=false`, `kind=failure`, `error`, ordered `reasons`, `state_changed=false`, `read_only=true` | invalid/unknown/lifecycle/read/proposal/service failure의 stable projection이다. |

`planner_decision`은 기존 frozen Planner DTO를 `dataclasses.asdict()`로 JSON object/list에 투영한다. endpoint가 field priority, required, Fieldset 또는 validation 규칙을 재계산하지 않는다.

# 신규 또는 변경된 API

## `POST /api/orchestrator/messages`

허용 request 예시:

```json
{
  "conversation_id": "conversation_<server-id>",
  "message": "요청 개요를 입력해 줘",
  "intent": "patch",
  "extraction_payload": {},
  "extraction_metadata": {}
}
```

허용하지 않는 top-level authority에는 `state`, `request_state`, `version`, `request_version`, `operation`, `operations`, `proposal`, `proposal_id`, `event`, `workflow_event`, `approved` 및 기타 unknown key가 포함된다. 이들은 `400 invalid_orchestrator_message_payload`로 service 호출 전에 거절된다. opaque extraction payload/metadata의 내용은 endpoint가 operation이나 rule로 해석하지 않는다.

| 결과 | HTTP | stable body 핵심 |
|---|---:|---|
| Proposal 생성 | 200 | `ok=true`, `kind=proposal_created`, server Proposal reference/read-only diff |
| read-only route/no-candidate/Tool failure | 200 | `ok=true`, `kind=read_only` 또는 `next_field`, route/reasons/optional Planner DTO |
| invalid message DTO | 400 | `error=invalid_*` |
| unknown Conversation | 404 | `error=conversation_read_failed` |
| closed/paused/invalid workflow | 409 | lifecycle/workflow stable code |
| Request/Registry/Proposal/service read failure | 503 | stable failure code |

기존 Request, Conversation, legacy chat/form API는 삭제하거나 변경하지 않았다. 승인/거절/만료 public HTTP API를 새로 만들지 않았다.

# 중요 설계 결정

## Authority 표

| 데이터/결정 | authoritative boundary | message client/endpoint 권한 |
|---|---|---|
| Conversation identity/lifecycle/workflow | `ConversationStore`와 `ConversationWorkflowMachine` | server-issued `conversation_id` reference만 전달; event/lifecycle mutation 금지 |
| Request State/latest version | `RequestStateStore.read()`와 approved CAS | payload 제공·대체·직접 mutation 금지 |
| Field metadata/conditional activation | existing Field Registry/Fieldset | endpoint rule 해석·복제 금지 |
| natural-language candidate | injected existing structured extractor -> H5-ORCH-014 Tool/sanitizer/geometry Adapter | message/opaque metadata만 제공; raw operation authority 없음 |
| intent route | H5-ORCH-015 Router가 allowlisted intent를 read-only 분류 | keyword/regex routing 금지 |
| Proposal create/diff/lifecycle | `ProposalService`와 server `ProposalStore` | server reference/read-only diff만 수신; client Proposal/operations/base version 금지 |
| approved apply | `ProposalService.approve_proposal(proposal_id)`의 recorded Proposal + Request CAS | message endpoint가 호출·복제하지 않음 |
| next field | latest Request/Registry/history를 받은 H5-ORCH-013 Planner | Planner result 표시만 가능; direct workflow/form mutation 금지 |

## Service/Conversation/Request/Proposal/approval/Planner 경계

- endpoint는 DTO conversion과 result projection만 한다. source inspection test는 endpoint에 CAS, patch apply, Proposal approve/reject/expire, workflow dispatch가 없음을 확인한다.
- service만 first patch candidate의 server-owned `start` sequence를 선택한다. sequence는 existing pure `transition()`을 반복 호출할 뿐 event rule을 새로 정의하지 않으며 `dispatch_many()`가 final Conversation status/reference를 한 번에 저장한다.
- service가 server Conversation을 읽어 `request_id`를 얻고 server Request를 latest-read한다. client가 Request id/State/version을 message body로 선택할 수 없다.
- service의 candidate path만 server Proposal을 생성한다. endpoint의 extra ledger read는 생성된 reference의 diff projection을 위한 read-only 호출이다.
- approval은 기존 lifecycle 밖에서 수행된다. approved result 뒤에는 기존 Request GET이 latest State/version을 읽고 Planner 호출 전 service도 Request를 다시 읽는다.
- Planner는 no-candidate이면서 existing workflow가 `planning_next_question`일 때만 service가 호출한다. endpoint는 Planner reason/order를 그대로 JSON으로 만든다.

## 승인 전 불변과 stable failure

- pending Proposal 생성은 Conversation workflow/reference만 변경하고 Request State/version을 바꾸지 않는다.
- approved CAS 성공만 Request version을 정확히 1 증가시킨다. stale approval은 Proposal을 `conflicted` terminal로 기록하되 approval 시점 Request/Conversation을 추가 변경하지 않는다.
- invalid client authority, no-candidate, general/RAG/current-input/clarification, Tool/Router failure, unknown/closed/paused Conversation, Request read failure, stale workflow, Proposal creation failure는 Request partial write를 남기지 않는다.
- Proposal creation failure는 preflight 뒤 ledger/Conversation write 전에 stable failure가 된다. sequence의 later event가 invalid이면 `dispatch_many()`가 Conversation write를 하지 않는다. process-local lifecycle 경쟁으로 Proposal record 뒤 workflow transition이 실패할 수 있는 H5-ORCH-016의 알려진 원자성 한계는 그대로 남으며 endpoint가 rollback 규칙을 만들지 않는다.

# 기존 기능 재사용 지점

- H5-ORCH-011 Conversation create/read/pause/resume/close API와 store identity
- H5-ORCH-012 pure workflow transition 및 atomic server-owned sequence dispatch
- H5-ORCH-013 deterministic `plan_next_fields()` DTO
- H5-ORCH-014 injected extractor, existing `sanitize_external_operations()`, geometry Adapter
- H5-ORCH-015 five-intent Router vocabulary/reason ordering
- H5-ORCH-016 `OrchestratorService.handle()` DTO/result 경계
- H5-ORCH-007 Request latest-read/version/CAS와 H5-ORCH-009 Proposal create/approve lifecycle

기존 Fieldset, normalizer, Validator, Case Matrix, Preview, Word, renderer, Q&A/RAG 구현은 변경하거나 복제하지 않았다.

# 수행하지 않은 작업

- UI/HTML/renderer와 frontend state를 수정하지 않았다.
- RAG 구현·호출, 실제 LLM/network, regex/alias extraction, keyword/regex intent routing을 추가하지 않았다.
- sanitizer, geometry Adapter, Field Registry, Fieldset, Validator, Case Matrix, Preview, Word 규칙을 endpoint에 복제하지 않았다.
- Request State/version direct mutation, client Proposal/operation apply, optimistic apply를 추가하지 않았다.
- Proposal/Workflow/Conversation lifecycle API를 재구현하거나 기존 endpoint를 삭제하지 않았다.
- DB migration, external storage, durable/multi-worker transaction, H5-ORCH-018 이후 UI/E2E를 구현하지 않았다.
- Roadmap 상태, 기준 카드, `current_stage.md`, Reviewer/다음 단계 prompt를 변경하지 않았다.

# 최소 검증

실행 명령:

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_backend_vertical_slice.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py request_ai_agent_h5_v0/tests/test_orchestrator_conversation_api.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_workflow_machine.py request_ai_agent_h5_v0/tests/test_orchestrator_next_field_planner.py
python tools/check_encoding.py --changed
git diff --check
```

focused pytest 결과: `71 passed in 1.25s`.

검증 범위:

- strict HTTP DTO allowlist와 client State/version/operation/Proposal/event/approved 거절
- server-created Request/Conversation의 첫 HTTP patch Proposal, server latest Request 사용과 internal pre-dispatch 부재
- Proposal reference/read-only diff, 승인 전 Request 불변, 기존 approve 뒤 version +1, latest GET, 다음 Planner decision
- general/RAG/current-input/clarification의 extractor/RAG/Proposal/apply 미호출과 read-only response
- no-candidate/Tool/Router ordered reasons, closed/paused/unknown Conversation, Request read failure, Proposal creation failure
- stale approval terminal result와 approval 시점 Request/Conversation 추가 write 부재
- 서로 다른 Request/Conversation 격리와 endpoint direct mutation surface 부재

# 실패하거나 실행하지 못한 검증

전체 suite, browser/UI E2E, 실제 LLM/RAG/network, external DB/vector store, restart/multi-worker deployment test는 단계 범위 밖이므로 실행하지 않았다. 초기 focused 실행은 테스트가 store lifecycle 메서드를 `closed/paused`로 잘못 호출해 2건 실패했고, 실제 API 이름 `close/pause`로 테스트를 정정했다. Reviewer 보완으로 fresh Conversation first-message flow를 추가한 뒤 지정 suite `71 passed`를 확인했다. 구현 failure는 아니었다.

# 알려진 문제와 제한사항

- Request, Conversation, Proposal ledger와 composition root는 모두 process-local runtime-only다. restart 시 record가 사라지고 separate worker/scale-out 사이에는 shared identity, transaction, CAS, exactly-once가 없다.
- `app.extensions` 참조는 focused in-process test와 현재 composition 관찰용이며 public HTTP authority가 아니다.
- Conversation 생성 직후 workflow는 existing H5-ORCH-012 `started`다. first patch candidate에서만 service가 client event 없이 existing `start -> proposal_created` sequence를 server-owned로 적용한다. no-candidate/read-only route는 workflow를 진행시키지 않는다.
- H5-ORCH-016이 기록한 Proposal create 뒤 workflow lifecycle 경쟁은 durable atomic rollback 없이 `workflow_transition_failed`가 될 수 있다. endpoint가 Proposal delete/rollback을 추론해 추가하지 않았다.
- unknown Conversation read와 store read exception은 H5-ORCH-016 service의 동일 stable code `conversation_read_failed`로 표현된다.
- Q&A/RAG/current-input route는 이 단계에서 기존 기능을 새로 호출하지 않고 stable read-only route metadata만 반환한다. 실제 Q&A/RAG 연결은 기존 API 또는 후속 명시 범위를 사용해야 한다.

# 발견된 위험

| 위험 | 현재 방어 | 후속 확인 |
|---|---|---|
| client authority injection | strict top-level allowlist, opaque payload 미해석 | 018~020 UI가 State/version/Proposal/event를 보내지 않는지 확인 |
| optimistic apply | 모든 message response `state_changed=false`, diff read-only | 019 Proposal card와 020 form sync가 pending diff를 채택하지 않는지 확인 |
| stale/replay approval | existing Proposal ledger/base version/CAS/replay contract | 019가 server id만 승인하고 terminal replay를 새 apply로 취급하지 않는지 확인 |
| stale form after approval | existing versioned Request GET으로 latest-read | 020이 approved 결과 후 반드시 Request refresh하는지 확인 |
| runtime partial transaction | process-local preflight와 stable failure, durable 보장 없음 | 배포 topology 확정 후 별도 승인된 durable transaction 설계 |

# 다음 단계에서 반드시 참고할 내용

| 후속 단계 | 소비할 API/model/test 계약 |
|---|---|
| H5-ORCH-018 | `POST /api/orchestrator/messages`에는 다섯 allowed field만 보낸다. 새 Conversation의 first patch message는 server-owned start sequence를 사용한다. UI는 Request/form/workflow를 직접 바꾸지 않는다. |
| H5-ORCH-019 | Proposal card는 `proposal.proposal_id`, `status`, read-only `diff`만 소비한다. operations/base version/State를 client authority로 만들지 않고 existing Proposal lifecycle의 explicit approve/reject를 사용한다. pending response를 form에 적용하지 않는다. |
| H5-ORCH-020 | approved lifecycle 성공 후 기존 `GET /api/request/versioned/<request_id>`의 State/version만 채택한다. terminal/plan-next workflow 뒤 message response의 Planner decision과 refreshed form Fieldset을 동기화하며 patch를 중복 적용하지 않는다. |

H5-ORCH-018~020 test는 이 단계의 mocked extractor composition, strict payload rejection, ordered stable response, approval 전 불변, approved-only version 증가, cross-request isolation을 회귀 계약으로 유지해야 한다.

# 다음 단계 수정이 예상되는 파일

- H5-ORCH-018: `ui.py`와 대화 panel/API focused tests
- H5-ORCH-019: existing Proposal lifecycle을 소비하는 card/approval UI와 focused tests
- H5-ORCH-020: form refresh/Fieldset synchronization과 bounded MVP E2E tests

이번 Worker는 위 파일을 수정하지 않았다.

# 후속 개선 후보

- 배포 topology와 저장 요구가 확정된 뒤에만 shared durable Request/Conversation/Proposal storage, transaction/idempotency/authorization/audit을 별도 승인 단계로 설계한다.
- 실제 Q&A/RAG 응답 연결은 H5-ORCH-029 또는 명시적으로 승인된 기존 API adapter 범위에서 수행한다.

# Roadmap 변경 필요 여부

Worker가 변경할 필요는 없다. 현재 Roadmap의 H5-ORCH-017 상태, 기준 카드, 다음 단계 프롬프트를 유지하고 Reviewer가 실제 diff·focused test·initial workflow 경계를 검토한 뒤 완료 여부를 결정해야 한다.

# Worker 보고

H5-ORCH-017의 additive message API와 mockable app composition root, first-message server workflow sequence, backend vertical focused test, 본 인수인계 문서를 추가했다. endpoint는 client State/version/operation/Proposal/event를 거절하고 service result와 server Proposal read-only diff만 표현한다. 기존 Proposal approval 뒤에만 Request version이 증가하며 fresh Conversation의 natural patch Proposal, latest Request 재조회와 Planner 다음 field까지 `71 passed`로 검증했다. Roadmap·기준 카드·다음 단계 프롬프트는 변경하지 않았고 Reviewer 검토 대기로 남긴다.
