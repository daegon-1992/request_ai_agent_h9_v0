# H5-ORCH-027 Preview connection

## Status and selected authority

Worker implementation complete; awaiting Reviewer review. The Roadmap and
following-stage prompts are unchanged.

The selected active Preview authority is the existing browser renderer,
`ui.py:renderDocumentPreviewPanel()`. The investigation confirmed that
`POST /api/document-preview` is disabled and its `preview_document.py` path is
legacy-shaped; this stage neither enables nor treats it as the active Preview
contract. `POST /api/preview` is also a client-State normalization endpoint, so
it is not an authority boundary for the panel action.

`PreviewActionService` is a read-only server adapter. It accepts only a
server-issued Request id, reads its latest canonical stored snapshot, and uses
`RequestStateStore.at_version()` to fence that read. It does not select or run
a renderer, call `sanitize_state()`, `validate_state()`, or
`review_pipeline`, create a document, calculate readiness, or alter a Request.
On a successful response the panel calls the one existing browser Preview entry
with the returned fenced server snapshot. The response is server output, never
client-provided State, preview, document, validation, version, operation, or
explanation authority. Existing `review.validator` evidence remains part of
the canonical State unchanged; the panel creates no readiness or blocking
judgment.

## Action and no-action contract

`POST /api/orchestrator/preview/action` accepts exactly:

```json
{"request_id":"server_issued_panel_request"}
```

The explicit `Preview 확인` control reuses the H5-020 successful latest-GET
receipt already used by H5-025 and H5-026. It needs the matching approved
panel Request id/version before it can send its id-only DTO. The receipt is
invalidated before a newer approved GET and stays invalid after a failed or
malformed GET. The receipt id/version is not sent to the endpoint.

`preview_ready` contains the fenced server snapshot and version. The panel
only enters the existing Preview if the returned id/version still match that
receipt and the existing canonical State shape. It passes the server response
directly to `renderDocumentPreviewPanel(state)` without adopting it into the
form or `requestState`. `request_not_found`, `request_version_conflict`,
`preview_read_failed`, malformed/network responses, stale returned versions,
and unsynced attempts leave the legacy Preview DOM, Request/version/form,
Fieldset, Matrix, validation UI, Proposal/Undo ledger, chat, and workflow
unchanged. Replays are equivalent fenced reads; panel double-clicks are locally
suppressed. This action does not perform CAS or another H5-020 GET sync.

## Preserved and deferred boundaries

H5-026 Validation and H5-025 Matrix actions retain their existing receipt gate
and endpoints. H5-024 Undo evidence/version fence/ledger, H5-021 impact,
H5-019 decision DTO, and H5-018 loading and close/reopen behavior are not
changed. Legacy preview, chat, form, Matrix, and validation remain independent.

H5-028 owns Word behavior. In particular, this action does not call the Word
export path or change its existing browser-DOM contract. Renderer replacement,
server document-preview activation, templates, Fieldset/Registry/Matrix rule
changes, LLM/RAG generation, persistence, and migrations remain out of scope.

## Changed files

- `request_ai_agent_h5_v0/preview_action.py`
- `request_ai_agent_h5_v0/app.py`
- `request_ai_agent_h5_v0/ui.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_preview.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py`
- this handoff

## Runtime-only durability limit

Request State, Proposal/Undo ledger, H5-020 receipt, and click guards remain
process-local runtime state. Restart and multi-worker deployments have no
shared identity, durable CAS/ledger, transaction, or cross-process
exactly-once guarantee. No DB, migration, or durable storage was introduced.

## Focused verification

Executed from the project root with the workspace virtual environment:

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_preview.py request_ai_agent_h5_v0/tests/test_orchestrator_validation.py request_ai_agent_h5_v0/tests/test_orchestrator_case_matrix.py request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py request_ai_agent_h5_v0/tests/test_orchestrator_undo.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py
python tools/check_encoding.py --changed
git diff --check
```

Result: `91 passed in 5.20s`; encoding and whitespace checks passed.
