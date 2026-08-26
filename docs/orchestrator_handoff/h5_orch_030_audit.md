# H5-ORCH-030 Audit·최소 관측성

## 상태

Worker 구현 완료, Reviewer 검토 대기. Roadmap과 다음 프롬프트는 변경하지 않았다.

## 선택한 audit authority

`RuntimeAuditLog`는 `app.py`의 HTTP adapter에서 **기존 authority가 결과를
결정한 뒤** 실행되는 process-local, append-only observer다. Proposal lifecycle,
Request CAS, Conversation transition, Undo, H5-025 Case Matrix, H5-026
Validation, H5-027 Preview, H5-029 RAG guidance의 기존 result DTO/status를
재사용한다. observer는 Request write/CAS, Proposal·Undo ledger, workflow,
form sync, Matrix/Validator/Preview/Word/RAG 실행 또는 message dispatch를 호출하거나
재구현하지 않는다.

## event/redaction/order/replay contract

각 event는 server-generated `event_id`, UTC `timestamp`, monotonic process-local
`sequence`, `action`, `result_code`, `status`, 그리고 authority가 반환한
server-issued `request_id`/`conversation_id`/`proposal_id`만 가진다. `sequence`가
유일한 order metadata다. State/snapshot/version, operation/diff, draft/message,
RAG question/answer/evidence, validation payload, Preview/Word DOM, secret와
환경값은 기록·반환·해시하지 않는다.

`GET /api/orchestrator/audit/events`는 bounded redacted DTO만 반환한다. 입력을
받지 않으며 audit event나 business result를 client가 제공·수정할 수 없다.
unknown/malformed client ID와 malformed DTO는 기존 stable result만 반환하고
event를 추가하지 않는다. audit read failure는 `audit_read_failed`의 bounded 빈
event DTO와 `read_only=true`만 반환하며, 정상 replay는 기존 authority 결과 뒤에 invocation당
하나의 새 observer event만 추가한다. audit append/read failure는 기존 결과나
mutation을 바꾸지 않는다.

## observed / no-observed boundary

- Observed: Proposal approve/reject/conflict terminal result, Request CAS
  success/conflict, server-validated paused/terminal workflow message failure,
  Conversation transition, Undo success/unavailable, and H5-025/026/027/029
  server Action results.
- Not observed: H5-028 explicit Word action. 이것은 server Action endpoint가
  없는 browser Preview DOM serializer/export 경로이므로 DOM/document payload를
  observer로 보내지 않는다. legacy chat/form/Preview/Word UI도 관측 authority가
  아니다.

## 보존된 경계

H5-019 decision DTO, H5-020 approved-only latest GET sync, H5-021 impact,
H5-024 inverse evidence/version fence, H5-025~029 Action/receipt gates와
H5-018 close-reopen/loading을 변경하지 않았다. database/migration, file/network
telemetry, durable queue/transaction, external observability, renderer/template,
RAG index는 추가하지 않았다.

## 변경 파일

- `request_ai_agent_h5_v0/orchestrator_audit.py`
- `request_ai_agent_h5_v0/app.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_audit.py`
- this handoff

## focused verification

프로젝트 루트에서 실행:

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_audit.py request_ai_agent_h5_v0/tests/test_orchestrator_rag_guidance.py request_ai_agent_h5_v0/tests/test_orchestrator_word_export.py request_ai_agent_h5_v0/tests/test_orchestrator_preview.py request_ai_agent_h5_v0/tests/test_orchestrator_validation.py request_ai_agent_h5_v0/tests/test_orchestrator_case_matrix.py request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py request_ai_agent_h5_v0/tests/test_orchestrator_undo.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py
python tools/check_encoding.py --changed
git diff --check
```

Final result: `103 passed in 5.64s`; `Encoding check passed`; `git diff --check`
passed with no output.

## runtime-only durability limit

Audit events are bounded process-local runtime memory. Restart, multi-worker,
or audit capacity rollover loses shared history/order and provides no durable
transaction, cross-process sequencing, or exactly-once guarantee. Request State,
Proposal/Undo ledger, and panel receipts retain their pre-existing runtime-only
limits.
