# Stage information

- Stage ID: `H5-ORCH-006`
- Stage name: Common Field Registry
- Project root: `request_ai_agent_h5_v0`
- Baseline: `69f9374` and H5-ORCH-005 contract
- Roadmap version: `0.7`
- Work status: implementation complete; awaiting Reviewer review

# Goal

Expose existing canonical field bindings through a read-only Registry so later Planner and Proposal work can ask for the same field meaning. The Registry does not interpret natural language, infer values, mutate Request State, calculate active/required rules, or replace validation.

# Input documents

- `AGENTS.md`
- Roadmap and common/manual execution contracts
- H5-ORCH-001 through H5-ORCH-005 handoff documents

# Actual work and changed files

- Added `request_ai_agent_h5_v0/field_registry.py`.
  - `FieldRegistryDTO` exposes stable ID, canonical/value path, label/type/unit, active/required/dependency metadata, validation binding, priority, operation reference, and condition card/key binding.
  - General fields adapt existing `FieldSpec` instances.
  - Conditional fields adapt the live result of `get_active_condition_fields(state)`; no Fieldset or Case Matrix rule is copied.
  - `GeometryProductsAdapterDTO` explicitly identifies `geometry.products` as a transport-only LLM DTO with no Request State path and the canonical base/comparison targets.
- Added focused mock-only tests in `tests/test_orchestrator_field_registry.py`.
- No existing API, renderer, Fieldset, normalizer, Validator, Case Matrix, Preview, Word, Roadmap, or future-stage prompt was changed.

# Data structures and API

There is no public HTTP API change.

`get_field_registry(state)` returns immutable Registry DTO snapshots. General field IDs use their static path, such as `analysis_overview.request_description`. Condition IDs use the existing active instance key, such as `conditions.space_environment_1.room_temp`; this deliberately separates a field definition from its live card instance.

For condition cards, canonical values remain in `conditions.condition_sets`. The derived `conditions.fields.*.values` path is retained only as the existing validation/proposal operation reference. The Registry reports both rather than pretending the derived list is the canonical storage location.

`get_geometry_products_adapter()` returns the adapter contract:

- transport path: `geometry.products`
- Request State path: `None`
- canonical targets: `geometry.base_product.drawing_no`, `geometry.comparison_products[].drawing_no`

# Authority and important decisions

The retained baseline is:

`LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply`

Registry reads are side-effect free. Any consumer write remains an already-approved operation that must pass existing `sanitize_state()` and `state_with_validation()`; `chat_patch.apply_patch_operations()` is the current boundary. Existing Fieldset code determines active/required state, normalizer determines cleanup/recomputation, Validator determines blocking results, and Case Matrix/Preview/Word retain their current authority.

The public `FieldSpec` catalogue and active card Fieldset were not treated as one source: general metadata comes from `FieldSpec`; conditional activation, requirement, instance binding, and priorities come from the actual live Fieldset result.

# Reused existing behavior

- `schema.py`: static `FieldSpec` metadata.
- `condition_fieldsets.py:get_active_condition_fields`: live conditional fields.
- `state.py:sanitize_state`: canonicalization and inactive-field/Matrix cleanup authority.
- `validator.py:state_with_validation` and `validate_state`: final validation authority.
- `chat_patch.py`: existing approved-operation and geometry adapter boundary.

# Not performed

No natural-language/regex extractor, intent router, LLM/RAG/external DB call, Proposal/version/ledger/Conversation/Workflow/Planner/UI implementation, migration, or renderer refactor was added. Inactive conditional-value retention and Matrix cleanup policy were not decided; they remain normalizer behavior and H5-ORCH-021 work.

# Focused verification

- General field Registry binding matches `FieldSpec` and required-field validator binding.
- Active conditional representative (`room_temp`) matches the live Fieldset instance, canonical condition-card path, and derived validation operation path.
- A mocked existing `conditional_required` Fieldset result matches the Validator's conditional-group blocking result.
- Registry lookup does not mutate Request State; a Registry-referenced write goes through `apply_patch_operations()` and receives normalizer/validator output.
- `geometry.products` is verified as adapter-only, not stored Request State.

# Known risks and limits

- R-004 remains: inactive conditional values and Case Matrix cleanup can be removed by the existing normalizer. The Registry reports no retention policy; H5-ORCH-021 owns the later user-facing impact treatment.
- R-008 is partially mitigated only by the existing geometry adapter. Client-supplied state/Proposal, stale/replay, latest-read, version/CAS, ledger, and exactly-once approval remain for H5-ORCH-007 through H5-ORCH-009.

# Contracts supplied to later stages

- H5-ORCH-007 to 009: Registry DTOs are read-only metadata, not version, Proposal, ledger, or apply authority. Approved writes still need sanitize/validate and the forthcoming latest-read/CAS lifecycle.
- H5-ORCH-013: use `field_id`, `active`, `required_level`, `dependencies`, and `priority` from a fresh Registry snapshot for deterministic next-field selection; do not recreate Fieldset logic.
- H5-ORCH-014 to 016: use `operation_path`/`field_key` only after LLM structured output passes the existing sanitizer; use the geometry Adapter DTO for `geometry.products`; do not turn DTO metadata into natural-language inference or direct State mutation.
- Tests establish the Registry/Fieldset/Validator agreement and the normalizer/validator final-decision boundary. Future consumers should preserve these focused contracts.

# Validation not run

Real LLM, RAG, external DB, full E2E, and broad test suites were intentionally not run.

# Failed or unavailable validation

The default `python` interpreter did not include `pytest`; the repository virtual-environment interpreter ran the focused tests instead. No required focused validation failed. Full E2E and live LLM/RAG/DB verification remain intentionally out of scope rather than failed checks.

# Expected files for later stages

- H5-ORCH-007 to 013: bounded version, Proposal, workflow, and Planner service/model/store modules plus focused `tests/test_orchestrator_*.py` coverage. Do not retrofit Registry data into Request State.
- H5-ORCH-014 to 016: `llm_client.py`, `chat_patch.py`, and an additive orchestration service boundary; retain the existing sanitizer and geometry adapter.
- H5-ORCH-018 to 020: `ui.py` additive chat/proposal/sync surfaces only after the approval lifecycle exists; do not change this Registry to support optimistic UI state.

# Follow-up improvement proposal

H5-ORCH-021 should make inactive conditional-value and Case Matrix cleanup effects visible to users without changing the Registry's read-only policy. H5-ORCH-031 should include Registry/normalizer agreement in the broader regression suite once later lifecycle work exists.

# Git state and commit

At Worker start, the working tree already contained Roadmap/prompt/automation/run-document changes and Python cache directories. This stage added only `field_registry.py`, its focused test, and this handoff document; it did not modify the pre-existing Roadmap or prompt changes. No commit was created: the stage remains awaiting Reviewer review.

# Roadmap change required

No. The Worker leaves H5-ORCH-006 awaiting Reviewer review and does not update Roadmap status, baseline cards, or next-stage prompts.
