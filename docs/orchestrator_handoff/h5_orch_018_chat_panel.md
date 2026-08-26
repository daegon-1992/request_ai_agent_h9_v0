# H5-ORCH-018 대화 패널 기본 UI

## 단계 정보

- 단계 ID: `H5-ORCH-018`
- 단계명: 대화 패널 기본 UI
- 상태: Worker 완료 후보, Reviewer 검토 대기
- 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 Commit: `69f9374` 및 H5-ORCH-017 작업 트리
- Roadmap 버전: `2.1` (2026-08-01)
- 기준선: `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply`
- Roadmap, 기준 카드, 다음 단계 프롬프트는 변경하지 않았다.

## 이번 단계 목표

기존 폼과 legacy chat을 대체하지 않는 최소 panel을 추가해 server-issued Conversation으로 메시지를 보내고, loading 및 stable read-only/error 응답까지만 표시한다. 승인과 form synchronization은 후속 단계로 남긴다.

## 사전 입력 문서

- `AGENTS.md`, 최신 Roadmap 및 `prompts/common_stage_contract.md`
- `prompts/baseline_prompts.md`, `prompts/manual_stage_execution.md`
- `h5_orch_004_agent_ui_survey.md`, `h5_orch_009_proposal_lifecycle.md`, `h5_orch_011_conversation_api.md`, `h5_orch_012_workflow_machine.md`
- `h5_orch_013_next_field_planner.md`부터 `h5_orch_017_backend_vertical_slice.md`까지

## 구현 내용

기존 폼과 legacy `Agent` 채팅을 유지한 채 `ui.py`에 닫을 수 있는 별도 대화 패널을 additive하게 추가했다. 상단의 `대화 패널` 버튼이 shell을 열고 닫으며, 패널은 별도 message list, text input, 전송 중 비활성화/loading, stable error 문구만 가진다.

패널 최초 전송 시에만 다음 server-issued bootstrap을 수행한다.

1. `POST /api/request/versioned`에 빈 `{}`만 보내 server Request id를 받는다.
2. `POST /api/conversations`에 그 `request_id`만 보내 server Conversation id를 받는다.
3. 이후 `POST /api/orchestrator/messages`에 정확히 `conversation_id`, `message`, `intent: "patch"`만 보낸다.

이 빈 Request는 panel-local runtime bootstrap이다. 현재 폼 draft, legacy client `requestState`, State snapshot, Request version은 읽거나 보내지 않으며 Request id는 bootstrap 함수의 지역 변수로만 사용한 뒤 보관하지 않는다. panel state는 server `conversationId`, loading flag와 DOM의 display-only history뿐이다.

## DTO 및 authority

| 경계 | UI가 보내거나 보관하는 것 | 금지/서버 권위 |
|---|---|---|
| panel bootstrap | empty Request create, server Conversation id | 기존 폼 State/draft/version을 Request create에 넣지 않음 |
| message request | `conversation_id`, `message`, `intent` | State/version/request id, Proposal/operation/event/approval field를 보내거나 보관하지 않음 |
| response | `kind`, route category, ordered reasons, planner decision, Proposal id/status/read-only diff의 표시 | direct RAG/LLM, rule/extraction, Request replacement, workflow event 생성 금지 |
| Proposal | pending 안내와 읽기 전용 변경 수 표시 | Yes/No, approve/reject/expire, card lifecycle, optimistic form apply 금지 |

첫 patch message의 `start -> proposal_created` 처리도 UI가 event를 보내지 않고 H5-ORCH-017 서버 서비스가 소유한다. `proposal_id`는 응답에 포함된 값을 화면에 읽기 전용으로 보이는 용도뿐이며 client lifecycle authority가 아니다.

## 신규 또는 변경된 데이터 구조

`orchestratorPanelState`는 `conversationId`와 loading flag만 가진다. message history는 panel DOM에만 표시하며 form draft나 Request/Proposal/workflow record를 복제하지 않는다. 새 server persistence DTO나 State 구조는 추가하지 않았다.

## 신규 또는 변경된 API

새 endpoint는 없다. panel은 기존 `POST /api/request/versioned`의 빈 body, `POST /api/conversations`의 server Request id, `POST /api/orchestrator/messages`의 allowlisted message DTO만 호출한다.

## 중요 설계 결정

- panel-local empty Request bootstrap은 existing versioned Request create를 안전하게 재사용하며, 현재 화면의 legacy form draft를 전달하거나 덮지 않는다.
- 항상 allowlisted `intent:"patch"`를 보내며 UI가 keyword/regex로 intent를 분류하지 않는다.
- response는 `textContent` 및 read-only DOM만으로 표현한다. diff 또는 planner result를 State/form value로 해석하지 않는다.

## 기존 기능 재사용 지점

H5-ORCH-011 Conversation create, H5-ORCH-017 message endpoint와 server-owned first-message sequence, 기존 `ui.py`의 style/input conventions를 재사용한다. Fieldset, sanitizer, geometry Adapter, Validator, Case Matrix, Preview, Word, RAG와 legacy Agent chat은 호출·복제·변경하지 않는다.

## 승인 전 불변 및 실패 동작

- pending Proposal은 안내와 read-only diff만 표시하며 form DOM, legacy `requestState`, server Request State/version에 반영하지 않는다.
- Q&A/RAG/current-input/clarification/no-candidate/Tool·Router 결과는 server response의 route/reasons/planner 안내를 표시한다. 패널은 RAG 또는 LLM을 직접 호출하지 않는다.
- bootstrap, network, malformed/error response는 `대화 패널 오류`와 `폼과 기존 채팅은 변경되지 않았습니다.`라는 stable message로 끝난다.
- close/reopen은 Conversation id와 표시 DOM을 유지하지만 lifecycle transition을 호출하지 않는다. unknown/closed/paused Conversation은 message endpoint의 stable failure를 표시한다.
- runtime stores는 process-local이다. restart, multi-worker shared Conversation/Request/Proposal durability, transaction, exactly-once는 제공하지 않는다.

## 변경 파일

- `request_ai_agent_h5_v0/ui.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py`
- `docs/orchestrator_handoff/h5_orch_018_chat_panel.md`

## focused 검증

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_backend_vertical_slice.py request_ai_agent_h5_v0/tests/test_orchestrator_conversation_api.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py
python tools/check_encoding.py --changed
git diff --check
```

UI focused test는 panel shell과 legacy chat DOM 공존, panel-local bootstrap/message payload allowlist, proposal display-only 경계, apply/reject/expire/direct patch/workflow dispatch 부재를 source/HTML 수준에서 확인한다. Node mock DOM/fetch runtime은 pending Proposal 표시, close/reopen, unknown/closed/paused, malformed response/network failure의 stable error 및 legacy form/chat DOM 격리를 직접 확인한다. 기존 backend focused suite는 strict allowlist, fresh first-message server start sequence, pending Request 불변, Q&A/Tool/Router/lifecycle failure, cross-session isolation을 계속 확인한다.

실행 결과: `46 passed in 0.92s`. `python tools/check_encoding.py --changed`와 `git diff --check`도 통과했다.

## 실패하거나 실행하지 못한 검증

실제 browser E2E, 실제 LLM/RAG/network, external DB, restart/multi-worker deployment은 범위 밖이다. UI runtime test는 browser 대신 Node mock DOM/fetch로 좁게 실행했으며 실제 network를 호출하지 않는다.

## 알려진 문제와 제한사항

Request, Conversation, Proposal store는 process-local runtime-only다. bootstrap으로 만든 panel Conversation은 restart나 별도 worker에 공유되지 않으며 durable transaction, shared identity, exactly-once를 주장하지 않는다.

## 발견된 위험

legacy form의 client draft와 panel-local empty Request를 혼동하면 승인 전 authority가 넓어진다. 현재 panel은 `collectState()`/legacy `requestState`를 참조하지 않고, pending diff도 form DOM에 쓰지 않아 이를 차단한다.

## H5-ORCH-019~020 소비 계약

| 후속 단계 | 소비할 계약 |
|---|---|
| H5-ORCH-019 | 이 패널의 server `proposal_id`, status, read-only diff 표시를 별도 approval UI가 소비한다. approval 호출은 이 단계에 없다. |
| H5-ORCH-020 | approved lifecycle 성공 후에만 existing versioned Request GET으로 latest State/version을 재조회하고 form/Fieldset을 동기화한다. pending diff를 form에 쓰지 않는다. |

## 다음 단계 수정이 예상되는 파일

- H5-ORCH-019: Proposal card/approval UI 및 focused test
- H5-ORCH-020: existing versioned Request refresh, Fieldset/form synchronization, bounded E2E test

## 후속 개선 후보

배포 topology와 durability 요구가 별도로 승인될 때만 shared durable store, authorization, idempotency/audit을 설계한다. 현 단계 panel에 persistence나 lifecycle endpoint를 암묵적으로 추가하지 않는다.

## Roadmap 변경 필요 여부

없음. Worker와 Reviewer는 Roadmap 상태, 기준 카드, current/review prompt를 직접 변경하지 않으며 Reviewer verdict 뒤에만 별도 Planner 절차가 이를 반영한다.

## 수행하지 않은 작업

Proposal lifecycle HTTP/UI, optimistic apply, Request/version mutation or refresh, Fieldset recalculation, RAG/LLM direct call, regex/alias routing/extraction, sanitizer/geometry/Registry/Validator/Case Matrix/Preview/Word rule duplication, database/migration/durable storage, renderer/form replacement는 추가하지 않았다.

## Worker 보고

기존 UI를 대체하지 않는 H5-ORCH-018 대화 패널을 추가했다. panel-local empty Request/Conversation bootstrap과 strict message DTO, loading/error, server response의 display-only Proposal/planner 표현만 구현했으며 승인 전 폼과 Request는 불변이다. Roadmap 상태, 기준 카드, 다음 단계 프롬프트는 변경하지 않았고 Reviewer 검토 대기로 남긴다.
