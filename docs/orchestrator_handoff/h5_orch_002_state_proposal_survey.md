# H5-ORCH-002 Request State · Proposal 경로 조사

# 단계 정보

- 단계 ID: `H5-ORCH-002`
- 단계명: Request State·Proposal 경로 조사
- 수행 기준 프로젝트 루트: `G:\Tech\00_Agent\01_Agent_Code\request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: `ed6c2af` (`build: add H5 orchestrator runner`)
- Roadmap 버전: `0.3`
- 작업 상태: 완료 후보 — Reviewer 검토 대기
- 조사 기준: 2026-07-31 (Asia/Seoul), 현재 작업 트리
- 범위: Request State 모델·직렬화·저장·조회, mutation, Proposal 승인/거절/적용, 우회 경로, stale/중복/동시성 위험
- 제외: Fieldset·출력·RAG/UI의 상세 설계 조사(H5-ORCH-003/004 범위), 앱·설정·테스트 코드 변경

# 이번 단계 목표

공식 Request State와 주요 mutation 및 기존 Proposal 승인 경로를 실제 코드에서 읽기 전용으로 추적해, H5-ORCH-005 이후의 최소 변경 설계가 실제 구조를 기반으로 시작할 수 있게 한다.

# 사전 입력 문서

- `AGENTS.md`
- `docs/orchestrator_handoff/orchestrator_roadmap.md`
- `docs/orchestrator_handoff/prompts/common_stage_contract.md`
- `docs/orchestrator_handoff/prompts/baseline_prompts.md`
- `docs/orchestrator_handoff/prompts/manual_stage_execution.md`
- `docs/orchestrator_handoff/h5_orch_001_repo_map.md`

# 실제 수행 내용

## 결론

현재 공식 Request State는 서버 DB나 파일에 저장되는 레코드가 아니다. 클라이언트가 각 API 호출에 `state` JSON을 포함하면 Flask가 이를 정규화·검증하여 응답의 `state`로 반환하고, 브라우저가 그 반환값을 다음 호출에 다시 전달하는 **클라이언트 보유형 구조화 상태**다. 따라서 현재는 `request_id`, 저장소 조회, 낙관적 version, 서버 측 Proposal ledger가 없다.

Chat Proposal도 서버에 보관되지 않는다. Proposal 생성 시 기준 State 일부의 SHA-256 fingerprint를 `proposal_context`에 붙일 뿐이며, `/api/chat/apply`는 클라이언트가 다시 제출한 Proposal과 State를 검사·적용한다. 이 구조는 승인 전 직접 변경을 피하지만, 서버가 Proposal의 발급·미사용·승인 상태를 권위 있게 보장하지 못한다.

## 공식 Request State: 모델, 정규화, 직렬화, 조회

### 모델과 계약

| 항목 | 실제 위치 | 확인 근거 |
|---|---|---|
| 초기 공식 상태 | `request_ai_agent_h5_v0/state.py:1058` `create_initial_state()` | `metadata`, `request_context`, `basic_info`, `analysis_overview`, `geometry`, `conditions`, `case_matrix`, `review`, `legacy_internal`을 생성한다. |
| 공식 정규화 경계 | `state.py:1160` `sanitize_state()` | 외부 입력을 초기 상태 기반으로 재구성하고, 허용된 metadata·필드·형상·조건·Case Matrix만 정규화한다. |
| 검증 포함 상태 | `validator.py:453` `state_with_validation()` | 정규화 상태에 `review.validator`, `metadata.issue_registry`, `review.submission`을 파생해 붙인다. |
| 공용 스키마 설명 | `schema.py:31-118` | `FieldSpec`, `SectionSpec`, `get_public_schema()`가 schema version, 상태값, section/field metadata를 API에 제공한다. |
| 필드 표현 | `state.py:351-378` | 필드는 `value`, `status`, `source`, `note`, `display_value`로 canonicalize된다. |
| HTTP 입력 경계 | `app.py:192-201` | `_state_from_request()`가 JSON의 `state`(없으면 payload 자체)를 읽고, `_derive_state()`가 `state_with_validation()`을 호출한다. |
| HTTP 직렬화 | `app.py:430-445`, `app.py:1148-1150` | `_response_payload()`가 정규화 `state`와 파생 결과를 반환하고 Flask `jsonify`가 JSON으로 직렬화한다. JSON ASCII escaping은 비활성화되어 있다. |

현재 h5 모델의 geometry 공식 형식은 `geometry.base_product`와 `geometry.comparison_products`이며 (`state.py:497-534`, `state.py:1231-1240`), Case Matrix는 `case_matrix.rows`의 수동 매핑이다 (`state.py:971-1055`). `sanitize_state()`는 전체 전달 State를 재구성하므로 누락되거나 현재 계약에 없는 키는 기본값으로 돌아가거나 제거될 수 있다.

### 저장소와 조회 경로

- 일반 Request 경로에는 파일·DB·Flask session·전역 Request map 저장 코드가 없다. `/api/bootstrap`은 매 호출마다 `_derive_state()`로 새 초기 상태를 반환한다 (`app.py:1233-1273`). `/api/request/new`도 새 초기 상태만 반환한다 (`app.py:1275-1285`).
- `/api/input/save`는 이름과 달리 요청 payload를 정규화해 반환할 뿐 저장하지 않는다 (`app.py:1287-1292`). `/api/preview`도 동일하게 전달 State에서 파생 응답을 만든다 (`app.py:1294-1299`).
- 기존 최소 회귀 테스트는 한 클라이언트가 `/api/input/save`로 반환받은 State가 다른 클라이언트의 `/api/bootstrap`에 나타나지 않으며, `/api/recent*`가 404임을 확인한다 (`tests/test_task12_minimal_regression.py:236-251`).
- `demo_db_store.py`에는 MySQL upsert/delete/commit 도우미가 남아 있으나, 현재 `submit()`은 `_disabled_db_upload()`만 사용한다 (`app.py:151-157`, `app.py:1606`). `upload_submission_to_demo_db`는 import만 되고 호출되지 않는다. 일반 Request의 활성 저장소로 보지 않는다.

따라서 조회의 권위는 서버 저장소가 아니라 **호출자가 보낸 최신 `state` JSON**이다. 정규화된 응답을 브라우저가 보관하는 것이 현재 UI/API 계약의 전제다.

## Request mutation 전체 경로

아래의 “변경”은 서버에 영속되는 변경이 아니라, 입력 State의 복사본 또는 새 상태를 응답으로 반환하는 변경이다. 클라이언트가 응답 State를 채택하여 다음 요청에 전송할 때만 사용자 흐름에서 지속된다.

| 경로 | 실제 변경/파생 | 승인 또는 제약 | 위험/비고 |
|---|---|---|---|
| `POST /api/request/new` | 새 초기 State를 반환한다. | 별도 승인 없음. | 기존 브라우저 State를 서버가 삭제하지는 않는다. |
| `POST /api/request-context/confirm` | 필수 context, fieldset snapshot, `context_locked=True`, 기본값, request number를 설정한다. | business unit/product group/platform/analysis type 필수 (`app.py:1171-1201`, `app.py:223-244`). | payload 전체 State를 기반으로 하므로 오래된 브라우저 State가 다른 변경을 누락시킬 수 있다. |
| `POST /api/request-context/fieldset` | context와 fieldset snapshot을 갱신하되 기존 lock 값은 유지한다. | 필수 context 확인 (`app.py:1202-1231`, `app.py:247-264`). | context 변경은 조건·Case Matrix 정규화 결과를 무효화/삭제할 수 있다. |
| `POST /api/input/save` | 전달 State를 정규화·검증하고 완료 알림 metadata를 덧붙여 반환한다. | 어떤 필드도 서버 측 allowlist로 제한하지 않는다. | 가장 넓은 직접 mutation 우회 경로다. Proposal 승인이나 version 검증 없이 임의의 구조화 State를 보낼 수 있다. |
| `POST /api/preview` | save와 마찬가지로 정규화 및 완료 알림 metadata를 포함한 State를 반환한다. | 없음. | 이름은 preview지만 반환 State에는 `assistant_notified_completed_stages`가 바뀔 수 있다 (`app.py:789-826`). |
| `POST /api/analysis-type/select` | 선택한 해석 유형 또는 demo 유형으로 State를 직접 갱신한다. demo는 여러 overview/geometry/condition 값을 채운다. | 유형 값 검증은 있으나 Proposal 승인 없음 (`app.py:1379-1414`; `analysis_type_recommender.py:434-472`; `demo_analysis_type.py:129-194`). | 현재 context confirm과 별개로 analysis type을 바꿀 수 있어 snapshot/lock 일관성을 재검토해야 한다. |
| `POST /api/chat/apply` | 승인된 operation을 State 복사본에 적용하고 정규화·검증한다. | stale fingerprint 검사와 operation 존재 검사는 한다 (`app.py:1684-1720`; `chat_patch.py:745-760`). | 아래 Proposal 수명주기 위험 참조. |
| `POST /api/review` + `approve_candidates=true` | AI 후보 condition의 source를 user/approved로 직접 승격한 뒤 final review를 만든다. | Boolean 하나가 승인 신호다 (`app.py:1515-1548`; `analysis_type_recommender.py:501-528`). | Proposal id, 기준 version, 후보별 선택 기록이 없다. 응답상 `state_changed=False`지만 반환 State의 review와 후보 source는 달라질 수 있다. |
| `POST /api/submit` + `approve_candidates=true` | 후보 condition 승인과 validation/submission 상태, 필요한 경우 request number를 반환 State에 설정한다. | validation 통과 여부만 확인 (`app.py:1550-1626`). | DB 업로드는 비활성화지만 candidate 승인은 review와 동일하게 bypass 가능하다. 응답은 `state_changed=False`이다. |
| `state_with_draft`, `state_with_final_review`, validation | draft/final review/validator처럼 파생 review 영역을 State copy에 채운다. | 구조화 State·Case Matrix 기반 (`draft_pipeline.py:389-395`, `review_pipeline.py:225-242`, `validator.py:453-467`). | 구조화 입력 자체의 권위는 바꾸지 않지만, 클라이언트가 반환 State를 보관하면 review substate는 변경된다. |

현재 비활성 feature 경로도 구분해야 한다. `/api/document-preview`, `/api/analysis-type/recommend`, `/api/conditions/recommend`는 함수 첫 줄에서 403을 반환하므로 그 아래의 legacy/Proposal 코드는 실행 불가다 (`app.py:1301-1316`, `app.py:1355-1377`, `app.py:1424-1467`).

## Agent/Proposal 생성, 승인, 거절, 적용

### 생성 및 read-only 보장

- `chat_patch.py:635-682`의 `extract_patch_proposal()`은 규칙 기반으로 operation을 만들고 `status=pending`, `state_changed=False`, `read_only=True`를 설정한다. LLM 결과도 `sanitize_external_operations()`의 allowlist를 거쳐 Proposal로 변환된다 (`chat_patch.py:494-565`, `app.py:1041-1106`).
- `/api/chat/instant`, `/api/chat/propose`, `/api/chat/send`의 patch 분기는 모두 State를 반환하지 않고 Proposal/dry-run만 만든다 (`app.py:1628-1682`, `app.py:1769-1810`). pending Proposal에는 `_store_pending_proposal()`가 fingerprint만 부착한다. 함수 주석대로 서버 저장은 하지 않는다 (`app.py:499-502`).
- `proposal_response()`의 dry-run은 `preview_patch()`/`apply_patch_operations()`로 별도 복사 State에만 적용한다 (`chat_patch.py:763-789`). 따라서 생성만으로 요청 State는 변경되지 않는다.
- `/api/chat/reject`는 전달받은 Proposal의 status만 `rejected`로 바꾸어 반환하고 State를 변경하지 않는다 (`app.py:1722-1737`).

### 적용 계약

`/api/chat/apply`는 클라이언트가 보낸 `proposal`과 `state`를 받는다. `proposal_context.source_fingerprints`가 전달 State에서 다시 계산한 네 fingerprint와 모두 같고 operation list가 비어 있지 않으면, `apply_patch_operations()`가 허용된 set/list/condition operation만 적용한 뒤 `sanitize_state()`와 validator를 실행한다 (`app.py:1689-1719`, `chat_patch.py:745-760`).

허용 patch 표면은 `chat_patch.py:71-90`의 `basic_info.*`, 일부 `analysis_overview.*`, legacy-style `geometry.*`, `conditions.fields.*.values`로 제한된다. Proposal의 `base_schema_version`은 생성되지만(`chat_patch.py:596-598`, `635-682`) apply 시 검사되지 않는다.

## 승인 전 변경, stale 적용, 중복 적용, 동시성 위험

### 승인 전 및 우회 mutation

1. `/api/input/save`와 `/api/preview`는 임의의 client `state`를 그대로 정규화 경계에 넣는다. Agent Proposal이 아닌 폼 mutation에는 필요한 현재 동작이지만, 미래 Proposal 계약은 이 우회 경로와 공존해야 한다.
2. `/api/analysis-type/select`은 Proposal 없이 State를 직접 바꾼다. demo branch는 더 넓은 State를 자동 입력한다.
3. `/api/review`와 `/api/submit`의 `approve_candidates=true`은 후보를 일괄 승인한다. 별도 Proposal lifecycle이나 stale 검사가 없다.
4. `/api/chat/apply`는 서버 저장된 pending Proposal을 조회하지 않고 client supplied Proposal을 신뢰한다. 현재 State의 fingerprint를 재생성할 수 있는 호출자는 `proposal_context`를 위조해 allowlist 안의 operation을 적용할 수 있다. 이는 인증/권한 모델이 없고 State 자체도 client authority인 현재 구조와 일치하지만, “서버 권위의 승인”으로 해석하면 안 된다.

### stale/version

- 현재 stale 보호는 `app.py:465-496`의 네 fingerprint다: `original_fields`, `analysis_type`, `condition_snapshot`, `case_matrix`. 하나라도 달라지면 적용을 막는다.
- `request_id`도 request version도 없고, HTTP payload에 compare-and-swap precondition도 없다. `base_schema_version`은 호환성 표기일 뿐 적용 보호가 아니다.
- fingerprint는 metadata 전체, request number, chat history, 일부 request context 값 등을 포괄하지 않는다. 반대로 operation과 무관한 원본 field 변경도 네 묶음 중 하나가 달라지면 Proposal 전체를 stale 처리한다. 이는 false negative와 과도한 invalidation 모두 가능함을 뜻한다.
- apply는 요청 시작 후 별도 서버 상태를 다시 읽지 않는다. 즉, 서버 저장소가 도입되면 현재 구현만으로는 read-check-write 원자성이 없다.

### 중복 적용 및 lifecycle

- Proposal id는 UUID 문자열이지만 서버에 pending/applied/rejected ledger가 없다. apply/reject는 id의 존재·발급자·이미 사용됨을 검증하지 않는다.
- 같은 base State와 Proposal을 재전송할 수 있다. replace 및 dedupe 처리 덕분에 일부 operation은 값이 같을 수 있으나, 상태 변경이라고 응답하고 replay 차단은 없다.
- rejection도 서버에서 terminal state로 기록되지 않는다. 거절한 Proposal을 다시 apply할 수 있고, `status` 값 자체는 apply의 전제 조건으로 검사되지 않는다.

### 동시성 및 데이터 손실

- 서버 공유 State가 없으므로 서로 다른 브라우저/탭은 자동 병합되지 않는다. 각 응답 State 중 브라우저가 마지막으로 채택해 다음 요청에 보낸 것이 사실상 승자가 된다.
- 오래된 full State를 `/api/input/save`, context API, analysis type API에 보내면 다른 탭의 변경이 payload에 없으므로 정규화 후 소실될 수 있다. 최소 회귀 테스트는 클라이언트 격리를 확인할 뿐 병합이나 충돌 처리를 보장하지 않는다.
- `sanitize_state()`는 활성 fieldset/geometry를 기준으로 조건 및 Case Matrix를 재계산하고, 유효하지 않은 선택을 비운다 (`state.py:971-1055`, `state.py:1242-1269`). 올바른 정규화이지만 context/geometry가 오래된 payload인 경우 의도치 않은 삭제로 나타날 수 있다.
- request number는 context confirm/submit에서 난수 기반 sequence를 사용하지만(`app.py:209-220`, `1555-1574`) 저장소 unique constraint 및 충돌 재시도는 활성 Request 흐름에 없다. `assign_request_no_if_missing()`의 기본 sequence는 1이다(`state.py:1147-1157`). 영속 저장을 도입하면 식별자 발급 책임을 별도로 설계해야 한다.

### 현재 모델과 chat patch의 불일치

중요한 구조 불일치가 있다. chat patch allowlist는 `geometry.products`, `geometry.parts`, `geometry.has_changed_part`, `geometry.changed_from_part`을 허용하지만 (`chat_patch.py:71-90`), h5 정규화 geometry는 `base_product`, `comparison_products`, `boundary_bindings`만 공식 모델로 재구성한다 (`state.py:1231-1240`). `sanitize_state()`가 legacy-style `products`/`parts`를 현재 공식 geometry로 변환하지 않으므로 geometry 관련 Proposal operation은 apply 직후 정규화에서 제거되거나 공식 Case Matrix에 반영되지 않을 가능성이 높다. H5-ORCH-005~009에서는 이 경로를 그대로 확장하지 말고 공식 field registry/binding과 맞춘 migration 또는 adapter 결정을 먼저 해야 한다.

# 다음 단계에서 반드시 참고할 내용

## H5-ORCH-005~009 필수 참고 지점

| 후속 단계 | 반드시 참고할 파일·계약·테스트 | 이유 |
|---|---|---|
| 005 최소 변경 아키텍처 | `state.py:1058-1321`, `app.py:192-264`, `app.py:430-502`, `app.py:1171-1299`, `tests/test_task12_minimal_regression.py:218-251` | client-held canonical State, 정규화 경계, 현재 조회/저장 부재, client isolation을 기준으로 target authority를 정해야 한다. |
| 006 Field Registry | `schema.py:31-118`, `state.py:351-378`, `state.py:497-534`, `state.py:971-1055`, `chat_patch.py:71-90` | public FieldSpec과 실제 canonical State, Case Matrix binding, legacy patch path가 다르다. |
| 007 Request State version | `app.py:460-496`, `chat_patch.py:568-598`, `chat_patch.py:635-760`, `state.py:1160-1321` | schema version과 per-request version/fingerprint/CAS의 역할을 분리해야 한다. |
| 008 Proposal 계약·저장 구조 | `chat_patch.py:494-682`, `app.py:484-502`, `app.py:1628-1720`, `app.py:1769-1810` | 현재 Proposal은 client supplied이고 server ledger가 없으며 operation allowlist와 official geometry가 불일치한다. |
| 009 Proposal 승인 lifecycle | `app.py:491-502`, `app.py:1684-1737`, `analysis_type_recommender.py:501-528`, `app.py:1515-1626` | stale, replay, rejection terminality, candidate approval bypass, apply idempotency를 명시적으로 설계·테스트해야 한다. |

후속 검증은 적어도 다음을 추가할 위치가 필요하다: `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py` 또는 새 focused test module. 최소 matrix는 승인 전 State 불변, stale version 거절, 같은 Proposal의 두 번째 apply 거절, forged/unknown Proposal 거절, 두 client의 update conflict, direct form mutation 뒤 Proposal invalidation, official geometry patch가 Case Matrix에 반영되는지다.

# 다음 단계 수정이 예상되는 파일

- H5-ORCH-005: `docs/orchestrator_handoff/h5_orch_005_target_architecture.md`
- H5-ORCH-006: `request_ai_agent_h5_v0/schema.py`, `request_ai_agent_h5_v0/state.py`, `request_ai_agent_h5_v0/chat_patch.py`
- H5-ORCH-007: `request_ai_agent_h5_v0/state.py`, `request_ai_agent_h5_v0/app.py`, 관련 focused test module
- H5-ORCH-008~009: `request_ai_agent_h5_v0/chat_patch.py`, `request_ai_agent_h5_v0/app.py`, `request_ai_agent_h5_v0/analysis_type_recommender.py`, 관련 focused test module

# 최소 검증

| 확인 | 결과 |
|---|---|
| 소스 정적 추적 | 완료. `state.py`, `schema.py`, `app.py`, `chat_patch.py`, `analysis_type_recommender.py`, `demo_analysis_type.py`, `validator.py`, `draft_pipeline.py`, `review_pipeline.py`, `demo_db_store.py`, 최소 회귀 테스트를 읽었다. |
| 일반 Request 저장소 탐색 | 활성 `app.py` 경로에서 DB/파일/session/전역 Request 저장소를 확인하지 못했다. Demo DB helper는 존재하지만 submit의 실제 경로는 disabled payload다. |
| Proposal 승인 전 State 변경 | 생성 API와 `proposal_response()`가 `state_changed=False` 및 dry-run copy를 사용함을 코드로 확인했다. |
| stale/replay 보호 | fingerprint stale check는 존재하나 Request version, server ledger, status/one-time 검증이 없음을 코드로 확인했다. |
| 최소 회귀 테스트 | `G:\Tech\00_Agent\01_Agent_Code\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py` 실행 결과 `16 passed in 1.26s`. |

# 실패하거나 실행하지 못한 검증

- 없음. 최소 회귀 테스트는 상위 작업공간의 `.venv`에서 통과했다.
- 실제 LLM, 외부 RAG/vector store, Demo DB upload는 조사 범위를 벗어나고 Request State를 실제로 변경하지 않는 원칙에 따라 실행하지 않았다.

# 알려진 문제와 제한사항

- 이 단계는 실제 앱 상태 저장소나 Request version을 구현하지 않은 읽기 전용 조사다. 식별자·저장소·원자 갱신 방식은 H5-ORCH-005~009 설계에서 확정해야 한다.
- 비활성 DB upload와 disabled feature 아래의 legacy code는 활성 MVP 실행 경로가 아니므로, 향후 활성화 시 별도 조사가 필요하다.
- UI의 반환 State 채택 시점은 H5-ORCH-004 범위이므로 상세 조사를 수행하지 않았다.

# 발견된 위험

- R-001: Agent Proposal 외 `/api/input/save`, analysis-type 선택, candidate approval이 공식 State를 직접 바꿀 수 있다.
- R-002: stale 보호가 per-request version/CAS가 아니라 client-state fingerprint이며 위조·재전송·TOCTOU 방어가 불완전하다.
- R-006: Proposal lifecycle ledger가 없어서 applied/rejected 상태와 중복 apply를 서버가 보장하지 못한다.
- 신규 위험: chat patch geometry 경로가 현재 h5 공식 geometry 계약과 다르다. 이 문제는 H5-ORCH-005의 target architecture 결정을 막지는 않지만 006/008 전에 해결 방향을 확정해야 한다.

# 변경 파일

| 파일 | 변경 |
|---|---|
| `docs/orchestrator_handoff/h5_orch_002_state_proposal_survey.md` | H5-ORCH-002 읽기 전용 조사 인수인계 문서 추가 |

# 신규 또는 변경된 데이터 구조

없음. 조사 단계이므로 애플리케이션 State/Proposal 데이터 구조는 변경하지 않았다.

# 신규 또는 변경된 API

없음. 앱 API와 UI 호출 계약은 변경하지 않았다.

# 중요 설계 결정

- 후속 설계의 공식 기준점은 현재 client-supplied State를 정규화하는 `state.py`/`app.py` 경계다.
- schema version, per-request version, stale fingerprint는 서로 다른 책임으로 분리해야 한다.
- Proposal lifecycle은 client payload 상태가 아니라 server-side 발급·상태·idempotency 계약으로 설계해야 한다.
- geometry patch는 legacy path를 확장하지 않고 h5 공식 geometry binding에 맞춘 adapter 또는 migration 결정을 선행해야 한다.

# 기존 기능 재사용 지점

- State 정규화: `state.py`의 `sanitize_state()` 및 초기 State 생성
- 스키마 metadata: `schema.py`의 `FieldSpec`/`SectionSpec`/`get_public_schema()`
- 기존 검증: `validator.py`의 `state_with_validation()`
- 기존 patch 적용: `chat_patch.py`의 operation allowlist 및 `apply_patch_operations()`
- 기존 API 응답 형식: `app.py`의 `_state_from_request()`와 `_response_payload()`

# 수행하지 않은 작업

- H5-ORCH-003의 Fieldset·Validation·출력 상세 조사 및 H5-ORCH-004의 RAG/UI 상세 조사를 수행하지 않았다.
- 앱·설정·테스트·DB schema·Roadmap·다음 단계 프롬프트를 수정하지 않았다.
- 실제 Request, 외부 DB, 실제 LLM/RAG 호출을 변경하거나 실행하지 않았다.

# 후속 개선 후보

- Request 저장소와 단조 version/CAS 계약 도입 시 request number 발급 책임과 충돌 재시도 정책을 함께 정리한다.
- Proposal replay, forged Proposal, direct form mutation 뒤 invalidation을 focused regression test로 고정한다.

# Roadmap 변경 필요 여부

필요함. 단, 이 Worker는 Roadmap을 변경하지 않는다. 독립 Reviewer가 이 문서와 검증 결과를 승인한 뒤에만 H5-ORCH-002 완료 상태 및 다음 단계 계획을 확정한다.

# Git 상태와 Commit 여부

- 이 단계에서 추가·수정한 파일: `docs/orchestrator_handoff/h5_orch_002_state_proposal_survey.md`만.
- 기존 사용자/선행 단계 변경으로 `docs/orchestrator_handoff/orchestrator_roadmap.md` 수정과 H5-ORCH-001 문서·automation 산출물·`__pycache__` 미추적 항목이 존재하며, 이를 수정하거나 stage하지 않았다.
- Commit 여부: 하지 않음. Worker는 Reviewer 검토 대기 상태이며, Roadmap 상태를 스스로 완료로 확정하지 않는다.

# Worker 보고서

H5-ORCH-002 조사 문서를 공통 계약 형식으로 보완했다. 공식 Request State는 client-supplied JSON을 정규화해 반환하는 구조이며, 현재 Proposal은 서버 저장 없이 fingerprint만 붙여 client가 재제출한다. 핵심 후속 설계 항목은 Request version/CAS, server-side Proposal lifecycle, form mutation과 Proposal의 단일 적용 경계, 그리고 legacy chat geometry path와 h5 공식 geometry 모델의 정합성이다. `G:\Tech\00_Agent\01_Agent_Code\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`는 16개 통과했다. 이번 보완은 이 survey 문서만 변경했으며 Roadmap/기준 카드/다음 단계 프롬프트는 변경하지 않았다. Reviewer 검토 대기 상태로 남긴다.
