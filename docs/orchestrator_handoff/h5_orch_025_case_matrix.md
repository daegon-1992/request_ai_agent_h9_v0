# H5-ORCH-025 Case Matrix connection

## Status and selected authority

Worker implementation complete; awaiting Reviewer review. Roadmap and later prompts are unchanged.

The selected existing Case Matrix authority is `case_matrix.generate_case_matrix()`. It delegates to `state.sanitize_state()` and retains existing manual Matrix normalization: active columns, condition choices, row retention/clearing, geometry rows, and validation are not duplicated by Orchestrator or the panel.

The added `CaseMatrixActionService` is a read-only adapter. It accepts only a panel-local, server-issued `request_id`, reads the server latest snapshot, and uses `RequestStateStore.at_version()` to fence the read while the existing Validator and Matrix engine run. It returns only a display-only Matrix summary; it has no client State, Matrix row, operation, Request-version, Proposal, workflow, or LLM/RAG input.

## Action and no-action boundary

`POST /api/orchestrator/case-matrix/action` accepts exactly:

```json
{"request_id":"server_issued_panel_request"}
```

The panel's explicit `Case Matrix 확인` control is available only after H5-020 has successfully adopted an approved latest GET for its existing panel-local Request id. The panel keeps a display-only sync receipt containing that server GET's request id and version; it sends neither value to the Action endpoint. A newer approved write invalidates the receipt before its GET, and a malformed or failed GET leaves it invalid. The control does not bootstrap a Request, read the legacy form/draft, or use cached State/version as Action authority. A second click while pending is ignored.

Within the version fence, the existing `validate_state()` result is the sole readiness gate. Existing blocking codes return `case_matrix_blocked`; only a non-blocked canonical Request enters `generate_case_matrix()`. The success response is `case_matrix_ready` with server-derived counts only. It never adopts returned data into form DOM, Fieldset, or legacy Matrix UI.

Unknown Request, concurrent latest-version race, malformed DTO, duplicate read-only action, engine/normalizer failure, and Validator blocking return stable read-only results. None writes Matrix, Request/version, Proposal or Undo ledger, form, Fieldset, conversation, workflow, or chat message.

## Approval, Undo, and later-stage boundaries

This read-only Matrix action neither creates nor decides a Proposal. H5-019 decision DTO and H5-024 inverse evidence/version fence/replay ledger remain unchanged. It does not perform H5-020 synchronization: because the selected engine is read-only, there is no Request CAS success and no latest GET. The existing H5-020 approved-Proposal path remains the exclusive form/Fieldset latest-GET exact-once boundary.

H5-021 canonical conditional impact remains display-only and unchanged. Validation presentation/connection is deferred to H5-026; Preview, Word, RAG, renderer/form replacement, Matrix editing UI changes, persistence, and durability work are out of scope.

## Changed files

- `request_ai_agent_h5_v0/case_matrix_action.py`
- `request_ai_agent_h5_v0/app.py`
- `request_ai_agent_h5_v0/ui.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_case_matrix.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py`
- this handoff

## Focused verification

The focused tests cover server-latest-only engine entry, client Matrix/state exclusion, pre-success Request/version/ledger invariance, Validator blocking, unknown id, fenced stale race, duplicate/replay, engine failure, request-id-only UI payload, H5-020-success receipt gating, GET-failure invalidation, double-click/loading, no legacy chat/form/Matrix sync, and the existing Proposal/Undo/H5-020/H5-021/panel suites.

Executed from the project root with the workspace virtual environment:

```powershell
& G:\Tech\00_Agent\01_Agent_Code\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_case_matrix.py request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py request_ai_agent_h5_v0/tests/test_orchestrator_undo.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py
```

Result after the final correction: `81 passed`.

## Runtime-only limit

Request State, Proposal/Undo ledger, and panel click guards remain process local and runtime-only. Restart and multi-worker deployment do not provide shared identity, durable CAS/ledger, transactions, or cross-process exactly-once behavior. No migration or durable storage was introduced.
