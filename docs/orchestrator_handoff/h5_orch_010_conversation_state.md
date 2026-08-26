# H5-ORCH-010 Conversation State model

## Stage information

- Stage ID: `H5-ORCH-010`
- Stage name: Conversation State model
- Baselines: `69f9374`, `c1ab16f`, H5-ORCH-008 Proposal ledger, and H5-ORCH-009 terminal lifecycle
- Roadmap state: awaiting Reviewer review; this Worker did not change the Roadmap, baseline cards, or subsequent prompts.
- Scope: an additive, bounded, process-local internal DTO/store only.

## Current situation and objective

`RequestStateStore` owns the latest canonical Request snapshot and its version. `ProposalService` owns the server-issued Proposal ledger and the terminal approve/reject/expire/apply lifecycle. This stage adds the smallest independent Conversation record required to retain workflow-facing progress without copying either authority.

The objective is a server-issued conversation/session identifier linked only by `request_id`, with bounded question history, pause/resume/close lifecycle, workflow-facing status, a pending `proposal_id` reference, summary, and local version. It is not a public session API or a workflow state machine.

## Work performed and changed files

- Added `request_ai_agent_h5_v0/conversation_store.py`.
  - `ConversationSnapshot` is a frozen DTO with `conversation_id`, `request_id`, `workflow_status`, `pending_proposal_id`, `question_history`, `paused`, `summary`, `version`, and lifecycle `status`.
  - `ConversationStore` creates server-issued `conversation_*` identifiers, returns deep-copy snapshots, bounds record/history/text size, and protects lifecycle transitions with an `RLock`.
  - Active-only workflow/question/summary/pending-reference updates, pause/resume, and terminal close are supported. Closed or paused records reject inappropriate mutations.
- Added `request_ai_agent_h5_v0/tests/test_orchestrator_conversation_store.py`.
- Added this handoff document.

No existing endpoint, Request store, Proposal lifecycle, UI, renderer, or rules engine was changed.

## Data and authority contract

| Concern | Conversation contract | Authoritative boundary |
|---|---|---|
| Request | Stores only the opaque server `request_id` string. No State, snapshot, client State, or Request version exists in a Conversation record. | `RequestStateStore.read(request_id)` and its CAS lifecycle |
| Proposal | Stores only an optional opaque server `proposal_id` string. No operations, base version, diff, validation, or terminal result is copied. | `ProposalService.read_proposal(proposal_id)` and H5-ORCH-009 lifecycle |
| Workflow progress | Local `workflow_status`, questions, pause flag, summary, local version, and lifecycle status are bounded process-local metadata. | `ConversationStore` only |
| Request mutation | Not available from Conversation State. | H5-ORCH-009 Proposal lifecycle / later application service |

The local `version` is strictly a Conversation record revision for later session/workflow consumers. It is not a Request version, Proposal base version, CAS token, or client authority.

The pending Proposal reference is deliberately retained even after a Proposal becomes terminal. Later consumers must re-read the server ledger to inspect terminal status; the Conversation store never decides, applies, rejects, expires, or clears it based on copied Proposal data.

## Lifecycle and bounds

- Creation starts `active`, unpaused, at local version `0`, with an empty history and no pending Proposal reference.
- Active records may update workflow status, append a bounded rolling question history, set/clear a Proposal ID reference, and update a bounded summary.
- `pause()` transitions `active -> paused`; `resume()` transitions `paused -> active`.
- `close()` transitions either non-terminal state to `closed`; close and all other mutations are rejected after terminal closure.
- The store has bounded conversation capacity and bounded question history. A capacity failure occurs before any new record is stored. No eviction, persistence, or cross-worker sharing is inferred.

This is only a safe local lifecycle envelope, not H5-ORCH-012's Workflow State Machine. `workflow_status` remains an opaque bounded workflow-facing label and does not encode event rules here.

## Reused behavior and explicit exclusions

The implementation intentionally has no dependency on `state.py`, `validator.py`, Field Registry, Request State contents, or Proposal operation data. It does not duplicate Fieldset/normalizer/Validator/Case Matrix/Preview/Word behavior, geometry adapter behavior, LLM/RAG behavior, regex/alias extraction, or intent routing.

It also adds no HTTP/session API, message handler, planner, orchestrator service, workflow machine, UI, database migration, external storage, or durable transaction. Existing legacy endpoints and client-held State behavior are untouched.

## Focused validation

Executed only the focused Conversation tests:

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_conversation_store.py
```

The tests cover:

- create/read deep-copy isolation and proof that a Conversation neither copies nor changes Request State;
- isolation between different conversation/request references and bounded store failure without changing existing records;
- bounded question history, pause/resume, invalid transition and terminal mutation rejection, while an attached Request snapshot/version remains unchanged;
- approved, rejected, and expired H5-ORCH-009 terminal Proposals: Request apply happens only through `ProposalService`, while Conversation retains only the server `proposal_id` reference and non-applying terminals leave Request unchanged.

Required repository checks are recorded with the Worker report after final edits:

```powershell
python tools/check_encoding.py --changed
git diff --check
```

Full E2E, real LLM/RAG/external DB, and multi-worker deployment tests were not run because they are outside this stage.

## Known risks and residual limits

- Conversation, Request, and Proposal stores are all process-local. Restart, separate worker, and scale-out execution lose or split Conversation records and cannot provide shared transaction semantics.
- A durable DB, multi-worker transaction, migration, ownership/authorization, or cross-process idempotency model requires an explicit future decision. None was inferred or implemented.
- Conversation does not prove that its referenced Request or Proposal currently exists. Later services must re-read the respective server authority and handle missing/terminal records safely.
- Keeping a terminal `proposal_id` reference is intentional observability for later workflow/API consumers; it is not permission to replay a lifecycle action.

## Contracts supplied to later stages

| Stage | Supplied model/test contract |
|---|---|
| H5-ORCH-011 | Expose this server-issued `conversation_id` through an API without importing client State or adding message/LLM behavior. Preserve deep-copy reads, bounded capacity, terminal mutation rejection, and request-reference isolation. |
| H5-ORCH-012 | Interpret `workflow_status` through a deterministic event machine, and use pause/resume/closed lifecycle safely. Approval waits retain only `proposal_id`; terminal Proposal data must be read from the server ledger. |
| H5-ORCH-016 | Compose fresh `RequestStateStore.read(request_id)` and lifecycle service reads with this Conversation record. It must not mutate Request State through Conversation or reconstruct Proposal operations/base versions. |
| H5-ORCH-018 to 020 | Render session/proposal references without optimistic form State. UI/API must use server Request refresh and server Proposal terminal reads; Conversation's local metadata cannot replace either authority. |

## Roadmap and Git status

The Worker leaves the roadmap status, baseline cards, and next-stage prompts unchanged and awaits Reviewer inspection. No commit was created. Pre-existing unrelated working-tree changes were preserved.

## Worker report

Implemented a minimal bounded process-local Conversation State store. It is strictly separate from Request State, references server `request_id` and optional `proposal_id` only, returns deep copies, and safely handles pause/resume/close transitions. Request latest state/version and Proposal terminal lifecycle remain server-authoritative through their existing stores. Runtime-only durability and multi-worker limitations remain documented for Reviewer review.
