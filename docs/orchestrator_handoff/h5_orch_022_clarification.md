# H5-ORCH-022 Ambiguous responses and clarification

## Stage information

- Stage ID: `H5-ORCH-022`
- Status: Worker complete; awaiting Reviewer review.
- Project root: `request_ai_agent_h5_v0`
- Roadmap version: `2.5` (2026-08-01)
- Baseline: `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply -> latest GET sync`
- Roadmap and following-stage prompts were not changed.

## Chosen authority and boundary

`orchestrator_extraction_tool.py` remains the only source of sanitized Tool
candidates/failures and ordered `ExtractionReasonDTO` values. The Intent Router
continues to accept only the existing LLM intent vocabulary and now labels a
plural candidate list as `multiple_candidates`; it does not select one.

`OrchestratorService` is the clarification authority. A blank patch message,
plural candidates, no candidate (including ambiguous value, missing unit, and
irrelevant input), or Tool/LLM failure returns an
`OrchestratorClarificationResult`. It never creates a Proposal, invokes the
next-field planner, dispatches workflow, or writes Request/Conversation state.
The app endpoint serializes this solely as a read-only response. The panel
renders its server-provided Korean `question`; it does not infer fields,
candidates, values, units, or ambiguity.

## Stable response contract

Successful clarification responses contain only:

```json
{
  "ok": true,
  "kind": "clarification",
  "route_category": "needs_clarification",
  "reasons": ["intent_patch", "tool_no_candidate", "missing_unit"],
  "question": "값의 단위를 함께 알려주세요. 예: 25 °C",
  "state_changed": false,
  "read_only": true
}
```

Reasons preserve Router order followed by the Tool's existing ordered reason
list, with the server-only `empty_message` or `multiple_candidates` boundary
code where applicable. The Korean question is selected by that ordered,
server-owned result and is deterministic. No client draft or pending Proposal
is read as authority.

## No-sync and error boundary

Clarification does not perform the H5-020 approved-only latest GET, form sync,
Fieldset rendering, conditional-impact rendering, workflow dispatch, or an
additional message. Existing approved Proposal decision and H5-021 impact paths
are unchanged. Tool/LLM failures return the same stable read-only clarification
shape; closed/paused/request/service failures remain the existing stable error
responses.

## H5-023 and durability boundary

This stage does not correct an existing value, create a replacement Proposal,
implement Undo, or change Proposal lifecycle/CAS/replay semantics. Request,
Conversation, and Proposal stores remain process-local runtime-only stores;
restart and multi-worker deployments still have no shared durable identity,
transaction/CAS, or exactly-once guarantee.

## Changed files

- `request_ai_agent_h5_v0/orchestrator_intent_router.py`
- `request_ai_agent_h5_v0/orchestrator_service.py`
- `request_ai_agent_h5_v0/app.py`
- `request_ai_agent_h5_v0/ui.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_clarification.py`
- focused existing Router/service/backend tests
- this handoff document

## Focused verification

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_clarification.py request_ai_agent_h5_v0/tests/test_orchestrator_intent_router.py request_ai_agent_h5_v0/tests/test_orchestrator_extraction_tool.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py request_ai_agent_h5_v0/tests/test_orchestrator_backend_vertical_slice.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py
python tools/check_encoding.py --changed
git diff --check
```

Focused pytest result: `87 passed in 1.59s`.
