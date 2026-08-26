# H5-ORCH-024 Undo

## Status and scope

Worker implementation complete; awaiting Reviewer review.  This stage leaves the
Roadmap and later prompts unchanged.  The retained boundary is:

`server-issued approved Proposal -> server-authoritative inverse evidence -> inverse Proposal/dry-run -> explicit approved apply -> H5-020 latest GET sync`

## Inverse-evidence authority

`ProposalService` now records `canonical_set_inverse_v1` evidence at the
original server dry-run only when every normalized operation is a canonical
allowed `set`, each prior canonical value is non-empty, and the dry-run proves
the corresponding current canonical value.  The evidence contains only the
specific inverse operation values and expected current values; it is not a
Request snapshot and is never supplied by the client.

List, geometry-adapter, conditional, empty-prior-value, ambiguous, and other
operations receive no inverse evidence.  Undo does not infer their values,
targets, or units and does not restore a snapshot.

## Undo Proposal/no-Proposal boundary

`POST /api/orchestrator/proposals/undo` accepts exactly the selected server
`proposal_id`.  It can neither accept nor replace operations, inverse values,
Request state/version, snapshots, or Proposal records.

For a server-approved non-inverse original with evidence, `ProposalService`
requires that the latest Request version equal the original approval result
version and that its canonical values still match the recorded evidence.  It
then creates a distinct pending `source="server_inverse"` Proposal with the
latest base version, display-only diff, and server ledger `undo_of` reference.
The original and inverse remain separate ledger records.

The inverse dry-run and ledger record run through the Request store's additive
`at_version()` fence.  A Request write that is already current causes
`undo_stale`; a write that arrives while the inverse record is being made waits
until that record is tied to the checked version.  It therefore cannot create
an inverse ledger entry from an obsolete read-before-record gap.

Unknown, non-approved/inverse-terminal, missing evidence, stale/latest-version
mismatch, canonical conflict, duplicate pending Undo, already-resolved inverse,
and creation/request failures return stable read-only codes and create no
Proposal or Request mutation.  An inverse Proposal remains subject to the
unchanged lifecycle: validation/apply failure or CAS conflict produces its
ordinary terminal record and no Request mutation.  A resolved inverse blocks a
second Undo for the same original.

## UI and synchronization boundary

The existing panel shows a `되돌리기 제안` control only after an approved
Proposal.  Its request contains only `{proposal_id}`.  Successful inverse
creation renders a new pending display-only Proposal card; it does not patch,
rollback, sync the form, dispatch workflow, send a message, or calculate
impact.  The inverse card uses the existing H5-019 approval decision endpoint.
Only a subsequently approved inverse goes through the unchanged H5-020
approved-only exact-once latest GET sync.  Pending, rejected, conflicted,
failed, replay, Undo creation, and GET failure do not sync.

H5-021 remains the owner of canonical conditional-impact display.  H5-025 and
later Case Matrix, validation, preview, Word, RAG, audit, and durability work
remain out of scope.

## Changed files

- `request_ai_agent_h5_v0/proposal_store.py`
- `request_ai_agent_h5_v0/request_state_store.py`
- `request_ai_agent_h5_v0/app.py`
- `request_ai_agent_h5_v0/ui.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_undo.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py`
- this handoff

## Runtime-only durability limit

Request State, Proposal ledger, inverse evidence, duplicate protection, CAS,
and the panel refresh guard are process-local runtime state.  Restart and
multi-worker deployments have no shared ledger, transaction, durable inverse
evidence, or cross-process exactly-once guarantee.  No DB rollback, migration,
or durable storage was introduced.

## Focused verification

Executed:

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_undo.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_service.py request_ai_agent_h5_v0/tests/test_orchestrator_correction.py
python tools/check_encoding.py --changed
git diff --check
```

Result: `57 passed in 1.87s`; encoding and whitespace checks passed.  The added
version-fence test queues a Request write at inverse ledger-record time and
proves it cannot enter before that record.  Roadmap
status remains Reviewer pending regardless of those results.
