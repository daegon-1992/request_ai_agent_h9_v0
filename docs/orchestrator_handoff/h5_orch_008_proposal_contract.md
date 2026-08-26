# 단계 정보

- 단계 ID: `H5-ORCH-008`
- 단계명: Proposal 계약·저장 구조
- 수행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: `69f9374`, `c1ab16f`
- Roadmap 버전: `0.9` (2026-07-31)
- 작업 상태: 완료 후보 — Reviewer 검토 대기

# 이번 단계 목표

H5-ORCH-007의 서버 발급 `request_id`와 latest-read `request_version` 위에서, 승인 전 후보 변경을 server-side runtime Proposal DTO/ledger에 보관한다. 생성은 Request State와 version을 변경하지 않으며, 승인·거절·만료·apply 및 exactly-once lifecycle은 H5-ORCH-009에 남긴다.

# 사전 입력 문서

- `AGENTS.md`
- `docs/orchestrator_handoff/orchestrator_roadmap.md` (v0.9)
- `docs/orchestrator_handoff/prompts/common_stage_contract.md`
- `docs/orchestrator_handoff/prompts/baseline_prompts.md`
- `docs/orchestrator_handoff/prompts/manual_stage_execution.md`
- `docs/orchestrator_handoff/h5_orch_001_repo_map.md`부터 `h5_orch_007_request_version.md`까지의 선행 인수인계 문서

# 실제 수행 내용

- `ProposalService`가 `RequestStateStore.read(request_id)`로 서버 latest snapshot을 먼저 읽고, 그 서버 version만 `base_version`으로 기록한다.
- 선택적인 client-supplied base version은 authority가 아니라 stale precondition이다. latest version과 다르면 `RequestVersionConflictError`로 거절하며 Proposal ledger를 기록하지 않는다.
- `proposal_from_operations()`과 기존 sanitizer를 사용해 operation을 정규화하고, `apply_patch_operations()`으로 latest State의 copy-only dry-run을 수행한다. 이 경로가 기존 geometry Adapter, `sanitize_state()`, `state_with_validation()`, active conditional cleanup을 그대로 사용한다.
- `ProposalStore`는 process-local memory의 최대 256개 bounded ledger다. 기록/조회는 `ProposalService` 내부 경로로만 사용하며, 외부에는 service의 server-issued Proposal 생성·조회와 count만 노출한다. status 전이 또는 apply surface는 제공하지 않는다.

# 변경 파일

- `request_ai_agent_h5_v0/proposal_store.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py`
- `docs/orchestrator_handoff/h5_orch_008_proposal_contract.md`

# 신규 또는 변경된 데이터 구조

| 구조 | 내용과 권위 |
|---|---|
| `ProposalSnapshot` | `proposal_id`, `request_id`, server-read `base_version`, sanitized normalized `operations`, bounded `diff_summary`, `source`, `status`, validation/result metadata, `created_at`을 가진 frozen DTO다. |
| `ProposalStore` | server-issued Proposal만 service 내부 기록 경로로 저장하는 bounded runtime ledger다. caller가 보낸 Proposal DTO를 기록하거나 신뢰하지 않는다. |
| `ProposalService` | Request latest-read와 sanitize/Adapter/dry-run을 연결하는 additive internal surface다. Request write/CAS를 호출하지 않는다. |

`status`는 생성 시 `pending`만 기록한다. `result`는 `state_changed: false`, `read_only: true`, dry-run diff 여부를 기록한다. `validation`은 dry-run의 기존 `review` 결과이며 별도 Validator/Case Matrix를 복제하지 않는다.

# 신규 또는 변경된 API

새 public HTTP API는 추가하지 않았다. 다음 internal service만 additive하게 제공한다.

| Surface | 계약 |
|---|---|
| `ProposalService.create_proposal(request_id, operations, source, message, client_base_version)` | 서버 Request latest read에서 `request_id`/`base_version`을 얻어 Proposal을 기록한다. invalid/unsupported operation, 잘못된 type, unknown request, stale client version은 Request와 ledger 모두 불변으로 거절한다. |
| `ProposalService.read_proposal(proposal_id)` | server ledger의 deep-copy snapshot을 조회한다. |

기존 public API, client-held legacy flow와 UI는 변경하지 않았다.

# 중요 설계 결정

1. Proposal authority는 server ledger에만 있다. client-held legacy State, forged Proposal DTO, client base version은 저장 권위가 아니다.
2. Request/base-version authority는 `RequestStateStore.read()`의 latest snapshot이다. caller 제공 State는 Proposal base 계산이나 dry-run base로 사용하지 않는다.
3. `geometry.products`는 LLM-facing Adapter DTO로만 sanitizer에 입력되며, dry-run 결과는 canonical base/comparison product cards다. Request State에 legacy products field를 저장하지 않는다.
4. diff는 existing canonical State와 existing copy-only dry-run 결과의 bounded structural summary다. 별도 geometry State나 Fieldset/normalizer/Validator/Case Matrix 규칙을 만들지 않는다.
5. Runtime-only 한계 때문에 DB migration, external store, durable multi-worker semantics는 구현하지 않았다.

# 기존 기능 재사용 지점

- `request_state_store.py:RequestStateStore.read()` — request identity, latest State, version authority.
- `chat_patch.py:sanitize_external_operations()` 및 `proposal_from_operations()` — allowlist sanitizer와 normalized operation/geometry Adapter metadata.
- `chat_patch.py:apply_patch_operations()` — State copy 적용, geometry Adapter, `sanitize_state()`, `state_with_validation()` finalization.
- `state.py:sanitize_state()` 및 `validator.py:state_with_validation()` — normalizer, conditional cleanup, Validator/Case Matrix final authority.
- `field_registry.py` — 수정하지 않았으며 read-only metadata다.

# 수행하지 않은 작업

- Request mutation, Proposal approve/reject/expire/apply API, terminal status 전이, replay/exactly-once 처리를 구현하지 않았다.
- Conversation/Workflow/Planner/UI, DB migration, durable/외부 저장소, 실제 LLM/RAG/외부 DB 호출을 추가하지 않았다.
- Fieldset/normalizer/Validator/Case Matrix/Preview/Word 규칙 또는 renderer를 복제·변경하지 않았다.
- Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 수정하지 않았다.

# 최소 검증

실행 명령:

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py request_ai_agent_h5_v0/tests/test_orchestrator_request_version.py request_ai_agent_h5_v0/tests/test_orchestrator_field_registry.py
python tools/check_encoding.py --changed
git diff --check
```

focused pytest 결과: `14 passed`.

검증한 계약:

- 유효 Proposal은 server-side 조회 가능하고, 생성 전후 Request State/version이 동일하다.
- malformed type, invalid/unsupported operation, unknown request, stale client base version은 Request와 Proposal ledger를 변경하지 않는다.
- bounded ledger 저장 실패는 Request State/version과 기존 stored Proposal을 변경하지 않는다.
- normalized geometry dry-run은 Adapter를 거쳐 canonical product cards를 만들고, `sanitize_state()`/`state_with_validation()` review 결과와 active conditional cleanup을 우회하지 않는다.

# 실패하거나 실행하지 못한 검증

- 실제 LLM/RAG/외부 DB, 전체 E2E, 전체 suite, multi-process/multi-worker durability test는 범위 밖이라 실행하지 않았다.
- 이 단계의 focused pytest는 모두 통과했다. encoding/diff 결과는 아래 최종 검증에 기록한다.

# 알려진 문제와 제한사항

- Proposal ledger는 process-local memory다. restart, 다중 Flask worker, scale-out에서는 Proposal과 Request latest-read/CAS 보장이 공유·영속되지 않는다. durable 저장소가 필요해지면 별도 storage/transaction/migration 결정을 받아야 한다.
- legacy client-held flow는 유지된다. 해당 경로의 client State와 Proposal은 이 ledger의 권위를 자동으로 얻지 않는다.
- 현재 Proposal은 pending candidate일 뿐이다. stale/replay/forged Proposal은 생성 때 server id/base를 고정하지만, approval 시 one-time CAS/revalidation은 아직 없다.

# 발견된 위험

| 위험 | 현 상태 | H5-ORCH-009 대응 |
|---|---|---|
| stale Proposal | 생성 시 client stale base를 거절하지만 이후 Request 변경을 적용할 lifecycle은 없다. | approval 직전 latest-read/CAS를 수행한다. |
| replay/duplicate approval | terminal status와 exactly-once 기록이 없다. | ledger status 전이와 one-time apply를 원자적으로 설계한다. |
| forged client Proposal | client DTO는 ledger 기록으로 신뢰되지 않는다. | server-issued `proposal_id`를 다시 조회해 operations/base를 사용한다. |
| runtime-only durability | restart/multi-worker 안전성이 없다. | 배포 요구가 확정되기 전 durable migration을 자동 도입하지 않는다. |

# 다음 단계에서 반드시 참고할 내용

- H5-ORCH-009은 `ProposalService.read_proposal()`의 server record만 사용하고, client-supplied Proposal/operations/base version으로 apply하지 않아야 한다.
- approval 시 `RequestStateStore.compare_and_swap(request_id, proposal.base_version, mutation)` 안에서 latest State를 다시 읽고, server-recorded normalized operations를 `apply_patch_operations()`에 다시 통과시켜야 한다.
- CAS conflict, validation failure, duplicate/replay는 Request State/version과 ledger terminal status를 모두 안전하게 유지·전이해야 한다. exactly-once 성공 여부는 Proposal ledger에 남겨야 한다.
- Registry는 계속 read-only이며 `geometry.products`는 Adapter input DTO다.

# 다음 단계 수정이 예상되는 파일

- `request_ai_agent_h5_v0/proposal_store.py` — H5-ORCH-009의 lifecycle-only status/one-time apply 경계 후보
- `request_ai_agent_h5_v0/request_state_store.py` — existing CAS 재사용 후보
- `request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py` — approval conflict/replay/exactly-once focused test 위치

# 후속 개선 후보

- 배포 topology와 durability 요구가 결정된 뒤에만 durable Proposal/Request storage와 transaction 모델을 별도 승인 단계로 제안한다.
- request ownership/authorization, audit event, idempotency key는 lifecycle/audit 단계에서 추가 검토한다.

# Roadmap 변경 필요 여부

없음. Worker는 H5-ORCH-008을 완료로 확정하지 않으며 Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 변경하지 않는다. Reviewer 검토 대기로 남긴다.

# Git 상태와 Commit 여부

- 시작 전 존재하던 Roadmap/prompt/automation/run 문서 및 Registry 관련 변경은 보존했다.
- 이번 단계의 의도된 변경은 Proposal runtime store/service, focused test, 이 handoff 문서다.
- Commit 여부: Worker는 커밋하지 않는다.

# Worker 보고서

H5-ORCH-008은 server latest-read를 base authority로 사용하는 bounded Proposal DTO/ledger를 추가했다. 생성은 기존 sanitizer → geometry Adapter → copy-only dry-run → canonical sanitize/validation 경로를 재사용하며 Request State/version을 변경하지 않는다. client-held State, stale base, forged Proposal은 ledger authority가 아니고, runtime-only durability와 approval/replay/exactly-once lifecycle은 H5-ORCH-009의 명시적 후속 작업이다. Reviewer 검토 전 완료 상태를 확정하지 않는다.
