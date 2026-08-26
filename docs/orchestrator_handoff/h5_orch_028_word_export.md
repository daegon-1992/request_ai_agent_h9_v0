# H5-ORCH-028 Word export connection

## Status and selected authority

Worker implementation complete; awaiting Reviewer review. The Roadmap and later prompts are unchanged.

The selected Word authority remains the existing browser Preview DOM serializer,
`ui.py:previewDomForWord()`, and existing `POST /api/export/word` endpoint,
which continues to call `word_export.build_word_docx()`. No renderer, template,
document builder, Validator, Fieldset, Registry, Matrix rule, or API payload was
replaced or duplicated.

## Action and no-action boundary

The additive panel `Word output` action has no new server endpoint and sends no
Request, version, State, document, validation, readiness, or operation payload.
It is enabled only after H5-020's approved latest GET receipt and a successful
H5-027 Preview action for the same server Request id/version. The Preview DOM is
marked only when the existing `renderDocumentPreviewPanel()` receives that fenced
server response. The Word action then calls the existing
`exportWordFromPreview({useExistingPreviewDom:true})`, which serializes that DOM
through the existing serializer and posts it to the existing Word endpoint.

The legacy header Word control remains independent: without the explicit option
it retains its existing `collectState()` and Preview render behavior. The new
panel action never collects client State, rerenders Preview, adopts form data,
performs a latest GET, creates a Request or Proposal, changes the ledger, or
updates Fieldset, Matrix, Validator, workflow, chat, or legacy UI.

Missing sync, missing Preview receipt, stale DOM marker, duplicate click,
serializer/export/network/cancel failure leave Request/version/form/Preview and
all other panel boundaries unchanged. Browser download remains the pre-existing
successful endpoint side effect.

## Preserved boundaries and durability

H5-027 retains the only Preview-action server snapshot and render entry. H5-026
Validation, H5-025 Case Matrix, H5-024 Undo, H5-021 impact, H5-019 decisions,
and H5-018 panel behavior are unchanged. H5-029 RAG guidance and all persistence,
migration, renderer/template replacement, and multi-worker durability work remain
out of scope.

The H5-020 receipt, Preview-DOM marker, and click guard are browser runtime-only;
Request State and Proposal/Undo ledger remain process-local. Restart and
multi-worker deployments have no durable or cross-process guarantee.

## Changed files

- `request_ai_agent_h5_v0/ui.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_word_export.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py`
- this handoff

## Focused verification

The added tests cover unchanged DOCX endpoint output, Preview-DOM-only action
entry, H5-020/H5-027 matching receipt and marker gates, stale DOM, duplicate
click, export failure, and legacy UI isolation. The required focused suite,
encoding check, and whitespace check were run after implementation.

Executed from the project root:

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_word_export.py request_ai_agent_h5_v0/tests/test_orchestrator_preview.py request_ai_agent_h5_v0/tests/test_orchestrator_validation.py request_ai_agent_h5_v0/tests/test_orchestrator_case_matrix.py request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py request_ai_agent_h5_v0/tests/test_orchestrator_undo.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py
python tools/check_encoding.py --changed
git diff --check
```

Result: `95 passed in 5.32s`; encoding and whitespace checks passed.
