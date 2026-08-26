# H5-ORCH-003 Fieldset·Validation·출력 구조 조사

# 단계 정보

- 단계 ID: `H5-ORCH-003`
- 단계명: Fieldset·Validation·출력 구조 조사
- 수행 기준 프로젝트 루트: `G:\Tech\00_Agent\01_Agent_Code\request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: `dfd6655b6843a397b43838997a8e7827b8073494` (현재 작업 트리; Roadmap의 기준 Commit 표기는 `ed6c2af`)
- Roadmap 버전: `0.4`
- 작업 상태: 완료 후보 — Reviewer 검토 대기
- 조사 기준: 2026-07-31 (Asia/Seoul), 읽기 전용 정적 추적
- 범위: field 원천/public schema, request context 기반 condition Fieldset, State 정규화, Validator·Case Matrix·draft/final review, Preview·Word 출력 계약

# 이번 단계 목표

기존 h5_v0의 공용 field 설명, 실제 조건 카드 Fieldset, Validation·Case Matrix·review·Preview·Word 엔진의 입력/출력/재사용 경계를 추적했다. H5-ORCH-005와 H5-ORCH-006은 아래의 기존 builder와 정규화 경계를 호출·조회해야 하며, 조건 규칙이나 renderer를 복제해서는 안 된다.

# 사전 입력 문서

- `AGENTS.md`
- `docs/orchestrator_handoff/orchestrator_roadmap.md`
- `docs/orchestrator_handoff/prompts/common_stage_contract.md`
- `docs/orchestrator_handoff/prompts/baseline_prompts.md`
- `docs/orchestrator_handoff/prompts/manual_stage_execution.md`
- `docs/orchestrator_handoff/h5_orch_001_repo_map.md`
- `docs/orchestrator_handoff/h5_orch_002_state_proposal_survey.md`

# 실제 수행 내용

## 결론과 최소 변경 경계

`schema.py`의 공용 `FieldSpec` 목록과 `condition_fieldsets.py`의 실제 조건 카드 템플릿은 같은 key 일부를 공유하지만 단일 정의가 아니다. 공용 schema는 API 설명/legacy metadata의 원천이고, 현재 활성 조건·필수 여부·Case Matrix 열은 `build_condition_fieldset()`과 카드형 `conditions.condition_sets`가 결정한다. 공식 State 경계는 여전히 `state.sanitize_state()`이며, 이 함수가 조건 카드를 활성 Fieldset에 맞춰 재구성한 직후 Case Matrix를 재정규화한다.

따라서 H5-ORCH-006의 Registry는 새 규칙 저장소가 아니라 다음 두 adapter view를 제공하는 최소 구조여야 한다.

| Registry/Adapter 후보 | 반드시 위임할 기존 원천 | 제공해야 할 읽기 결과 | 복제 금지 대상 |
|---|---|---|---|
| Public schema adapter | `schema.py:get_public_schema()`, `FieldSpec`, `SectionSpec`, `constants.py:*_FIELD_DEFS` | section/key/label/type/unit/static required/binding/legacy key | `FieldSpec` 정의 재작성 |
| Active condition-fieldset adapter | `condition_fieldsets.py:build_condition_fieldset()`, `get_active_condition_fields()`, `get_active_case_matrix_columns()` | context별 card/field active·required·ordered case-column, card-instance State binding | `_REQUIRED_BY_TYPE`, `CARD_TEMPLATES`, `CASE_MATRIX_CONDITION_COLUMNS` 복사 |
| Canonicalization adapter | `state.py:sanitize_state()` | patch 후의 canonical State, 재계산된 `conditions.fields`와 `case_matrix` | 카드 필터/Case Matrix 선택 정리 재구현 |

## Field 원천과 public schema/state 경로

| 층 | 실제 원천·진입점 | 입력 | 출력/역할 | 주의점 |
|---|---|---|---|---|
| Static public metadata | `constants.py:BASIC_INFO_FIELD_DEFS`, `REQUEST_CONTEXT_FIELD_DEFS`, `ANALYSIS_OVERVIEW_FIELD_DEFS`, `CONDITION_FIELD_DEFS` | Python 상수 | `schema.py:FieldSpec`, `SectionSpec`, `get_public_schema()` | `CONDITION_FIELD_DEFS`는 카드 field와 일치하지 않는 legacy/public catalog도 포함한다. |
| Public API | `app.py:/api/bootstrap` | 없음 | `schema`, initial validated `state`, `case_matrix`, `validation` | `schema`는 active Fieldset 결과가 아니다. |
| Dynamic condition templates | `condition_fieldsets.py:CARD_TEMPLATES`, `_REQUIRED_BY_TYPE`, `CASE_MATRIX_CONDITION_COLUMNS` | `request_context.analysis_type` | active group/field/required 수준 및 ordered case columns | 현재 `operation_mode`는 fieldset 반환에 `""`로만 들어가며 active 규칙을 바꾸지 않는다. |
| Canonical State | `state.py:create_initial_state()`, `sanitize_state()` | client-supplied State | `request_context`, card형 `conditions.condition_sets`, derived `conditions.fields`, manual `case_matrix` | 허용되지 않거나 비활성인 입력은 기본값/제거/정리될 수 있다. |

`FieldSpec`의 `required`는 static metadata다. 반면 실제 조건 카드의 field metadata는 `_field(..., required=active)`로 만들어진다. 즉 활성 card의 모든 field가 `required=True`, `required_level="required"`이고 비활성 card의 field는 `required=False`, `optional_non_blocking`이지만 해당 card는 `field_keys`와 `condition_sets`에서 제외된다. 현재 조건 카드에는 `conditional_required`를 산출하는 template가 없지만 Validator와 UI에는 그 level/group을 처리하는 호환 경로가 있다.

### Request context → Fieldset → canonical State

1. `POST /api/request-context/confirm`과 `/api/request-context/fieldset`는 payload의 `state`/`request_context`를 받아 business unit, product group, platform, analysis type이 모두 있는지 확인한다 (`app.py:_context_confirm_state`, `_context_fieldset_state`).
2. 두 helper는 `build_condition_fieldset(current_context)`을 호출하고 `analysis_type`, `condition_fieldset_key`, `condition_fieldset_snapshot`, `context_locked`를 State에 넣는다. confirm은 lock을 `True`로 하고 기본 overview/request number를 적용한다. fieldset refresh는 기존 lock만 유지한다.
3. 두 helper의 마지막 `_derive_state()`는 `state_with_validation()`을 호출한다. 그 내부 `sanitize_state()`가 `sanitize_condition_sets(raw condition_sets, request_context)`로 active card만 새로 만들고, `get_active_condition_fields(state)`로 derived `conditions.fields`를 다시 만든다.
4. 같은 `sanitize_state()` 호출 안에서 `_sanitize_manual_case_matrix()`가 `get_active_case_matrix_columns(request_context)`와 active card 값으로 dropdown option/visible column/row selection을 재생성한다.

`request_context.condition_fieldset_snapshot`은 UI/응답에 보관되는 group snapshot이지만 현재 normalizer와 Validator의 활성 판정은 이를 읽어 재현하지 않고 live `request_context.analysis_type`로 builder를 다시 호출한다. 따라서 snapshot은 현 상태에서 authority가 아니라 표시·stale fingerprint 대상에 가깝다.

## 활성·비활성·필수 규칙과 Case Matrix 산출

| analysis type | active card | active field | Case Matrix condition column |
|---|---|---|---|
| `이슬맺힘` | operating, heat_exchanger, supply_air, space_environment | fan_rpm; name/fin_type/tube_diameter/row_count/fpi; heat_exchanger_temp/rh; room_temp/rh | fan_rpm, heat_exchanger(name), heat_exchanger_temp/rh, room_temp/rh |
| `열유동 해석` | 위와 동일 | 위와 동일 | 위와 동일 |
| `일반 유동 해석`, `열교환기 유속 프로파일` | operating, heat_exchanger | fan_rpm; name/fin_type/tube_diameter/row_count/fpi | fan_rpm, heat_exchanger(name) |

- `condition_fieldsets.py:_analysis_type()`는 일부 alias를 일반 유동으로 바꾸며, 알 수 없거나 빈 analysis type은 이슬맺힘으로 fallback한다.
- `sanitize_condition_sets()`는 비활성 card를 source list에서 수집하지 않고 결과에 넣지 않는다. active card가 누락되면 빈 기본 card 하나를 새로 만든다. operating card에서 `running=False`인 fan은 derived active field 및 Matrix option에서 제외된다.
- `_manual_matrix_condition_options()`은 operating의 각 running fan RPM, heat_exchanger의 `name`, 나머지 active card의 matching field에서 중복 제거한 최신 dropdown value를 만든다. `_sanitize_manual_case_matrix()`은 이 value set에 없는 `condition_values`와 비활성 열을 제거한다.
- `conditions.fields`의 실제 key는 public `conditions.room_temp`가 아니라 예를 들어 `space_environment_1.room_temp`처럼 card instance prefix를 포함한다. `field_key`는 `room_temp`로 따로 보존된다. H5-ORCH-006은 field definition ID와 instance binding을 분리해야 한다.

## Validator, Case Matrix, draft/final review

| 엔진/호출 지점 | 입력 계약 | 출력 계약 | 기존 재사용 방식 |
|---|---|---|---|
| `validator.validate_state()` | 임의 Mapping State | `blocking`, `warning`, `info`, `summary` | 내부에서 sanitize + geometry axis 후 static basic/overview required, geometry, active condition, current Matrix selection을 검증한다. chat log를 사용하지 않는다. |
| `validator.state_with_validation()` | raw State | canonical State + `review.validator`, `metadata.issue_registry`, `review.submission` | API의 `_derive_state()`가 공통 진입점으로 사용한다. |
| `state._sanitize_manual_case_matrix()` | raw matrix + normalized products + active condition sets/context | manual rows, visible_columns, dropdown_options, source_inputs | 실제 활성 Matrix 엔진이다. invalid selection clear, 삭제 geometry의 auto row 제거, 새 geometry auto row 추가를 수행한다. |
| `case_matrix.generate_case_matrix()` / `state_with_case_matrix_generation()` | State | `case_matrix` / normalized State | 역사적 API 호환 wrapper이며 조합 생성이 아니다. 앱 route가 직접 호출하지 않는다. |
| `draft_pipeline.build_request_draft()` | State, 선택적인 read-only RAG package | `status`, structured draft document, validation summary/blocks/warnings | 먼저 validation한다. submit 가능일 때만 markdown을 채우며 State를 변경하지 않는다. |
| `review_pipeline.build_final_review()` / `state_with_final_review()` | State, 선택 draft | final review, optional `build_submission_contract()` payload / State의 `review.*` | validator + manual case row 수를 재사용한다. final payload authority는 `structured_state_and_case_matrix_only`다. |

Validator의 조건 검증은 lock이 없으면 `request_context.not_locked`를 blocking으로 반환한다. lock 후에는 `get_active_condition_fields()`만 읽어 active field에 값이 있는지 검사하고, 조건부 group이 존재하면 group 중 하나 이상의 provided value를 요구한다. 이후 Matrix 검증은 `visible_columns`의 condition key마다 해당 dropdown_options의 현재 값만 허용한다. 따라서 Fieldset과 Matrix의 최신 State 정규화가 Validator보다 선행한다.

## Preview와 Word 출력

| 경로 | 실제 입력 | 실제 출력/호출 | 상태/호환성 |
|---|---|---|---|
| `POST /api/preview` | client `state` | `_derive_state()`와 progress notification이 든 JSON State/case_matrix/validation | 활성. 이름과 달리 `preview_document.py` renderer를 호출하지 않는다. 정규화 응답이며 metadata notification은 바뀔 수 있다. |
| Browser Preview | browser `requestState`, `collectState()` | `ui.py:renderDocumentPreviewPanel()`의 current-state DOM | 활성. State의 overview/context, official geometry, `condition_sets`, Matrix visible columns/cells를 직접 렌더한다. |
| `preview_document.build_request_preview()` | raw State | sections/markdown/case matrix summary | 코드와 direct test는 존재하나 Flask `/api/document-preview`는 첫 줄 403으로 반환한다. 함수는 legacy overview/geometry field names를 읽는 부분이 있어 현재 UI Preview 대체물로 가정하면 안 된다. |
| `POST /api/export/word` | `{sections:[{title, blocks:[field/table/stale]}]}` serialized browser preview DOM | DOCX bytes, fixed `analysis_request.docx` | 활성. `word_export.build_word_docx()`는 State/Validator/Fieldset을 받거나 재계산하지 않고 입력 순서 그대로 DOCX XML을 작성한다. |

UI의 Word path는 `exportWordFromPreview()`에서 먼저 browser field를 `collectState()`로 모아 `renderDocumentPreviewPanel()`을 다시 그린 다음, `previewDomForWord()`가 `data-preview-*` DOM을 `{sections, blocks}` JSON으로 직렬화해 `/api/export/word`에 POST한다. 서버 Word endpoint에는 readiness/validation gate가 없다. `FEATURE_LOCKS.word_export=True`인 반면 `FEATURE_LOCKS.preview_screen=False`이고 `/api/document-preview`가 비활성인 점은 의도적 분리로 기록해야 한다.

## 대표 조건부 field end-to-end: `room_temp` (공간 온도)

선택 이유: `room_temp`는 공용 schema에도 있고, 이슬맺힘/열유동에서만 활성인 `space_environment` card 및 Case Matrix 열에 실제 연결된다. 일반 유동 해석으로 context를 바꾸면 값과 Matrix 선택이 정규화에서 제거되는 경계를 하나의 추적으로 확인할 수 있다.

1. 정의: `constants.py:CONDITION_FIELD_DEFS`는 `room_temp`의 label/unit/binding/legacy key를 public schema에 제공하고 `schema.py:CONDITION_FIELD_SPECS`가 이를 `FieldSpec`으로 만든다. 실제 카드 정의는 별도로 `condition_fieldsets.py:CARD_TEMPLATES`의 `space_environment` → `(room_temp, 공간 온도, °C)`다.
2. 활성화: `condition_fieldsets.py:_REQUIRED_BY_TYPE`에서 이슬맺힘과 열유동 해석만 `space_environment`를 포함한다. `build_condition_fieldset()`은 card와 두 field (`room_temp`, `room_rh`)를 `active=True`, `required=True`, `required_level=required`로 반환한다. 일반 유동 해석은 해당 card를 inactive로 반환한다.
3. State binding/정규화: context confirm/fieldset API가 snapshot을 넣은 뒤 `_derive_state()`를 호출한다. `sanitize_condition_sets()`는 이슬맺힘일 때 `space_environment_1.fields.room_temp`만 canonical value row로 보관하고 `get_active_condition_fields()`는 derived `conditions.fields`에 key `space_environment_1.room_temp`, `field_key=room_temp`, `card_id=space_environment_1`를 만든다.
4. Validation과 Matrix 소비: `validator._validate_conditions()`는 derived room_temp values 중 provided value가 없으면 `conditions.space_environment_1.room_temp.required_missing` blocking issue를 낸다. `_manual_matrix_condition_options()`은 active space_environment card 값에서 `room_temp` option을 만들고, Matrix가 `room_temp` visible column을 보일 때 row selection은 이 option set에 있어야 한다. `validator._validate_case_matrix()`은 없거나 stale한 선택을 `case_matrix.room_temp.missing`으로 막는다.
5. 비활성화/출력: analysis type을 일반 유동으로 바꾼 뒤 `sanitize_state()`하면 `sanitize_condition_sets()`이 `space_environment` card 전체를 제외하고 `_sanitize_manual_case_matrix()`가 `room_temp`/`room_rh` 열·row values를 제거한다. Browser Preview는 남은 `condition_sets`와 normalized Matrix만 표시하며 Word는 그 Preview DOM만 직렬화한다.

정적 회귀 근거는 `tests/test_task12_minimal_regression.py:test_analysis_type_controls_active_cards_columns_and_clears_inactive_values`다. 이 테스트는 이슬맺힘에서 6개 active Matrix condition column을 확인하고 일반 유동으로 바꾼 뒤 `space_environment`/`supply_air`가 card 목록에서 제거되고 row keys가 `fan_rpm`, `heat_exchanger`로 제한됨을 확인한다.

# 변경 파일

| 파일 | 변경 |
|---|---|
| `docs/orchestrator_handoff/h5_orch_003_rules_engines_survey.md` | H5-ORCH-003 읽기 전용 조사 인수인계 문서 추가 |

# 신규 또는 변경된 데이터 구조

없음. 애플리케이션 State, field definition, Fieldset, Validator, Case Matrix, renderer, API를 변경하지 않았다.

# 신규 또는 변경된 API

없음. 조사 중 API 호출·실제 Request 변경·외부 DB·실제 LLM/RAG 호출을 하지 않았다.

# 중요 설계 결정

- H5-ORCH-005는 public schema와 dynamic condition card Fieldset을 하나의 기존 source로 오인하지 않아야 한다. Registry는 둘을 설명·binding하는 adapter여야 한다.
- H5-ORCH-006은 active/required/case-column 판단을 `build_condition_fieldset()` 결과에 위임하고 canonical update 뒤에는 반드시 `sanitize_state()` 결과를 읽어야 한다.
- `request_context.condition_fieldset_snapshot`은 현재 active rule authority가 아니다. 정책상 snapshot authority로 승격할지, live builder 결과만 authority로 유지할지는 005에서 명시해야 한다.
- Preview/Word 연결은 renderer를 새로 만들지 말고 현재 browser preview DOM → `build_word_docx()` 계약을 재사용해야 한다. `/api/document-preview` 활성화나 `preview_document.py` 대체는 이 단계의 범위가 아니다.

# 기존 기능 재사용 지점

- Static metadata/public API: `constants.py`, `schema.py:get_public_schema()`, `/api/bootstrap`.
- Dynamic Fieldset: `condition_fieldsets.py:build_condition_fieldset()`, `sanitize_condition_sets()`, `get_active_condition_fields()`, `get_active_case_matrix_columns()`.
- Official normalization/Matrix: `state.py:sanitize_state()`, `_sanitize_manual_case_matrix()`.
- Validation: `validator.py:validate_state()`, `state_with_validation()`.
- Draft/final review/export payload: `draft_pipeline.py:build_request_draft()`, `review_pipeline.py:build_final_review()`/`state_with_final_review()`, `export_contract.py:build_submission_contract()`.
- Active Preview/Word: `ui.py:renderDocumentPreviewPanel()`/`previewDomForWord()`/`exportWordFromPreview()`, `app.py:/api/export/word`, `word_export.py:build_word_docx()`.

# 수행하지 않은 작업

- H5-ORCH-004의 Agent/Q&A/RAG/UI 상세 조사를 수행하지 않았다. UI는 Preview와 Word의 입력 계약·호출 경로 확인에 필요한 함수만 정적으로 읽었고, Agent intent/Proposal UI/session/RAG 설계·실행을 조사하지 않았다.
- H5-ORCH-005 이후의 Registry/Adapter, Request version, Proposal lifecycle, UI 변경을 설계·구현하지 않았다.
- 앱·설정·테스트·DB schema·Roadmap·기준 카드·다음 단계 프롬프트를 수정하지 않았다.

# 최소 검증

| 확인 | 결과 |
|---|---|
| 대표 조건부 field 정적 추적 | 완료. `room_temp`의 constants/schema → Fieldset → `sanitize_state()` → Validator/Case Matrix → browser Preview/Word 경로를 위에 기록했다. |
| 기존 회귀 테스트 | 프로젝트 루트에서 `G:\Tech\00_Agent\01_Agent_Code\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py` 실행: `16 passed in 1.37s`. 상위 작업공간에서 사용자가 제시한 동일 상대 경로는 실제 test 파일보다 한 단계 짧아 `file or directory not found`(0 collected)였으며, 이는 경로 기준 차이다. |
| 문서 인코딩 | `G:\Tech\00_Agent\01_Agent_Code\.venv\Scripts\python.exe tools/check_encoding.py --changed` 실행: `Encoding check passed`. |
| diff 형식 | `git diff --check` 실행: 성공(출력 없음). |

# 실패하거나 실행하지 못한 검증

- 실제 LLM/RAG, 외부 DB, 실제 browser/download, disabled `/api/document-preview`의 아래 unreachable 코드 경로는 실행하지 않는다. 이는 범위 및 상태 변경 금지에 따른 의도적 제외다.
- `preview_document.build_request_preview()`의 legacy-style field 표현은 정적 확인만 했다. 활성 browser Preview와 완전 동일하다는 E2E 검증은 수행하지 않는다.

# 알려진 문제와 제한사항

- `conditions.fields`에는 FieldSpec 기반의 초기/legacy representation이 존재하지만 `sanitize_state()`가 active card에서 derived list를 다시 만든다. static `CONDITION_FIELD_DEFS`의 `material_type`, `pressure`, `vane_or_louver`, `filter_state` 등은 현재 card-based Fieldset/Matrix에서 활성 input으로 나오지 않는다.
- `condition_engine.py`에는 condition-axis/cartesian helper가 남아 있으나 active app validation/Matrix path는 manual mapping을 사용한다. `case_matrix.py`의 historical generate wrapper도 cartesian generation을 하지 않는다. 005/006이 이 legacy-like helper를 새 authority로 채택하면 현 UI와 달라질 수 있다.
- `preview_document.py`는 `state_with_validation()`을 호출하지만 `analysis_overview.analysis_type`, `geometry.products` 같은 현 State와 다른 legacy-style reads를 포함한다. Flask route도 403이므로, 이를 활성 Preview의 public contract로 문서화하면 안 된다.

# 발견된 위험

| 위험 | 근거와 영향 | H5-ORCH-005~006 대응 |
|---|---|---|
| R-004 조건부 비활성화 값 유실 | active type 변경 시 `sanitize_condition_sets()`이 비활성 card를 결과에서 제외하고 Matrix invalid selection/columns도 제거한다. `room_temp`는 일반 유동 전환 시 canonical State에서 사라진다. | Proposal/apply 전후 Fieldset diff와 inactive-value retention policy를 명시한다. 현재 canonical State만 patch의 유일한 보존 위치로 가정하지 않는다. |
| R-005 규칙 이중화 | static public schema와 dynamic card template이 분리돼 있고 label/unit/key도 일부 중복/상이하다. | public schema adapter와 active-fieldset adapter를 분리하고 rule table 복사를 금지한다. |
| Matrix 종속 값 소실 | 조건 값 변경/삭제 또는 type 전환 뒤 Matrix rows의 invalid `condition_values`를 normalizer가 조용히 제거한다. | 005에서 proposal preview에 Fieldset/Matrix side effect를 포함하고 006 adapter는 sanitize 전/후 diff를 노출할 후보가 된다. |
| Snapshot authority 불명확 | snapshot을 저장하지만 normalizer/validator는 live analysis_type builder를 사용한다. stale State의 snapshot과 live context가 다르면 표시·질문·검증이 엇갈릴 수 있다. | 005에서 snapshot의 audit-only vs immutable policy를 선택하고 006에서 한 authority만 노출한다. |
| Preview/Word 호환성 | Active Word는 canonical State가 아닌 browser-rendered DOM을 신뢰하고 server validation gate가 없다. 비활성 server Preview renderer는 다른 legacy reads를 가진다. | 005는 Word action 직전 canonical State refresh/readiness 정책을 설계하고, 006은 Word renderer를 복제하지 않는다. |
| Legacy condition/geometry 경계 | 002에서 확인한 legacy chat geometry patch와 official geometry 불일치에 더해, public condition catalog/condition axis도 active card contract와 다르다. | patch path는 official card-instance binding 및 `sanitize_state()` 결과에 맞춰 adapter/migration을 먼저 확정한다. |

# 다음 단계에서 반드시 참고할 내용

## H5-ORCH-005 최소 변경 아키텍처

- `request_ai_agent_h5_v0/condition_fieldsets.py:25-152`: active card, required, Matrix column의 authoritative builder/helper.
- `request_ai_agent_h5_v0/state.py:924-1055, 1223-1269`: canonicalization 및 Fieldset side effect가 발생하는 단일 경계.
- `request_ai_agent_h5_v0/validator.py:262-468`: validation은 normalized active field/Matrix만 소비한다.
- `request_ai_agent_h5_v0/ui.py:1636-1664, 2041-2071` 및 `request_ai_agent_h5_v0/word_export.py:59-121`: actual Preview-to-Word contract.
- 설계 검토 최소 matrix: context/type 전환 시 retained inactive values, normalized Matrix removals, approval 전 State 불변, approval 후 Fieldset·Matrix 재계산, Word 전 readiness/DOM staleness.

## H5-ORCH-006 공통 Field Registry

- `request_ai_agent_h5_v0/schema.py:31-118`와 `constants.py:79-222`: static public field metadata의 adapter source.
- `request_ai_agent_h5_v0/condition_fieldsets.py:17-70, 122-152`: dynamic field definition/instance binding source. `room_temp` 같은 definition key와 `space_environment_1.room_temp` 같은 State instance path를 모두 표현해야 한다.
- `request_ai_agent_h5_v0/state.py:1242-1269`: Registry 소비자가 write한 뒤 반드시 기존 normalizer가 result를 결정한다는 계약.
- `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py:54-77, 145-196`: 일반·조건부 field 및 active Matrix 결과 동일성의 기존 regression anchor.

# 다음 단계 수정이 예상되는 파일

- H5-ORCH-005: `docs/orchestrator_handoff/h5_orch_005_target_architecture.md`.
- H5-ORCH-006: `request_ai_agent_h5_v0/schema.py`, `request_ai_agent_h5_v0/condition_fieldsets.py`, `request_ai_agent_h5_v0/state.py` 및 focused regression test module. 실제 수정 범위는 005 결정 후 최소화해야 한다.
- H5-ORCH-025~028: 기존 `validator.py`, `state.py`, `ui.py`, `word_export.py`를 호출하는 adapter/service와 focused tests. 해당 엔진 자체의 규칙/renderer 변경은 예상하지 않는다.

# 후속 개선 후보

- inactive card values를 canonical State 밖의 audit/retention envelope에 보관할지, 명시적 사용자 확인 후 폐기할지에 대한 설계 및 regression test.
- field definition ID, card instance ID, Matrix column key, legacy public path를 구분하는 adapter DTO.
- Word export 직전 browser DOM과 최신 normalized State의 version/readiness를 비교하는 action-level guard.
- `preview_document.py` legacy renderer의 유지/제거/adapter 여부를 별도 호환성 조사로 결정.

# Roadmap 변경 필요 여부

필요 여부는 Reviewer 판단이 선행되어야 한다. 이 Worker는 Roadmap 상태, 기준 카드, `current_stage.md`, `review_current_stage.md` 또는 다음 단계 프롬프트를 변경하지 않았다. H5-ORCH-003은 Reviewer 검토 대기 상태로 남긴다.

# Git 상태와 Commit 여부

- 이번 단계에서 추가한 파일: `docs/orchestrator_handoff/h5_orch_003_rules_engines_survey.md`.
- 기존 작업 트리에는 Roadmap/current/review prompt 수정, 001·002 문서 및 automation/runs/cache 미추적 항목이 있었으며 수정·stage하지 않았다.
- Commit 여부: 하지 않음. Worker는 Reviewer 검토 전 Roadmap 완료를 확정하지 않는다.

# Worker 보고서

변경 파일은 이 조사 문서 1건뿐이다. 실제 active 조건 규칙은 `condition_fieldsets.py`의 card template/type mapping이며, public `FieldSpec`은 별도 설명 계층임을 확인했다. 대표 `room_temp`는 이슬맺힘/열유동에서 required card field·Matrix column이지만 일반 유동 전환 시 normalizer가 card와 Matrix 값을 제거한다. Validator·draft·final review는 normalized State와 manual Matrix를 재사용한다. 활성 Preview는 browser DOM renderer이고 Word는 그 DOM 직렬화만 받으며, 서버 document-preview는 비활성이다. 검증 명령 결과를 보완한 뒤 Reviewer 검토 대기로 남긴다.
