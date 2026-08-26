# H5-ORCH-029 RAG 근거 안내 연결

## 단계 정보

- 단계 ID: `H5-ORCH-029`
- 상태: 완료 후보 — Reviewer 검토 대기
- 프로젝트 루트: `request_ai_agent_h5_v0`
- Roadmap: 3.1 (2026-08-01)
- Roadmap과 다음 프롬프트는 변경하지 않았다.

## 선택한 기존 RAG authority

기존 `rag_qa.run_rag_qa()`와 그 반환 QA/evidence DTO를 그대로 사용했다.
`RagGuidanceActionService`는 server-issued panel-local `request_id`가 존재하는지와
동시 write가 없는지만 `RequestStateStore.at_version()`으로 fence한다. snapshot의
`state`는 읽거나 RAG에 전달하지 않는다. RAG의 유일한 입력은 명시적으로 입력한
문서 질문이며 호출은 `run_rag_qa(question, state=None)`이다. 따라서 client State,
draft, Preview/Word DOM, validation, operation, Proposal, Request snapshot/version은
RAG 입력이나 결과 authority가 아니다.

`current input` 질문은 기존 structured-state Q&A 경로이므로 이 Action에서는
`rag_guidance_requires_document_question` stable read-only result로 차단한다.

## Action/no-Action 경계

`POST /api/orchestrator/rag-guidance/action`은 정확히 다음 DTO만 받는다.

```json
{"request_id":"server_issued_panel_request","question":"explicit document question"}
```

panel의 `RAG 근거 안내`는 기존 panel Request id가 이미 있을 때만 동작한다. Request나
Conversation을 bootstrap하지 않고, sync receipt도 필요로 하지 않으며 H5-020 GET을
호출하지 않는다. UI는 existing `qa.answer_text`와 existing `sources`, score,
confidence, limitations, source_types DTO를 display-only로 보인다. 문서, 근거, 점수,
번역, 요약, next question, workflow 결정을 새로 만들지 않는다.

Action은 Request CAS/write, form adoption, Fieldset/Matrix/Validator/Preview/Word,
Proposal 생성·결정, Undo, workflow dispatch, message dispatch를 실행하지 않는다.
H5-019 decision DTO, H5-021 impact, H5-024 inverse evidence/version fence,
H5-025~028 receipt/action boundaries는 변경하지 않았다.

## evidence/no-result/error/stale/duplicate/cancel 계약

- 정상 기존 evidence는 `rag_guidance_ready`로 원본 `qa`를 보존한다.
- 빈 existing sources는 `rag_guidance_no_result`, existing `rag_disabled`는
  `rag_guidance_disabled`, existing `rag_error`/runner error는
  `rag_guidance_error`다.
- malformed existing QA DTO는 `rag_guidance_malformed`, unknown Request는
  `request_not_found`, concurrent fence race는 `request_version_conflict`다.
- replay는 동일한 read-only evaluation이고 UI double-click은 local loading guard가
  억제한다. network/cancel/malformed HTTP response는 panel stable error로 표시한다.
- 이 모든 결과는 Request/version/form/Fieldset/Matrix/Proposal·Undo ledger/legacy
  chat/Preview/Word UI를 변경하지 않는다.

## 변경 파일

- `request_ai_agent_h5_v0/rag_guidance_action.py`
- `request_ai_agent_h5_v0/app.py`
- `request_ai_agent_h5_v0/ui.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_rag_guidance.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py`
- 이 handoff

## focused 검증

새 tests는 server fence가 Request snapshot 대신 id/race 확인에만 사용되고 runner가
`state=None`만 받는 것, existing evidence/no-result/disabled/error/malformed,
unknown/race/replay, strict action DTO, Request/Proposal ledger 불변 및 panel legacy
isolation을 검증한다.

실행 명령:

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_rag_guidance.py request_ai_agent_h5_v0/tests/test_orchestrator_word_export.py request_ai_agent_h5_v0/tests/test_orchestrator_preview.py request_ai_agent_h5_v0/tests/test_orchestrator_validation.py request_ai_agent_h5_v0/tests/test_orchestrator_case_matrix.py request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py request_ai_agent_h5_v0/tests/test_orchestrator_undo.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py
python tools/check_encoding.py --changed
git diff --check
```

실행 결과: `99 passed in 5.46s`; `python tools/check_encoding.py --changed`는
`Encoding check passed`, `git diff --check`는 성공(출력 없음)이었다.

## H5-030 이후 및 runtime 한계

H5-030 audit/observability, durable idempotency, shared storage, transaction,
restart/multi-worker semantics는 이 단계 범위 밖이다. Request, Conversation,
Proposal/Undo ledger, fence와 panel loading guard는 process-local runtime-only이며
cross-process durability, transaction, exactly-once를 주장하지 않는다.
