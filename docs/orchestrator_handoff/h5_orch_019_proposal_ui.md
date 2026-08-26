# H5-ORCH-019 Proposal card and approval UI

## Stage information

- Stage ID: `H5-ORCH-019`
- Status: Worker complete; awaiting Reviewer review.
- Project root: `request_ai_agent_h5_v0`
- Baseline: `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply`
- Roadmap, baseline card, and next-stage prompts were not changed.

## Objective and implementation

The additive panel UI turns the H5-018 server Proposal reference into a small
card containing only the server `proposal_id`, its status, and a read-only diff
count plus bounded changed paths (and truncation notice). Pending cards provide explicit Approve and Reject controls. The controls
are disabled while their request is outstanding and the local in-flight guard
prevents a double-click from issuing a duplicate decision request.

`POST /api/orchestrator/proposals/decision` is the minimal lifecycle HTTP
adapter. Its JSON body must be exactly:

```json
{"proposal_id":"proposal_server_issued","decision":"approve"}
```

`decision` is `approve` or `reject`. The response is only
`ok`, `proposal_id`, terminal/current `status`, and `read_only`. Invalid DTOs,
unknown IDs, and service errors return stable read-only errors. It accepts and
returns no Request state/version, form draft, operations, diff payload, result,
workflow event, or approval result state.

The adapter delegates to the existing `ProposalService`; it does not recreate
approval, rejection, expiry, validation, CAS, or replay rules. A pending approve
uses the recorded server operation and base version through the existing CAS.
The same ledger record becomes terminal (`approved`, `rejected`, `conflicted`,
or `failed`) and replay returns that record without another apply. Rejection
does not mutate the Request. Unknown, terminal, stale/conflicted, validation,
and failed results are shown as stable read-only status in the card.

## Authority and boundaries

H5-018 panel-local Request/Conversation bootstrap, legacy form, legacy chat,
and their isolation remain intact. The panel never reads `collectState()` or
legacy `requestState`, and it never places form data, Request identity/version,
operation, diff, workflow event, or result in an approval request.

Pending diff is display-only. Before approval, form DOM and Request
state/version are unchanged. After either successful or failed approval/reject,
this stage only displays the terminal/status outcome: it does not refresh a
Request, replace state, synchronize form DOM, recalculate Fieldset/Validator/
Case Matrix/Preview/Word, send a next message, or dispatch workflow planning.
There is no optimistic/direct patch, RAG/LLM call, or client routing/extraction.

H5-020 exclusively owns approved-request GET refresh and subsequent form/
Fieldset synchronization. It must use the existing versioned Request latest
read rather than reapplying a pending diff.

## Changed files

- `request_ai_agent_h5_v0/app.py`: strict lifecycle decision adapter.
- `request_ai_agent_h5_v0/ui.py`: panel Proposal card, explicit controls, and
  terminal read-only status.
- `request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py`: focused API
  authority, CAS, terminal, stale, forged-ID, validation, and apply-failure coverage.
- `request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py`: panel card,
  minimal approval DTO, double-click, diff display, terminal/error status,
  close/reopen, and legacy-isolation mocks.

## Verification

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_backend_vertical_slice.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py
python tools/check_encoding.py --changed
git diff --check
```

Focused pytest result: `66 passed in 1.40s`.

## Not run

Browser E2E, real LLM/RAG/network, external DB, restart, and multi-worker
deployment tests are outside this stage. UI behavior is tested with a Node mock
DOM/fetch runtime.

## Known limits and risks

Request, Conversation, and Proposal ledger storage remains process-local and
runtime-only. A restart loses records; separate workers have no shared identity,
transaction, CAS, or exactly-once guarantee. The in-panel click guard is a UI
guard only; the server ledger remains the runtime exact-once authority.

## Worker report

Implemented the minimal server-ledger decision adapter and isolated Proposal
card approval UI. Pending diffs remain display-only; terminal outcomes do not
refresh or synchronize the form. Focused tests pass. Roadmap state, baseline
card, and next-stage prompt remain untouched for Reviewer review.
