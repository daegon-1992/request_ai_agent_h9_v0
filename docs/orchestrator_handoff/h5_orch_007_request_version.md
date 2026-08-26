# 단계 정보

- 단계 ID: `H5-ORCH-007`
- 단계명: Request State version
- 수행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: `69f9374` (`feat: adapt LLM geometry proposals safely`)
- Roadmap 버전: `0.8` (2026-07-31)
- 작업 상태: 완료 후보 — Reviewer 검토 대기

# 이번 단계 목표

서버가 식별한 Request의 최신 canonical State를 읽고, `expected_version`을 확인한 뒤 한 번만 원자 갱신할 수 있는 additive request identity/version/CAS 경계를 제공한다. 성공한 mutation만 version을 1 증가시키며, stale expected version 또는 mutation/normalization 실패는 State와 version 모두 바꾸지 않는다.

# 사전 입력 문서

- `AGENTS.md`
- `docs/orchestrator_handoff/orchestrator_roadmap.md` (v0.8)
- `docs/orchestrator_handoff/prompts/common_stage_contract.md`
- `docs/orchestrator_handoff/prompts/baseline_prompts.md`
- `docs/orchestrator_handoff/prompts/manual_stage_execution.md`
- `docs/orchestrator_handoff/h5_orch_001_repo_map.md`
- `docs/orchestrator_handoff/h5_orch_002_state_proposal_survey.md`
- `docs/orchestrator_handoff/h5_orch_003_rules_engines_survey.md`
- `docs/orchestrator_handoff/h5_orch_004_agent_ui_survey.md`
- `docs/orchestrator_handoff/h5_orch_005_target_architecture.md`
- `docs/orchestrator_handoff/h5_orch_006_field_registry.md`

# 실제 수행 내용

- `RequestStateStore`를 새 bounded runtime store로 추가했다. UUID `request_id`, 0부터 시작하는 단조 `version`, deep-copy 최신 조회, lock으로 보호한 compare-and-swap을 제공한다.
- store의 create/replace/CAS는 항상 기존 `_derive_state()`를 통해 `state_with_validation()`을 호출한다. 이는 기존 `sanitize_state()` 및 Validator/Case Matrix/active conditional cleanup의 최종 권위를 그대로 사용한다.
- `compare_and_swap()`은 lock 안에서 latest record를 읽고 expected version을 비교한다. mutation 결과의 canonical finalization까지 성공한 뒤에만 record를 교체하고 version을 증가시킨다.
- 기존 client-held endpoint와 payload shape는 변경하지 않았다. 새 버전 경계만 아래 additive API로 노출했다.
- 이 store는 DB/외부 저장소가 아닌 process-local memory다. migration이나 외부 저장소가 필요한 변경은 수행하지 않았다.

# 변경 파일

- `request_ai_agent_h5_v0/request_state_store.py`
- `request_ai_agent_h5_v0/app.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_request_version.py`
- `docs/orchestrator_handoff/h5_orch_007_request_version.md`

# 신규 또는 변경된 데이터 구조

| 구조 | 내용과 권위 |
|---|---|
| `RequestStateSnapshot` | `{request_id, version, state}` immutable DTO snapshot이다. `state`는 호출자에게 deep copy로만 노출된다. |
| `RequestStateStore` | runtime 내 공식 latest-read/CAS boundary다. `state`가 아닌 record의 `version`이 concurrency token이다. |
| `RequestVersionConflictError` | stale compare 결과이며 request id, expected/current version을 전달한다. |

`request_version`은 canonical State의 metadata에 저장하지 않는다. 그러므로 Field Registry는 계속 read-only metadata이고, `geometry.products`가 State에 저장되는 경로도 생기지 않는다.

# 신규 또는 변경된 API

모두 additive API이며 기존 `/api/request/new`, `/api/input/save`, `/api/chat/*`와 그 요청/응답 shape를 바꾸지 않는다.

| API | 요청 | 성공 응답 | 실패 계약 |
|---|---|---|---|
| `POST /api/request/versioned` | 선택적 `{state}`. 없으면 새 initial State, 있으면 legacy client-held State를 import한다. | `201`, `{request_id, request_version: 0, state, state_changed: true, ...}` | State가 mapping이 아니면 새 initial State로 제한한다. |
| `GET /api/request/versioned/<request_id>` | 없음 | `{request_id, request_version, state, ...}` latest snapshot | unknown id는 `404 request_not_found` |
| `PUT /api/request/versioned/<request_id>` | `{expected_version: int, state: mapping}` | 새 canonical state와 증가한 `request_version`, `state_changed: true` | stale은 `409 request_version_conflict` 및 `expected_version`/`current_version`, invalid precondition은 `400`, unknown id는 `404`; 모두 `state_changed: false` |

클라이언트가 보내는 `expected_version`은 신뢰하는 version 값이 아니다. server latest record의 version과 정확히 같을 때의 precondition일 뿐이며, server가 version을 생성·증가·반환한다.

# 중요 설계 결정

1. **권위 위치:** request identity, latest-read, CAS와 version 증가는 server runtime store만 권위를 가진다. client-held State 또는 client-supplied version은 authority가 아니다.
2. **원자성 범위:** 단일 Python process의 `RLock` 범위에서 latest-read → expected-version check → mutation → canonical finalization → record write가 원자적이다. process restart와 multi-worker deployment 사이에는 원자성이 없다.
3. **기존 엔진 재사용:** Store는 Fieldset/normalizer/Validator/Case Matrix 규칙을 복제하지 않고 `_derive_state()`를 호출한다. geometry write가 필요한 consumer는 기존 `apply_patch_operations()` 및 geometry Adapter 결과를 CAS mutation에 넘겨야 한다.
4. **호환 전략:** legacy client-held API를 versioned API로 암묵 전환하지 않았다. 기존 브라우저와 endpoint는 계속 동작하며, 기존 State는 명시적으로 versioned create에 import할 수 있다.
5. **승인 경계 보존:** Proposal, ledger, approve/reject API, Conversation/Workflow/Planner/UI를 추가하지 않았다. 이번 PUT은 versioned Request State replacement boundary일 뿐 Proposal 승인 생명주기가 아니다.

기준선은 계속 `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply`이다. LLM/RAG 호출, regex/alias extractor, keyword/regex intent router는 추가하지 않았다.

# 기존 기능 재사용 지점

- `state.py:sanitize_state()` — canonical State 생성과 conditional/Case Matrix cleanup 권위.
- `validator.py:state_with_validation()` — validator, issue registry, submission view 최종 권위.
- `chat_patch.py:apply_patch_operations()` — 허용 operation, legacy `geometry.products` Adapter, canonical geometry write의 기존 승인-apply helper. Store는 이를 대체하거나 복제하지 않는다.
- `field_registry.py` — 변경하지 않았다. Registry는 version/apply 권위가 아닌 read-only metadata로 유지된다.

# 수행하지 않은 작업

- Proposal/ledger/승인 API, exactly-once apply, Conversation, Workflow, Planner, UI를 구현하지 않았다.
- DB migration, 파일 저장, 외부 DB, 실제 LLM/RAG 호출을 하지 않았다.
- 기존 legacy endpoint를 server state로 이전하거나 Request State 직접 mutation 경로를 제거/재설계하지 않았다.
- Fieldset/normalizer/Validator/Case Matrix/Preview/Word 규칙 복제 또는 renderer 변경을 하지 않았다.
- Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 수정하지 않았다.

# 최소 검증

실행 명령:

```powershell
..\.venv\Scripts\python.exe -m pytest .\request_ai_agent_h5_v0\tests\test_orchestrator_request_version.py .\request_ai_agent_h5_v0\tests\test_orchestrator_field_registry.py
python tools/check_encoding.py --changed
git diff --check
```

focused pytest 결과: `7 passed`.

- `python tools/check_encoding.py --changed`: 통과 (`Encoding check passed`)
- `git diff --check`: 통과

검증한 계약:

- 새 Request와 legacy client State import 모두 version 0으로 초기화되고 latest read가 copy를 반환한다.
- 정상 expected-version write만 version을 1 증가시킨다.
- stale expected version은 conflict이며 State/version을 변경하지 않는다.
- mutation exception은 State/version을 변경하지 않는다.
- versioned write가 `apply_patch_operations()` 결과와 `state_with_validation()` 최종 결과를 보존한다. legacy `geometry.products`는 canonical base/comparison product로 Adapter 변환되고 State에는 남지 않는다.
- inactive `room_temp` 입력은 기존 active conditional cleanup에 의해 유지/복제되지 않으며 Validator submission 결과가 그대로 유지된다.
- Registry focused tests도 함께 실행하여 Registry가 read-only이고 normalizer/validator boundary를 우회하지 않음을 재확인했다.

# 실패하거나 실행하지 못한 검증

- 실제 LLM/RAG/외부 DB, 전체 E2E, multi-process deployment 테스트는 범위 밖이므로 실행하지 않았다.
- 없음. 필수 focused test, encoding, diff 검사가 모두 통과했다.

# 알려진 문제와 제한사항

- Store는 process-local memory다. restart, multiple Flask worker, scale-out 환경에서는 request identity/state/version이 공유·영속되지 않는다. durable server latest-read/CAS가 필요해지는 배포 전에는 storage adapter와 transaction semantics의 별도 설계가 필요하다.
- legacy endpoint는 여전히 client-held State를 받는다. 따라서 versioned API를 사용하지 않는 기존 경로는 server latest-read/CAS 보호를 얻지 못한다. 이 호환성 상태를 이번 단계에서 server-authoritative migration 완료로 해석하면 안 된다.
- `PUT`은 versioned State replacement만 제공하며 Proposal 검증, actor authorization, idempotency key, ledger terminal status를 제공하지 않는다.

# 발견된 위험

| 위험 | 현 상태 | 후속 최소 대응 |
|---|---|---|
| client-held state | 기존 API는 계속 client authority다. | H5-ORCH-008~009가 Proposal을 server store의 request id/base version에 연결해야 한다. |
| stale/replay | stale version은 versioned write에서 거절되지만 Proposal replay/one-time apply는 아직 해결되지 않았다. | 008 ledger와 009 terminal status/exactly-once apply 필요. |
| client-supplied Proposal | 아직 legacy apply 경로의 Proposal이 server ledger로 검증되지 않는다. | 008은 persistent Proposal DTO를 server-side로 저장해야 한다. |
| runtime-only store | restart/multi-worker CAS 보장이 없다. | 배포 요건이 확정되면 migration을 자동 시행하지 말고 durable store/transaction 결정을 별도 승인한다. |
| conditional cleanup | versioned mutation도 normalizer가 inactive 값/Matrix를 제거할 수 있다. | H5-ORCH-021에서 사용자 영향 안내를 만들되 규칙을 복제하지 않는다. |

# 다음 단계에서 반드시 참고할 내용

- H5-ORCH-008은 `request_id`와 server-provided `request_version`을 Proposal의 `base_version`으로 기록하고, Proposal 생성은 Request State/version을 바꾸지 않아야 한다.
- H5-ORCH-009은 store의 `compare_and_swap(request_id, base_version, mutation)` 안에서 latest Request를 다시 읽고, 승인 시 기존 sanitizer → geometry Adapter → `apply_patch_operations()` → `state_with_validation()`를 거쳐야 한다. conflict/validation failure/replay는 Request State/version과 Proposal terminal status를 안전하게 처리해야 한다.
- H5-ORCH-008~009는 current version을 client payload가 아니라 server `read()`에서 얻고, Proposal ledger/terminal status/exactly-once semantics를 이번 runtime store에 억지로 섞지 않는다.
- H5-ORCH-013 이후에도 Registry는 read-only이고 `geometry.products`는 LLM-facing Adapter DTO다. version store에 legacy geometry field를 저장하지 않는다.

# 다음 단계 수정이 예상되는 파일

- `request_ai_agent_h5_v0/request_state_store.py` — 009 approved apply가 CAS mutation을 연결할 때 재사용 후보
- 새 Proposal store/service 및 `chat_patch.py` adapter boundary — 008~009에서 server-side Proposal DTO와 revalidation 연결 후보
- `request_ai_agent_h5_v0/tests/test_orchestrator_request_version.py` 및 새 Proposal focused tests — stale/replay/duplicate/validation-failure 계약 위치

# 후속 개선 후보

- durable storage 필요성/배포 topology가 확정된 뒤에만 storage adapter와 transaction/migration 계획을 별도 단계로 제안
- request identity ownership/authorization, audit event와 idempotency key는 Proposal lifecycle 및 audit 단계에서 추가

# Roadmap 변경 필요 여부

없음. Worker는 H5-ORCH-007을 완료로 확정하지 않으며 Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 변경하지 않는다. Reviewer 검토 대기 상태로 남긴다.

# Git 상태와 Commit 여부

- 시작 시 Roadmap/current-stage/review-stage 문서와 이전 handoff/automation/Registry 관련 untracked 파일이 이미 존재했고 보존했다.
- 이번 단계의 의도된 변경은 request version store, additive API, focused test, 이 handoff 문서다.
- Commit 여부: Worker는 커밋하지 않는다.

# Worker 보고서

H5-ORCH-007의 최소 runtime Request identity/version/CAS 경계를 추가했다. 새 versioned API는 Request를 version 0으로 생성·조회하고 `expected_version` CAS write를 제공하며, stale conflict와 mutation 실패에는 State/version을 유지한다. 기존 `sanitize_state()`/`state_with_validation()` authority와 geometry Adapter/conditional cleanup을 그대로 재사용했다. 기존 client-held API는 호환을 위해 유지되므로 ledger, Proposal replay/exactly-once approval, durable multi-worker storage는 아직 해결되지 않았으며 H5-ORCH-008~009의 작업이다. Reviewer 검토 전 완료 상태를 확정하지 않는다.
