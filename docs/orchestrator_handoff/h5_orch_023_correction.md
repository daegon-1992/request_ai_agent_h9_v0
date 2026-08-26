# H5-ORCH-023 Existing-value correction

## Stage information

- Stage ID: `H5-ORCH-023`
- Status: Worker complete; awaiting Reviewer review.
- Project root: `request_ai_agent_h5_v0`
- Baseline: `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply -> latest GET sync`
- Roadmap and following-stage prompts were not changed.

## Chosen authority

`OrchestratorService` first reads the active Conversation and its server latest
Request snapshot.  It supplies that snapshot to the existing extraction Tool,
whose existing sanitizer and geometry Adapter remain the only candidate
authority.  The existing Intent Router remains the only allowed-intent and
ordered-reason authority.

For exactly one sanitized Tool candidate, the service applies the existing
canonical patch adapter to a copy of that latest State.  It considers the
candidate a correction only when the candidate's existing Field Registry or
geometry Adapter canonical binding has a non-empty value and the resulting
canonical State differs.  No client draft, cached response, pending Proposal,
or client version contributes to that decision.

The existing `ProposalService.create_proposal` remains the sole correction
dry-run, diff, source, base-version, ledger, and later CAS-approval authority.
Correction records retain `source="orchestrator_llm"`. The service passes its
server-read snapshot version into the existing ProposalService version fence;
a concurrent Request write therefore produces a stable no-Proposal failure
instead of a no-op ledger record. ProposalService still performs the latest
read, dry-run, ledger write, and records the base version. The response remains
the existing display-only Proposal DTO, so the existing panel card renderer
needs no special correction branch.

## Correction and no-Proposal boundary

- A single differing candidate for a populated canonical value creates a
  pending Proposal.  Proposal creation does not dispatch a workflow event.
- A canonical same-value candidate returns the H5-022 read-only clarification
  shape with ordered reasons `intent_patch`, `tool_candidates`, `same_value`.
  It creates no ledger entry.
- Unsupported fields, plural candidates, missing units, ambiguous values,
  blank/irrelevant messages, and Tool/LLM failures retain the H5-022 Router and
  Tool ordered clarification reasons/questions.  They create no Proposal.
- Stable service failures remain read-only failures.  The service neither
  selects candidates nor infers fields, values, or units.

The pre-existing initial-value Proposal behavior remains available for an empty
canonical field; this stage only adds the existing-value correction boundary.

## Sync, lifecycle, and later-stage boundaries

Pending correction diffs are display-only.  Before approval they do not change
Request State/version, form DOM, Fieldset/Registry/Validator, Case Matrix,
Preview, Word, or workflow.  Clarification also has no sync, planner, workflow,
or follow-up-message effect.

Approval continues through the unchanged decision endpoint and `ProposalService`
CAS/ledger behavior.  H5-020 remains the exclusive owner of approved-only
latest GET and form synchronization; H5-021 remains the exclusive owner of
approved conditional-impact guidance.  H5-024 Undo is not implemented here:
there is no inverse Proposal, rollback, or replay change.

Request, Conversation, and Proposal storage remains process-local and
runtime-only.  Restart or multi-worker deployment has no shared identity,
durable transaction/CAS, or durable exactly-once guarantee.

## Changed files

- `request_ai_agent_h5_v0/orchestrator_service.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_correction.py`
- `docs/orchestrator_handoff/h5_orch_023_correction.md`

## Focused verification

The new focused tests prove that a populated server latest value produces a
Proposal with the server Request id/base version, remains unchanged before
approval, and applies only through the existing decision plus latest GET path.
They also prove same-value clarification is deterministic Korean read-only,
the server version fence rejects a concurrent write without a no-op ledger
record, and a condition correction reads the Registry canonical condition set
instead of a legacy transport row. Existing focused suites retain
clarification, Tool/Router ordering, proposal lifecycle/CAS, backend slice,
panel, sync, and conditional-impact coverage.

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_correction.py request_ai_agent_h5_v0/tests/test_orchestrator_clarification.py request_ai_agent_h5_v0/tests/test_orchestrator_intent_router.py request_ai_agent_h5_v0/tests/test_orchestrator_extraction_tool.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py request_ai_agent_h5_v0/tests/test_orchestrator_backend_vertical_slice.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py
python tools/check_encoding.py --changed
git diff --check
```

Focused test result: `91 passed in 1.78s`; encoding and whitespace checks passed.

## Worker report

Implemented the smallest server-only correction gate and left Router, Tool,
Proposal lifecycle/CAS/replay, approval UI, approved-only sync, and conditional
impact paths in place.  Roadmap and next prompts remain untouched for Reviewer
review.
