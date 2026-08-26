# H5-ORCH-020 Form and conversation synchronization MVP E2E

## Stage information

- Stage ID: `H5-ORCH-020`
- Status: Worker complete; awaiting Reviewer review.
- Project root: `request_ai_agent_h5_v0`
- Roadmap version: `2.3` (2026-08-01)
- Baseline: `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply`
- The Roadmap, baseline cards, and next-stage prompts were not changed.

## Objective and implementation

The panel-local bootstrap Request id is retained only in
`orchestratorPanelState`. Bootstrap still sends an empty body to the existing
versioned Request create endpoint, and the conversation create request receives
only that server-issued id. No form draft, legacy Request state/version,
operation, diff, or workflow event is included in bootstrap or decision DTOs.

After a valid lifecycle decision response whose matching server Proposal status
is exactly `approved`, the panel performs one existing latest-read:

```text
GET /api/request/versioned/<panel-local request_id>
```

Only that GET response supplies the adopted form `state` and
`request_version`. The code replaces the existing form state, then uses the
existing `syncEditorFromState()` and `renderDerivedPanels()` paths, so the
normal form DOM and Fieldset rendering consume the canonical server state. It
does not apply the pending diff or create any client State/version authority.

`refreshedProposalIds` consumes an approved Proposal id before its read. Thus
replayed approval results, repeated handler calls, and double-click races can
produce at most one panel refresh GET for that Proposal. The existing in-flight
decision guard remains responsible for suppressing duplicate decision clicks.

## Terminal and error boundaries

`pending`, `rejected`, `expired`, `conflicted`, `failed`, `unknown`, replay
without a first refresh, malformed/network decision results, and GET failures
do not synchronize the form or Fieldset and do not send a next message. The UI
stops on its stable Korean terminal/error status. A GET failure after an
approved server decision displays `승인됨 · 최신 의뢰서 동기화 오류`; it does
not adopt partial or cached client data and the exact-once guard prevents a
second refresh attempt.

Close/reopen preserves the panel-local runtime identity without dispatching a
lifecycle event. A separately bootstrapped panel Request remains isolated from
legacy chat/form state until its own approved latest-read. The legacy chat and
the form's ordinary user-driven flows are otherwise unchanged.

## Changed files

- `request_ai_agent_h5_v0/ui.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py`
- `docs/orchestrator_handoff/h5_orch_020_mvp_sync.md`

## Focused verification

The UI mock tests cover approved-only GET exactly once, server-only
state/version adoption, terminal/error no-sync behavior, GET failure, the
existing double-click and close/reopen guard, and legacy chat/form isolation.

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_backend_vertical_slice.py request_ai_agent_h5_v0/tests/test_orchestrator_request_version.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py
python tools/check_encoding.py --changed
git diff --check
```

## H5-021 boundary and runtime limitation

This stage only adopts the approved latest Request through existing form and
Fieldset rendering. It does not add H5-021 conditional-impact guidance,
next-field messages, workflow dispatch, RAG/LLM calls, or a form/renderer
replacement.

Request, Conversation, and Proposal records remain process-local runtime-only
stores. Restart and multi-worker deployments do not provide shared identity,
durable transaction/CAS, or durable exactly-once behavior; the refresh guard is
only an in-panel runtime guard.

## Worker report

Approved-only GET authority, pending/terminal no-sync, server latest
state/version adoption, and the exact-once refresh guard are implemented and
covered by focused mocks. Roadmap and next prompts remain unchanged for
Reviewer review.
