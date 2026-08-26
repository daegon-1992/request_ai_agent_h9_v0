# H5-ORCH-026 Validation connection

## Status and selected authority

Worker implementation complete; awaiting Reviewer review.  The Roadmap and
following-stage prompts are unchanged.

The selected existing authority is `validator.validate_state()`.  It retains
its existing `state.sanitize_state()` entry, readiness summary, blocking,
warning and info issues, section/path bindings, and Case Matrix validation.
Neither the panel nor the Orchestrator duplicates a Validator rule, Fieldset,
Registry, Matrix rule, readiness decision, or next question.

`ValidationActionService` is only a read-only adapter.  It reads the
panel-local server Request's latest snapshot, then uses
`RequestStateStore.at_version()` while `validate_state()` runs.  The API returns
the raw Validator result without filtering, translating, or synthesizing its
issue evidence.  It has no client State, draft, validation result, Request
version, operation, Proposal, workflow, LLM, or RAG input.

## Action and no-action contract

`POST /api/orchestrator/validation/action` accepts exactly:

```json
{"request_id":"server_issued_panel_request"}
```

The explicit `Validation 확인` panel control uses the same display-only H5-020
latest-GET receipt already used by H5-025 Case Matrix.  It is available only
after an approved Proposal's successful latest GET has adopted the matching
server Request id and version.  A newer approval invalidates the receipt before
its GET; a malformed or failed GET leaves it invalid.  The receipt id/version
is never sent to the Action endpoint.

Inside the version fence, `validate_state()` is called exactly once.  A result
with existing blocking evidence returns `validation_blocked`; a result without
blocking evidence returns `validation_ready`.  Both responses contain the
unmodified canonical Validator payload.  Unknown Requests return
`request_not_found`; a latest-version race returns `request_version_conflict`;
Validator or normalizer exceptions return `validation_failed`.  Malformed HTTP
DTOs return `invalid_validation_action_payload`.  Replays are equivalent
read-only evaluations, and panel double-clicks are locally suppressed.

No result performs Request CAS, H5-020 GET synchronization, form adoption,
Fieldset or Matrix updates, Proposal creation/decision, Undo, workflow
transition, follow-up message, or legacy validation UI update.  Request State,
version, form, Fieldset, Matrix, and Proposal/Undo ledger remain unchanged
before and after the action.

## Preserved boundaries

H5-025's Matrix Action and its sync gate remain unchanged.  H5-024's inverse
evidence, version fence, and ledger remain unchanged.  H5-019 retains the sole
decision DTO, H5-020 retains approved-only latest GET/form synchronization, and
H5-021 retains conditional-impact display.  Existing chat, form, Matrix, and
validation UI remain independently functional.

H5-027 Preview and later Preview, Word, RAG, renderer replacement, persistence,
and durability work remain out of scope.

## Changed files

- `request_ai_agent_h5_v0/validation_action.py`
- `request_ai_agent_h5_v0/app.py`
- `request_ai_agent_h5_v0/ui.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_validation.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py`
- this handoff

## Runtime-only durability limit

Request State, Proposal/Undo ledger, panel latest-GET receipt, and click guards
remain process-local runtime state.  Restart and multi-worker deployment do not
provide shared identity, durable CAS/ledger, transactions, or cross-process
exactly-once behavior.  No DB, migration, or durable storage was introduced.

## Focused verification

Executed from the project root with the workspace virtual environment:

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_validation.py request_ai_agent_h5_v0/tests/test_orchestrator_case_matrix.py request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py request_ai_agent_h5_v0/tests/test_orchestrator_undo.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py
python tools/check_encoding.py --changed
git diff --check
```

Result: `86 passed in 5.06s`; encoding and whitespace checks passed.
