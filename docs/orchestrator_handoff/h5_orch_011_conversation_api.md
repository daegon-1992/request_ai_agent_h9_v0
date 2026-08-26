# 단계 정보

- 단계 ID: `H5-ORCH-011`
- 단계명: Conversation Session API
- 수행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: `69f9374`, `c1ab16f`, H5-ORCH-009 Proposal lifecycle, H5-ORCH-010 Conversation State model
- Roadmap 버전: `1.4`
- 작업 상태: 완료 후보; Worker는 Roadmap, 기준 카드, 다음 단계 프롬프트를 변경하지 않고 Reviewer 검토를 대기한다.

# 이번 단계 목표

H5-ORCH-010의 bounded process-local `ConversationStore`를 `create_app()`의 runtime `RequestStateStore`와 같은 프로세스 범위에 조합했다. 서버에 존재하는 `request_id`로만 Conversation을 생성하고, server-issued `conversation_id`를 사용해 생성·조회·pause·resume·close의 최소 additive HTTP API를 제공한다.

# 사전 입력 문서

- `AGENTS.md`
- `docs/orchestrator_handoff/orchestrator_roadmap.md`
- `docs/orchestrator_handoff/prompts/common_stage_contract.md`
- `docs/orchestrator_handoff/prompts/baseline_prompts.md`
- `docs/orchestrator_handoff/prompts/manual_stage_execution.md`
- `docs/orchestrator_handoff/h5_orch_001_repo_map.md`부터 `h5_orch_010_conversation_state.md`까지

# 실제 수행 내용

- `create_app()`마다 `RequestStateStore`와 별도의 `ConversationStore`를 만들었다. 두 store는 같은 process-local lifetime이지만 Request/Conversation record와 권한은 분리된다.
- `POST /api/conversations`는 `request_id`를 `RequestStateStore.read()`로 확인한 후에만 Conversation을 생성한다. 선택적 `proposal_id`는 opaque server reference로만 기록한다.
- `GET /api/conversations/<conversation_id>`, `POST .../pause`, `POST .../resume`, `POST .../close`를 추가했다.
- 모든 성공 응답은 deep-copy Conversation projection만 반환한다. projection은 `conversation_id`, `request_id`, `workflow_status`, `paused`, `status`, `question_history`, `summary`, `conversation_version`, 선택적 `proposal_id`만 포함한다.
- API 입력은 create의 `request_id`, 선택적 `proposal_id` 및 body 없는 전이로 제한했다. Request State/snapshot/full State, Request version, client State, Proposal operations/base version/diff/validation/result가 포함된 body는 `invalid_conversation_payload`로 거절한다.
- unknown Request/Conversation은 각각 `request_not_found`/`conversation_not_found` 404, 잘못된 또는 closed lifecycle 전이는 `invalid_conversation_transition` 409, bounded capacity는 `conversation_store_full` 409으로 안정적으로 반환한다.

# 변경 파일

- `request_ai_agent_h5_v0/app.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_conversation_api.py`
- `docs/orchestrator_handoff/h5_orch_011_conversation_api.md`

# 신규 또는 변경된 데이터 구조

새 record나 Request/Proposal DTO는 추가하지 않았다. H5-ORCH-010의 frozen `ConversationSnapshot`을 그대로 사용하며, HTTP projection에서만 local `version`을 `conversation_version`으로 이름 붙였다. 이는 Request version, Proposal base version, CAS token이 아니다.

Conversation은 opaque `request_id`와 optional opaque `proposal_id`만 보관한다. Request State, Request snapshot/version, client-held State, Proposal operations/base version/diff/validation/result 또는 terminal status를 복사하지 않는다.

# 신규 또는 변경된 API

| API | 입력 | 성공 응답 | 실패 계약 |
|---|---|---|---|
| `POST /api/conversations` | `{request_id, proposal_id?}` | `201`, Conversation projection | unknown Request `404 request_not_found`; invalid/forbidden payload `400 invalid_conversation_payload`; full store `409 conversation_store_full` |
| `GET /api/conversations/<conversation_id>` | 없음 | `200`, Conversation projection | unknown Conversation `404 conversation_not_found` |
| `POST /api/conversations/<conversation_id>/pause` | body 없음 | `200`, paused projection | unknown `404`; paused/closed transition `409 invalid_conversation_transition` |
| `POST /api/conversations/<conversation_id>/resume` | body 없음 | `200`, active projection | unknown `404`; active/closed transition `409 invalid_conversation_transition` |
| `POST /api/conversations/<conversation_id>/close` | body 없음 | `200`, closed projection | unknown `404`; already closed `409 invalid_conversation_transition` |

Proposal approve/reject/expire/apply API는 추가하지 않았다. `proposal_id` reference는 terminal 상태가 되어도 유지되며, 이후 service는 H5-ORCH-009 server ledger에서 `read_proposal(proposal_id)`로 terminal 상태를 재조회해야 한다.

# 중요 설계 결정

- Conversation create 전에 server Request existence를 확인하되 Request를 수정하거나 snapshot을 저장하지 않는다. 실패한 create/transition/capacity 경로는 다른 Conversation과 Request State/version을 바꾸지 않는다.
- API는 Conversation lifecycle envelope만 노출한다. workflow status의 event 규칙이나 message 처리 없이 H5-ORCH-012 Workflow State Machine을 선행 구현하지 않는다.
- `proposal_id`를 terminal data로 확장하지 않는다. API는 Proposal lifecycle을 우회하거나 재구현하지 않으며, H5-ORCH-009 ledger만 terminal authority다.
- app extension의 store 참조는 focused in-process test 관찰용이며 HTTP API가 아니다. durable/shared store 권한을 의미하지 않는다.

# 기존 기능 재사용 지점

- `RequestStateStore.read(request_id)`가 server request identity/latest-read authority다.
- `ConversationStore`가 server-issued ID, deep-copy snapshot, bounded capacity, pause/resume/close 및 terminal mutation 거절을 계속 담당한다.
- H5-ORCH-009 `ProposalService.read_proposal()`가 Proposal terminal lifecycle authority로 남는다.

Fieldset, normalizer, Validator, Case Matrix, Preview, Word, renderer, geometry Adapter, LLM/RAG, regex/alias extractor, keyword/regex intent router는 호출·복제·변경하지 않았다.

# 수행하지 않은 작업

- message 처리, 실제 LLM/RAG/외부 DB 호출, Workflow State Machine, Planner, Orchestrator service, UI를 추가하지 않았다.
- Request State mutation, Request snapshot persistence, client-held legacy State 이관, Request version 변경을 하지 않았다.
- Proposal operation/base version/diff/validation/result API 노출이나 approve/reject/expire/apply endpoint를 추가하지 않았다.
- DB migration, 외부 저장소, multi-worker deployment, H5-ORCH-012 이후 기능, 기존 endpoint/API 호환성 변경을 하지 않았다.

# 최소 검증

다음 focused tests만 실행했다.

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_conversation_api.py request_ai_agent_h5_v0/tests/test_orchestrator_conversation_store.py
```

결과: `11 passed`.

- API create/read/pause/resume/close lifecycle 및 invalid/closed 전이 거절
- unknown Request/Conversation, Request/Conversation isolation, bounded capacity failure 뒤 기존 Conversation과 Request State/version 불변
- response deep-copy projection 및 Request State/version, client State, Proposal operations/base version 비노출/비수용
- server `proposal_id` reference-only 보존과 H5-ORCH-009 terminal ledger re-read 계약

최종 저장소 검사는 아래 명령으로 수행한다.

```powershell
python tools/check_encoding.py --changed
git diff --check
```

# 실패하거나 실행하지 못한 검증

실패한 focused 검증은 없다. 전체 E2E, 전체 test suite, 실제 LLM/RAG/외부 DB, multi-worker deployment test는 이번 최소 API 범위 밖이므로 실행하지 않았다.

# 알려진 문제와 제한사항

Request, Conversation, Proposal ledger 모두 process-local memory다. 재시작, 별도 Flask worker, scale-out 환경에서는 Conversation record 및 shared transaction/exactly-once 보장이 유지되지 않는다. durable storage, migration, authorization, cross-process idempotency는 별도 승인된 설계가 필요하며 이번 단계에서 추론해 추가하지 않았다.

Conversation은 생성 시점의 Request 존재만 확인한다. 이후 Request/Proposal 삭제·terminal 변화·ownership은 Conversation snapshot으로 추정할 수 없고, 이후 service가 각 server authority를 다시 읽어 안전하게 처리해야 한다.

# 발견된 위험

- Conversation이 Request snapshot 또는 terminal Proposal 결과를 보관하면 stale authority가 생길 수 있다. 현재 API projection은 이를 포함하지 않아 Request/Proposal 분리를 유지한다.
- process-local capacity failure는 새 Conversation 저장 전에 발생한다. eviction을 추가하지 않았으므로 기존 Conversation record를 조용히 잃지 않는다.
- legacy client-held State endpoint는 호환성 때문에 계속 존재하지만 Conversation API의 authority가 아니다.

# 다음 단계에서 반드시 참고할 내용

| 후속 단계 | 제공 계약 |
|---|---|
| H5-ORCH-012 | `workflow_status`는 opaque local label이다. deterministic event rule은 이 API lifecycle과 `paused`/`closed`를 존중해 별도 구현한다. approval wait는 `proposal_id`만 보관하고 terminal Proposal을 ledger에서 재조회한다. |
| H5-ORCH-016 | Conversation API/model은 Request mutation authority가 아니다. service는 `RequestStateStore.read()` 및 Proposal lifecycle/ledger를 새로 읽어 조합하고 operations/base version을 Conversation에서 복원하지 않는다. |
| H5-ORCH-018~020 | UI는 server-issued `conversation_id`와 reference projection만 사용한다. optimistic form State나 Proposal terminal result를 Conversation에 저장하지 않고 server Request refresh와 ledger re-read를 사용한다. |

# 다음 단계 수정이 예상되는 파일

- H5-ORCH-012: workflow module 및 focused workflow tests
- H5-ORCH-016: additive orchestration service와 focused service tests
- H5-ORCH-018~020: `ui.py`와 해당 API/UI integration tests

이번 단계는 위 파일을 수정하지 않았다.

# 후속 개선 후보

배포 topology와 durability 요구가 명확해질 때에만 shared durable Request/Conversation/Proposal storage와 transaction/authorization/audit/idempotency 설계를 별도 단계로 제안한다. 현재 API에 persistence 또는 multi-worker semantics를 암묵적으로 도입하지 않는다.

# Roadmap 변경 필요 여부

없음. Worker는 H5-ORCH-011을 완료로 확정하지 않으며 Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 변경하지 않는다. Reviewer의 실제 diff·focused test·authority boundary 검토를 대기한다.

# Worker 보고

`ConversationStore`를 runtime `RequestStateStore`와 같은 process-local scope에 안전하게 조합하고, server Request가 존재할 때만 생성되는 additive Conversation Session API를 구현했다. API는 deep-copy Conversation projection과 reference-only `proposal_id`만 제공하며 Request State/version과 Proposal lifecycle payload를 노출하거나 수용하지 않는다. H5-ORCH-009 terminal Proposal은 이후 service가 server ledger에서 재조회해야 한다. runtime-only durability와 multi-worker 한계는 남아 있으며, Roadmap·기준 카드·다음 단계 프롬프트는 Reviewer 검토 대기로 변경하지 않았다.
