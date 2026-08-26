# H5-ORCH-009 Proposal approval lifecycle

## 1. Current situation

- Current stage: `H5-ORCH-009`; roadmap version is 1.0 and remains awaiting Reviewer review.
- Baselines: `69f9374`, `c1ab16f`, and the flow `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply`.
- H5-ORCH-008 already provides server-issued, pending `ProposalSnapshot` records with the authoritative `request_id`, `base_version`, and normalized operations.
- The focused implementation is limited to `proposal_store.py` and its focused tests. Existing request, Field Registry, UI, and legacy API paths are unchanged.

## 2. Objective

Provide a bounded internal lifecycle that resolves only a server-ledger pending Proposal. Approval must reapply the server-recorded normalized operations exactly once through the recorded Request CAS; rejection and expiration must be terminal, non-mutating decisions.

## 3. Scope

- Added `ProposalService.approve_proposal(proposal_id)`, `reject_proposal(proposal_id)`, and `expire_proposal(proposal_id)`.
- Added terminal ledger persistence (`approved`, `rejected`, `expired`, `conflicted`, or `failed`) with immutable result metadata and `resolved_at`.
- Added focused lifecycle tests for normal approval, replay, reject/expire, unknown IDs, stale CAS conflict, validation/apply failure, and canonical approved apply.

No public endpoint, client-held legacy-flow replacement, Conversation/Workflow/Planner/UI work, database migration, external storage, or LLM/RAG call was added.

## 4. Implementation safeguards

- The lifecycle methods accept only `proposal_id`; they cannot receive client Proposal data, operations, Request State, Request ID, or base version.
- They read the Proposal from `ProposalStore`; the server-recorded `request_id`, `base_version`, and normalized operations are the only approval inputs.
- `approve_proposal()` calls `RequestStateStore.compare_and_swap(record.request_id, record.base_version, mutation)`. The mutation invokes the existing `apply_patch_operations(current, record.operations)`.
- Therefore the established sanitizer/geometry Adapter, `sanitize_state()`, `state_with_validation()`, active conditional cleanup, Validator, and Case Matrix finalization remain authoritative. No rule is copied into the lifecycle service.
- `ProposalStore` owns a process-local lifecycle `RLock`. Every service sharing that store holds it from pending-record read through CAS and terminal ledger write. A replay sees the terminal record and returns it without another apply.
- `RequestStateStore` commits only after mutation and canonical finalization succeed. Only the successful approved CAS increases Request version, by exactly one.

## 5. Work performed

1. Confirmed the H5-ORCH-008 ledger and H5-ORCH-007 latest-read/CAS boundary.
2. Extended the bounded in-memory ledger with terminal snapshot replacement and a shared lifecycle lock.
3. Implemented the internal lifecycle service surface and focused invariant tests.
4. Kept Roadmap state, baseline cards, and next-stage prompts unchanged for Reviewer review.

## 6. Modified files

- `request_ai_agent_h5_v0/proposal_store.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py`
- `docs/orchestrator_handoff/h5_orch_009_proposal_lifecycle.md`

## 7. Explicitly excluded work

- No direct Request version update and no trust in a client-supplied base/version.
- No client Proposal/operation/State authorization, no public HTTP lifecycle endpoint, and no optimistic UI state.
- No Fieldset, normalizer, Validator, Case Matrix, Preview, Word, or renderer change.
- No regex/alias extractor, keyword/regex intent router, legacy `geometry.products` State persistence, durable DB, migration, multi-worker transaction, or deployment test.

## 8. Required validation

Executed only focused tests:

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_request_version.py request_ai_agent_h5_v0/tests/test_orchestrator_field_registry.py
```

Result: `24 passed`.

The lifecycle tests establish that:

- a server-recorded Proposal applies once, increments version once, and replay does not call apply a second time;
- reject and expire, unknown Proposal IDs, stale CAS conflict, and validation/apply failure leave Request State/version unchanged and record the appropriate terminal result where a ledger record exists;
- approved geometry input uses the existing Adapter, does not store `geometry.products`, and produces the same canonical State/review result as existing `apply_patch_operations()` finalization.

`python tools/check_encoding.py --changed` and `git diff --check` are final checks to run after all staged-file edits are complete.

## 9. High-cost validation not run

Full E2E, real LLM/RAG/external DB, and multi-worker deployment tests were not run: they are outside this bounded internal-stage scope.

## 10. Completion conditions

The implementation provides server-ledger-only lifecycle decisions, CAS-backed approved apply, terminal replay safety, and focused proof of Request/version non-mutation on all unsuccessful paths. Reviewer verification of the final diff and required repository checks remains pending; this Worker does not mark the Roadmap stage complete.

## 11. Known risks and limits

- Proposal and Request stores, their locks, and exactly-once guarantee are process-local. A restart, separate Flask worker, or scale-out deployment has no shared ledger/CAS transaction.
- Durable multi-worker semantics require an explicitly approved storage and transaction design; no migration was inferred or implemented.
- Legacy client-held State endpoints remain for compatibility and are not lifecycle authority. This stage does not convert them or claim their calls have server-ledger replay protection.
- Actor authorization, durable audit, idempotency keys across processes, and UI policy are deferred.

## 12. Downstream lifecycle contract

- H5-ORCH-012 Workflow State Machine may model an approval event only by retaining the server `proposal_id` and consuming this terminal snapshot; it must not reconstruct client Proposal/operations or bypass the lifecycle service.
- H5-ORCH-016 Orchestrator Service may create/read a pending Proposal and invoke this internal lifecycle boundary; it must present terminal result data rather than mutate Request State directly.
- H5-ORCH-019 Proposal UI may render a pending server Proposal and submit explicit approve/reject intent. It must not optimistically alter form State, send client operations/base version as authority, or retry an already-terminal Proposal as a new apply.
- Downstream focused tests should retain the invariant: the same `proposal_id` never causes a second Request apply, while stale/rejected/expired/failed records do not change Request State/version.

## Worker report

The H5-ORCH-009 internal lifecycle is implemented additively and remains awaiting Reviewer review. Roadmap status, baseline cards, and next-stage prompts were not changed. No commit was made.
