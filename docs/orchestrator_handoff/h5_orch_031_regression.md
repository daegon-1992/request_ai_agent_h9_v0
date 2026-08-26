# H5-ORCH-031 핵심 회귀 검증

## 단계 정보

- 단계 ID: `H5-ORCH-031`
- 단계명: 핵심 회귀 검증
- 수행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: Roadmap 기준 `69f9374` 이후의 현재 작업 트리
- Roadmap 버전: 3.4 (2026-08-01)
- 작업 상태: 완료 후보 — Reviewer 검토 대기

Roadmap, `current_stage.md`, `review_current_stage.md`, 다음 프롬프트는 변경하지 않았다.

## 이번 단계 목표

H5-009~030의 확정된 server-authority 경계와 기존 폼/API 호환성을 제한된 핵심 회귀 Matrix로 재검증했다. 신규 기능이나 endpoint는 만들지 않았으며, 재현 가능한 치명적 결함도 발견되지 않아 소스 수정은 하지 않았다.

## 사전 입력 문서

- `AGENTS.md`, 최신 Roadmap, `common_stage_contract.md`, `baseline_prompts.md`, `manual_stage_execution.md`
- `h5_orch_009_proposal_lifecycle.md`, `h5_orch_016_orchestrator_service.md`, `h5_orch_018_chat_panel.md`, `h5_orch_019_proposal_ui.md`, `h5_orch_020_mvp_sync.md`, `h5_orch_021_conditional_impact.md`
- `h5_orch_024_undo.md`부터 `h5_orch_030_audit.md`까지

## 실제 수행 내용

다음 제한된 Matrix의 기존 테스트를 실행했다.

- Request version/CAS stale·race, Proposal approve/reject/conflict/replay, 승인 전 Request 불변
- Conversation pause/terminal/Request 격리, workflow, clarification/correction
- H5-020 approved-only latest GET sync, Fieldset/conditional impact 및 Proposal UI/legacy panel 격리
- Undo success/unavailable/stale 및 inverse evidence/version fence
- Case Matrix, Validation, Preview, Word, RAG guidance의 ready/blocked/error, receipt/loading 및 legacy UI isolation
- Runtime audit의 redaction, order, replay, audit-read-failure 및 observer 비권위 경계

테스트 Matrix는 기존 authority와 contract를 검증하는 용도만으로 사용했다. Request State 직접 변경, client-provided State/version/Proposal/event/result의 authority 채택, audit payload 확장, telemetry, storage, migration, endpoint 또는 UI 문구 변경은 수행하지 않았다.

## 변경 파일

- `docs/orchestrator_handoff/h5_orch_031_regression.md` (이 문서만 신규 작성)

애플리케이션 소스와 테스트 소스는 수정하지 않았다. 한글 UI 문구도 수정하지 않았다.

## 신규 또는 변경된 데이터 구조

없음.

## 신규 또는 변경된 API

없음.

## 중요 설계 결정

- H5-009~030의 server-issued ID, latest-read/CAS, Proposal-first와 approved-only sync 경계를 기존 focused tests로 재확인했다.
- Audit은 authority 결과 뒤의 redacted process-local observer로만 남으며, State/snapshot/version, operation/diff, draft/message, RAG 원문, validation payload, Preview/Word DOM을 기록하지 않는 계약을 유지한다.
- Word의 browser DOM export와 RAG/Validator/State 원문은 audit 또는 새 telemetry로 전달하지 않았다.

## 기존 기능 재사용 지점

기존 RequestStateStore, ProposalService/ledger, Conversation/workflow, H5-020 sync, H5-024 undo, H5-025~029 action services, RuntimeAuditLog 및 각 focused test를 그대로 사용했다.

## 수행하지 않은 작업

- 신규 기능/endpoint, durable storage·transaction·queue, DB migration, 외부 telemetry, RAG index/vector DB, renderer/template 교체, LLM 권한 확대
- 전체 조합 또는 실제 browser/LLM/RAG/network E2E 확장
- 원인이 없는 예방적 수정 또는 대규모 리팩터링

## 최소 검증

실제 프로젝트 루트 `G:\\Tech\\00_Agent\\01_Agent_Code\\request_ai_agent_h5_v0`에서 실행했다.

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_request_version.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_conversation_store.py request_ai_agent_h5_v0/tests/test_orchestrator_conversation_api.py request_ai_agent_h5_v0/tests/test_orchestrator_workflow_machine.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py request_ai_agent_h5_v0/tests/test_orchestrator_backend_vertical_slice.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py request_ai_agent_h5_v0/tests/test_orchestrator_clarification.py request_ai_agent_h5_v0/tests/test_orchestrator_correction.py request_ai_agent_h5_v0/tests/test_orchestrator_undo.py request_ai_agent_h5_v0/tests/test_orchestrator_case_matrix.py request_ai_agent_h5_v0/tests/test_orchestrator_validation.py request_ai_agent_h5_v0/tests/test_orchestrator_preview.py request_ai_agent_h5_v0/tests/test_orchestrator_word_export.py request_ai_agent_h5_v0/tests/test_orchestrator_rag_guidance.py request_ai_agent_h5_v0/tests/test_orchestrator_audit.py request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py
python tools/check_encoding.py --changed
git diff --check
```

결과:

- pytest: `159 passed in 6.71s` (21 files, collect 159 items)
- `python tools/check_encoding.py --changed`: `Encoding check passed`
- `git diff --check`: 성공 (출력 없음)

## 실패하거나 실행하지 못한 검증

처음 workspace 루트에서 같은 명령을 실행하면 `..\\.venv\\Scripts\\python.exe`가 존재하지 않아 시작 전 실패했다. workspace 루트에서 `..\\.venv`를 `.\\.venv`로 바꿔도 test 경로가 한 단계 더 깊어 `file or directory not found`로 수집 전 실패했다. 둘 다 코드/테스트 실패가 아니라 실행 기준 경로 불일치이며, 위의 실제 프로젝트 루트에서 원문 명령은 정상 완료됐다.

실제 browser E2E, 실제 LLM/RAG/network, restart, multi-worker, 외부 DB/durable storage 검증은 이번 focused Matrix 범위 밖이며 실행하지 않았다.

## 알려진 문제와 제한사항

Request State, Conversation, Proposal/Undo ledger, H5-020 receipt, action receipt/DOM marker/loading guard 및 audit event는 process-local runtime state다. restart, capacity rollover, multi-worker 환경에서 shared identity/order, durable CAS/ledger, transaction, cross-process exactly-once를 제공하지 않는다. 이 단계는 그 한계를 변경하거나 은폐하지 않았다.

## 발견된 위험

- 현재 작업 트리에는 선행 단계의 미커밋 변경과 untracked 파일이 다수 존재한다. 이번 단계는 이를 보존했고, 신규 handoff 외에는 변경하지 않았다.
- 실행 명령은 반드시 Git 프로젝트 루트에서 수행해야 한다. 상위 workspace에서의 상대 가상환경/test 경로는 재현 가능한 운영상 혼동 요인이다.

## 다음 단계에서 반드시 참고할 내용

H5-032는 이 Matrix가 통과한 authority 경계를 변경해서는 안 된다. 안정화가 필요하더라도 재현 가능한 결함의 최소 원인과 수정 파일이 먼저 증명되어야 하며, H5-019 decision DTO, H5-020 approved-only sync, H5-024 inverse fence, H5-025~030 explicit Action/audit-redaction 계약은 유지해야 한다.

## 다음 단계 수정이 예상되는 파일

현재 회귀 결과만으로 필수 수정 파일은 없다. H5-032 후보가 별도로 승인되고 실행 경로 혼동을 문서화할 필요가 확인될 때에만 stage execution 안내 문서가 최소 후보이며, Roadmap/다음 프롬프트는 Reviewer/Planner 절차 전까지 변경하지 않는다.

## 후속 개선 후보

1. 동일한 실행 기준 프로젝트 루트를 모든 수동 실행 안내에 명시하는 운영상 정합성 점검.
2. durable shared storage, transaction, multi-worker idempotency/audit은 별도 권한·설계·migration이 필요한 후속 과제로만 검토.

둘 다 이번 단계에서 구현하지 않았다.

## Roadmap 변경 필요 여부

없음. Worker는 완료를 확정하지 않으며 Reviewer `approved`, `safe_to_continue=true` 판정 전까지 H5-031은 Reviewer 검토 대기다.

## Worker 결과 보고

1. 변경 파일: 이 handoff 문서만 작성.
2. 구현 또는 조사 내용: H5-009~030 핵심 authority/API/UI isolation 회귀 Matrix 실행.
3. 미수정·미완료 내용: 코드 수정 없음; durable/multi-worker 및 full E2E는 범위 밖.
4. 수행한 테스트: 지정된 21개 pytest 파일, 인코딩, diff 검사.
5. 테스트 결과: `159 passed in 6.71s`, 인코딩·공백 검사 통과.
6. 발견된 문제와 위험: 코드 결함 없음; 상위 workspace 실행 경로 혼동과 process-local runtime-only 한계 기록.
7. 다음 단계 영향: H5-032는 경계 보존 및 재현 가능한 최소 수정만 허용.
8. 생성한 인수인계 문서: 이 문서.
9. Git 상태와 Commit 여부: 선행 단계의 광범위한 기존 dirty/untracked 상태를 보존했고 commit 하지 않음.
