# 단계 정보

- 단계 ID: `H5-ORCH-012`
- 단계명: Workflow State Machine
- 수행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: `69f9374`, `c1ab16f`, H5-ORCH-009 Proposal lifecycle, H5-ORCH-011 Conversation Session API
- Roadmap 버전: `1.5` (2026-07-31)
- 작업 상태: 완료 후보 — Worker는 Roadmap, 기준 카드, 다음 단계 프롬프트를 변경하지 않고 Reviewer 검토를 대기한다.

# 이번 단계 목표

H5-ORCH-011 process-local Conversation lifecycle 위에 허용된 이벤트만 local `workflow_status`를 전이시키는 최소 결정론적 Workflow State Machine을 추가한다. Request State/version, Proposal ledger lifecycle 및 public HTTP surface는 소유하거나 호출하지 않는다.

# 사전 입력 문서

- `AGENTS.md`, 최신 Roadmap, `common_stage_contract.md`, `baseline_prompts.md`, `manual_stage_execution.md`
- `h5_orch_001_repo_map.md`부터 `h5_orch_011_conversation_api.md`까지

# 실제 수행 내용

- `workflow_machine.py`에 `WorkflowState`, `WorkflowEventType`, frozen event/context/transition DTO, pure `transition()`을 추가했다.
- `ConversationWorkflowMachine.dispatch()`는 pure transition 성공 뒤에만 local Conversation metadata를 반영한다.
- `ConversationStore.apply_workflow_transition()`을 최소 추가해 status와 opaque Proposal reference를 한 번에 저장하고 partial write를 막았다. lifecycle authority는 확장하지 않는다.
- 새 Conversation의 초기 workflow label을 `started`로 변경했다. H5-ORCH-011 API/lifecycle projection shape는 바꾸지 않았다.

# 변경 파일

- `request_ai_agent_h5_v0/conversation_store.py`
- `request_ai_agent_h5_v0/workflow_machine.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_workflow_machine.py`
- `docs/orchestrator_handoff/h5_orch_012_workflow_machine.md`

# 신규 또는 변경된 데이터 구조

| 구조 | 계약과 권위 |
|---|---|
| `WorkflowState` | `started`, `awaiting_answer`, `awaiting_proposal_approval`, `planning_next_question`, `proposal_completed`, `validation_ready`, `paused`, `completed`, `error` vocabulary다. pause는 H5-ORCH-011 lifecycle mode로 판정한다. |
| `WorkflowEvent` | event type과 선택적 opaque `proposal_id`만 갖는 frozen DTO다. Proposal terminal status/operations/base version/diff/validation 또는 Request data는 없다. |
| `WorkflowContext` | workflow label, Proposal reference, pause/lifecycle 상태만 pure function에 전달한다. |
| `WorkflowTransition` | next state와 유지 또는 새로 붙일 opaque Proposal reference만 반환한다. |
| `WorkflowTransitionError` | mutation 전 stable code (`conversation_closed`, `workflow_paused`, `approval_wait_required`, `invalid_workflow_event`)를 제공한다. |

# 상태 및 이벤트 전이

| 현재 상태 | 허용 event | 다음 상태 | Proposal reference |
|---|---|---|---|
| `started` | `start` | `awaiting_answer` | 유지 |
| `awaiting_answer` | `answer_received` | `planning_next_question` | 유지 |
| `planning_next_question` | `question_planned` | `awaiting_answer` | 유지 |
| `awaiting_answer`, `planning_next_question` | `proposal_created(proposal_id)` | `awaiting_proposal_approval` | server `proposal_id`만 저장 |
| `awaiting_proposal_approval` | `proposal_terminal(same proposal_id)` | `proposal_completed` | reference 유지, ledger re-read는 이후 consumer 책임 |
| `proposal_completed` | `plan_next_question` | `planning_next_question` | 유지 |
| `planning_next_question`, `proposal_completed` | `validation_ready` | `validation_ready` | 유지 |
| `proposal_completed`, `validation_ready` | `complete` | `completed` | 유지 |
| non-terminal active state | `fail` | `error` | 유지 |

그 밖의 event는 `invalid_workflow_event`로 거절한다. approval wait 중 terminal-reference event 외 진행 event는 `approval_wait_required`로 거절한다. `completed`, `error`, lifecycle `closed`는 terminal이다. paused Conversation은 어떤 진행 event도 `workflow_paused`로 거절하며 pause 직전 workflow label은 resume 후 유지된다.

# 신규 또는 변경된 API

새 public HTTP API는 없다.

| Internal surface | 계약 |
|---|---|
| `transition(context, event)` | store/service 호출 없이 결정론적 next DTO 또는 stable error를 반환한다. |
| `ConversationWorkflowMachine.dispatch(id, event)` | active Conversation에 pure result만 atomic 반영한다. Request/Proposal store를 읽거나 쓰지 않는다. |
| `ConversationStore.apply_workflow_transition(...)` | validated local status/reference 동시 저장만 한다. event 해석은 하지 않는다. |

# 중요 설계 결정

1. Conversation은 `request_id` reference만 보관하고 Request State/snapshot/version을 읽거나 저장하거나 변경하지 않는다.
2. Proposal approved/rejected/expired/conflicted/failed는 H5-ORCH-009 ledger 권위다. terminal event는 `proposal_id` 동일성만 확인하고 lifecycle을 호출·복제·해석하지 않는다.
3. terminal Proposal reference는 `proposal_completed` 뒤에도 유지한다. 이후 consumer는 `ProposalService.read_proposal(proposal_id)`와 `RequestStateStore.read(request_id)`를 새로 호출해야 한다.
4. pause/resume/close는 H5-ORCH-011 lifecycle authority를 그대로 사용한다. paused/closed dispatch는 Conversation과 Request 모두 불변이다.

# 기존 기능 재사용 지점

- `ConversationStore`의 server-issued ID, deep-copy, active/paused/closed lifecycle, bounded process-local storage를 사용했다.
- H5-ORCH-007 Request store와 H5-ORCH-009 Proposal service는 직접 호출하지 않으며 독립 authority로 남는다.
- Fieldset, normalizer, Validator, Case Matrix, Preview, Word, renderer, geometry Adapter, LLM/RAG, intent routing은 호출·복제·변경하지 않았다.

# 수행하지 않은 작업

- HTTP endpoint, message 처리, LLM/RAG/외부 DB, Planner, Orchestrator service, UI를 추가하지 않았다.
- Request State mutation/snapshot/version 변경 및 client State/Proposal operations/base version/diff/validation/result 수용을 하지 않았다.
- Proposal approve/reject/expire/apply, DB migration, durable storage, multi-worker semantics, H5-ORCH-013 이후 기능을 추가하지 않았다.

# 최소 검증

실행 명령:

`& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_workflow_machine.py request_ai_agent_h5_v0/tests/test_orchestrator_conversation_store.py request_ai_agent_h5_v0/tests/test_orchestrator_conversation_api.py`

결과: `18 passed`.

- 정상 start → answer wait → proposal wait → same terminal reference → next planning/validation-ready/completed와 failure를 검증했다.
- invalid event, approval-wait bypass, mismatch reference, paused/closed dispatch와 completed/error 뒤 event가 Conversation 및 Request State/version을 바꾸지 않음을 검증했다.
- H5-ORCH-011 pause/resume/closed API/model contract, terminal reference-only, Conversation/request isolation을 기존 focused tests와 함께 확인했다.

최종 저장소 검사는 `python tools/check_encoding.py --changed`, `git diff --check`로 수행한다.

# 실패하거나 실행하지 못한 검증

실패한 focused 검증은 없다. 전체 E2E, 실제 LLM/RAG/외부 DB, 전체 suite, multi-worker deployment test는 범위 밖이므로 실행하지 않았다.

# 알려진 문제와 제한사항

- Conversation, Request, Proposal ledger는 process-local memory다. restart, separate worker, scale-out에서 shared durability/transaction/exactly-once semantics가 없다.
- machine은 Proposal terminal status나 Request latest version을 snapshot하지 않는다. consumer가 server authority를 re-read해야 한다.
- concurrent lifecycle change는 active-only check로 workflow mutation을 거절하지만 durable cross-worker atomicity는 제공하지 않는다.

# 발견된 위험

| 위험 | 현재 대응 | 후속 경계 |
|---|---|---|
| approval wait bypass | same pending reference만 terminal event로 허용 | H5-ORCH-016 ledger re-read 뒤 event 선택 |
| stale Request/Proposal | Conversation에 State/version/terminal payload를 저장하지 않음 | H5-ORCH-016, 018~020 server latest read |
| runtime-only loss | bounded process-local store | 별도 승인된 durable 설계 필요 |
| terminal reference replay 오해 | observability reference로만 유지 | H5-ORCH-009 service만 lifecycle action 수행 |

# 다음 단계에서 반드시 참고할 내용

| 후속 단계 | 제공 model/test 계약 |
|---|---|
| H5-ORCH-013 | Planner는 `planning_next_question`에서 deterministic field choice만 만들고 `question_planned` 또는 `validation_ready` event를 선택한다. Request mutation은 하지 않는다. |
| H5-ORCH-015 | Intent Router는 `WorkflowEvent`를 분류해도 store를 직접 변경하지 않고 machine boundary로 전달한다. |
| H5-ORCH-016 | dispatch 전후 server Request latest-read/version과 Proposal terminal record를 재조회한다. Conversation `proposal_id`로 operations/base version/result를 복원할 수 없다. |
| H5-ORCH-018~020 | UI/API는 Conversation projection과 server refresh를 사용하고 paused/closed/approval wait를 optimistic form State로 우회하지 않는다. |

# 다음 단계 수정이 예상되는 파일

- H5-ORCH-013 planner module 및 focused tests
- H5-ORCH-015 intent router module 및 focused tests
- H5-ORCH-016 orchestration service 및 focused tests
- H5-ORCH-018~020 UI/API integration tests

이번 단계는 위 파일을 수정하지 않았다.

# 후속 개선 후보

배포 topology와 durability 요건이 명확해진 뒤에만 shared durable Conversation/Request/Proposal storage, transaction, authorization, idempotency, audit를 별도 승인해 설계한다.

# Roadmap 변경 필요 여부

없음. Worker는 H5-ORCH-012를 완료로 확정하지 않으며 Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 수정하지 않는다. Reviewer 검토를 대기한다.

# Worker 보고

H5-ORCH-012에 Conversation-local pure deterministic workflow machine과 focused tests를 추가했다. 유효 event만 status를 전이시키며 approval-wait bypass, paused/closed 및 terminal mutation은 stable error로 거절한다. Request State/version과 Proposal lifecycle은 건드리지 않고 terminal Proposal은 opaque `proposal_id` reference로만 유지한다. focused tests는 `18 passed`; runtime-only durability와 multi-worker 한계는 남아 있다.
