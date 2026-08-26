# H5-ORCH-016 Orchestrator 메시지 서비스

## 단계 정보

- 단계 ID: `H5-ORCH-016`
- 상태: Worker 완료, Reviewer 검토 대기
- 프로젝트 루트: `request_ai_agent_h5_v0`
- 기준선: `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply`
- 범위: HTTP/UI/RAG 없이 server-owned Conversation 메시지를 처리하는 최소 application service

## 구현 내용

`request_ai_agent_h5_v0/orchestrator_service.py`에 `OrchestratorService`와 명시적 DTO를 추가했다. 입력은 `conversation_id`, `message`, `intent`, opaque extraction payload/metadata뿐이다. caller가 Request state/version, Proposal, operation, workflow event를 제공할 수 없다.

| DTO/경계 | authority | mutation |
|---|---|---|
| `OrchestratorMessageInput` | caller 메시지와 Conversation id | 없음 |
| `ConversationStore.read` | server-issued Conversation, request reference, lifecycle/workflow projection | 없음 |
| `RequestStateStore.read` | latest canonical Request snapshot/version | 없음 |
| Registry/geometry adapter | 최신 Request로부터 읽는 read-only field metadata | 없음 |
| H5-ORCH-014 Tool | injected structured-output extractor -> sanitizer/geometry candidate | 없음 |
| H5-ORCH-015 Router | intent와 Tool result의 deterministic route | 없음 |
| `ProposalService.create_proposal` | validated candidate operation의 server Proposal/dry-run record | Request/version 불변 |
| `ConversationWorkflowMachine.dispatch` | server-issued Proposal reference만 Conversation workflow에 반영 | Conversation workflow/reference만 변경 |
| `OrchestratorProposalResult` / `OrchestratorReadOnlyResult` / `OrchestratorFailureResult` | service 결과 | 없음 |

patch만 Tool을 호출한다. Tool candidate가 있으면 workflow의 `proposal_created` transition을 먼저 pure preflight하고, candidate operation만 기존 Proposal service에 전달한다. 생성된 Proposal id만 기존 workflow 경계에 반영한다. `approve_proposal`/apply는 호출하지 않으므로 승인 전 Request State와 version은 불변이다.

`general_qa`, `rag_qa`, `current_input`, `needs_clarification`은 extractor/LLM, Proposal, RAG를 호출하지 않고 read-only route로 끝난다. patch의 no-candidate는 Conversation이 이미 `planning_next_question` 상태일 때만 기존 Planner의 결정 DTO를 반환하며, 그 밖에는 read-only result다. Router failure, Tool failure, malformed input, request/registry read failure, closed/paused Conversation, Proposal creation failure는 stable failure/result로 끝난다.

## 변경 파일

- `request_ai_agent_h5_v0/orchestrator_service.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_service.py`
- `docs/orchestrator_handoff/h5_orch_016_orchestrator_service.md`

## 검증

다음 focused suite를 실행해 `69 passed`를 확인했다.

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_service.py request_ai_agent_h5_v0/tests/test_orchestrator_intent_router.py request_ai_agent_h5_v0/tests/test_orchestrator_extraction_tool.py request_ai_agent_h5_v0/tests/test_orchestrator_workflow_machine.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_next_field_planner.py
```

focused test는 server latest Request/version과 server-issued Conversation만 사용한 Proposal 생성, 승인 전 Request 불변, closed/paused/stale/request/router/tool/proposal failure의 무부분쓰기, no-candidate와 Q&A route의 read-only 동작, deterministic reason 순서와 서로 다른 Request/Conversation 격리, public API/UI/RAG/approved apply·reject·expire 미호출을 확인한다.

아직 실행하지 않은 범위는 실제 LLM/RAG/network, 외부 DB, full E2E, durable multi-worker deployment다.

## 한계와 위험

Request, Conversation, Proposal ledger는 모두 process-local runtime store다. restart, multi-worker shared durability, distributed transaction, exactly-once 보장은 제공하지 않는다. service는 Proposal 생성 전에 same-snapshot workflow preflight를 수행하므로 정상 단일-process 경로의 invalid/stale/paused/closed workflow는 ledger write 전에 중단한다. 다만 Proposal 기록 뒤 외부 lifecycle 경쟁이 발생하면 existing lifecycle API에 rollback/delete가 없어 stable `workflow_transition_failed`를 반환할 뿐 pending ledger record를 원자적으로 되돌릴 수 없다. 이는 현재 단계가 해결할 수 없는 runtime-only durability 한계이며, durable transaction/idempotency는 별도 후속 설계가 필요하다.

## 다음 단계 계약

| 후속 단계 | 제공하는 model/test 계약 |
|---|---|
| H5-ORCH-017 | public API는 `OrchestratorMessageInput`만 만들고 service result를 표현한다. client State/version/operation/Proposal/event를 전달하거나 approved apply를 호출하지 않는다. |
| H5-ORCH-018~020 | UI는 route, read-only next-field decision, server Proposal reference를 표시만 한다. optimistic Request mutation, RAG 직접 호출, Proposal lifecycle 재구현을 하지 않는다. |

Roadmap 상태, 기준 카드, 다음 단계 프롬프트는 변경하지 않았다. Reviewer 검토 전까지 상태는 검토 대기다.
