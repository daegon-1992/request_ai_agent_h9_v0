# h3_v0 실행 인수인계

이 문서는 h3_v0 후속 작업이 이전 단계의 조사·변경·검증 결과를 이어받기 위한 인수인계 문서다. 기존 `docs/codex_handoff.md`는 참고만 했으며 변경하지 않았다.

## Stage 0 — 수정 대상 구조 조사

### 범위와 현 상태

- 조사 대상 프로젝트 루트: `request_ai_agent_h3_v0/`
- 실행 진입점: `Request_AI_Agent_h3_v0.py` → `request_ai_agent_h3_v0.create_app()`
- 서버: Flask, 화면: `request_ai_agent_h3_v0/ui.py` 안의 단일 HTML/CSS/JavaScript 템플릿
- 기능 소스는 수정하지 않았다. 이 Stage에서 새로 만드는 파일은 본 문서뿐이다.
- 상태의 정규 형태는 `state.py:create_initial_state()` 및 `sanitize_state()`가 만든다. 요청마다 `app.py:_derive_state()`가 `validator.py:state_with_validation()`을 호출해 형상 축, 조건 축, Case Matrix, 검증 결과를 파생한다.

상태 흐름은 다음과 같다.

```text
UI collectState()
  → Flask API (/api/input/save, context confirm, recent load 등)
  → state.sanitize_state()
  → geometry_engine.state_with_geometry_axis()
  → condition_engine.state_with_condition_axis()
  → case_matrix.generate_case_matrix_preview()
  → validator.validate_state() / state_with_validation()
  → state + stage_progress + review.validator를 UI에 반환
```

### 1. 의뢰 제목과 사업부/제품군/플랫폼/해석유형 조합

#### 현재 구현 위치

- UI 선택 카드 및 기본 정보/개요 입력: `request_ai_agent_h3_v0/ui.py` 약 450–620행.
  - 조합 입력 DOM ID: `quickBusinessUnitSelect`, `quickProductGroupSelect`, `quickPlatformSelect`, `quickAnalysisTypeSelect`.
  - 안내형 선택도 같은 `requestContextDraft`를 갱신한다.
- UI 조합 의존성 및 확정: `ui.py` 약 900–1210행.
  - 사업부 변경 시 제품군·플랫폼을 비우고, 제품군 변경 시 플랫폼을 비운다.
  - `confirmRequestContext()`가 네 값의 누락을 검사한 뒤 `/api/request-context/confirm`으로 보낸다.
  - 제품군/플랫폼 후보는 `/api/product-hierarchy`에서 받고, `product_hierarchy.py:build_product_hierarchy_payload()`가 제공한다.
- 서버 조합 확정/스냅샷: `app.py:_context_confirm_state()` (214행 부근), `/api/request-context/confirm` (1081행 부근).
  - 필수 조합은 `business_unit`, `product_group`, `platform`, `analysis_type` 네 개다.
  - 확정 시 `condition_fieldset_snapshot`, `condition_fieldset_key`, `operation_mode`, `context_locked=True`를 `request_context`에 기록한다.
  - 선택한 `analysis_type`은 `analysis_overview.analysis_type`에도 사용자 입력으로 동기화하고, 요청 번호를 발급한다.
- 계층 데이터: `product_hierarchy.py`, 폴백 데이터 `normalized_product_hierarchy.py`.
- 스키마/상태 키: `constants.py:REQUEST_CONTEXT_FIELD_DEFS`, `state.py:default_request_context()` 및 `sanitize_state()`.

#### 제목의 실제 동작

- 독립적인 `request_title` 상태 필드나 화면 입력은 현재 없다.
- 최근 의뢰 목록 제목은 `recent_store.py:recent_title()`이 `state.py:compose_request_title()`을 우선 사용하고, 없으면 해석유형·배경·목적·프로젝트명 순으로 파생한다.
- 브라우저도 `ui.py:recentTitle()`/`generatedRequestTitle()`로 같은 목적의 제목을 만들어 `/api/recent/save`에 전달한다. 서버는 다시 `recent_store.py` 기준으로 저장한다.
- Word 제목은 `word_export.py:_fill_template_tables()`에서 `해석 의뢰서 – {해석유형} {의뢰번호}`로 별도 생성한다.

#### 후속 수정 시 주의

- 제목을 새 입력값으로 만들려면 UI, `constants.py`, `schema.py`, `state.py` 정규화·마이그레이션, `recent_store.py`, `word_export.py`, 미리보기/초안 계열까지 함께 결정해야 한다. 최근 목록 제목과 Word 제목을 무심코 같은 필드로 바꾸지 말 것.
- `basic_info.division`(의뢰자 소속 사업부)와 `request_context.business_unit`(제품 사업부)는 의미와 검증 경로가 다르므로 합치지 말 것.
- 조합 변경은 기존 조건 스냅샷과 값의 호환성을 깨뜨릴 수 있다. UI에는 변경 경고와 lock 해제 흐름이 있으므로, 변경 작업은 `context_locked`, snapshot 재생성, 기존 조건값 보존/정리 정책을 함께 검토할 것.

### 2. 단계별 진행률

#### 현재 구현 위치와 계산

- 서버의 기준 계산: `app.py:_stage_progress()` (302행 부근).
  - 단계 순서: `analysis_overview`, `geometry`, `conditions`.
  - 개요: `ANALYSIS_OVERVIEW_SPECS`의 모든 필드를 `status == provided` 및 값 존재 여부로 계산한다.
  - 형상: 제품 입력 + 변경부품 여부 확정이 기본 2개이며, 변경 있음이면 기준 부품 + 변경 부품을 추가해 총 4개로 계산한다.
  - 조건: context가 확정되지 않으면 `request_context` 하나를 미완료로 표시한다. 확정되면 `get_active_condition_fields()`의 필수 필드만 분모·분자로 계산한다.
  - 응답에는 각 단계의 `filled_count`, `total_count`, `completion_percent`, `missing_fields`, `is_complete`와 전체 `remaining_stages`가 포함된다.
- UI 렌더링과 즉시 표시: `ui.py:sectionProgress()`/`renderStageProgress()` (1794행 부근).
  - UI도 자체 산식을 갖고 있어, 서버와 조건부 변경부품·선택 조건 처리 방식이 어긋나지 않게 함께 수정해야 한다.
- 알림/챗 흐름: `app.py:_progress_notifications()`, `_stage_completion_message()`.

#### 후속 수정 시 주의

- 진행률 정의를 바꾸면 서버 산식과 UI 산식을 동시에 바꾸고, `/api/bootstrap` 및 모든 저장/미리보기 응답의 `stage_progress` 계약을 유지할 것.
- 개요 진행률은 실제 제출 필수 여부가 아니라 모든 개요 필드의 입력 상태를 본다. validator의 required 규칙과 의도적으로 다를 수 있으므로, 요구사항에 따라 둘을 통일할지 별도로 정해야 한다.

### 3. 제품 및 변경 부품 입력

#### 현재 구현 위치와 상태

- UI: `ui.py` 약 580–605행의 `productRows`, `hasChangedPart`, `changedFromPartModeling`, `changedFromPartDescription`, `partRows` 및 행 추가/삭제 처리(약 2430행 이후).
- UI 직렬화: `ui.py:collectState()` (1660행 부근).
  - `geometry.products`, `geometry.parts`는 다중 값 행이다.
  - `geometry.has_changed_part`는 체크박스 값, `geometry.changed_from_part`는 `{modeling_no, description}` 구조로 보낸다.
- 상태 정규화: `state.py:create_initial_state()` 및 `sanitize_state()`.
  - `geometry.products`, `geometry.parts`는 `sanitize_geometry_rows()`의 값 행.
  - `changed_from_part`는 모델링 번호와 설명을 포함하는 geometry entry.
- 파생 축: `geometry_engine.py:generate_geometry_axis()`/`state_with_geometry_axis()`.
  - 변경부품이 있으면 제품/기준부품/변경부품 조합으로 geometry variant와 baseline 정보를 만든다.
- 검증: `validator.py:_validate_geometry()` (199행 부근).
  - 제품은 최소 1개 필요, 제품/부품/기준부품 모델링 번호는 영문·숫자·하이픈 형식 검사.
  - 변경부품 여부 미확정은 warning, 변경 있음인데 변경 부품이 없으면 blocking, 기준 부품은 warning.
  - 기준 부품이 있는 변경부품 의뢰에서 Case Matrix baseline이 빠지면 `case_matrix.baseline_missing` blocking.

#### 후속 수정 시 주의

- `changed_from_part`는 단순 문자열이 아니라 `{modeling_no, description}`을 수용하는 상태이다. UI와 `state.py`의 정규화 계약을 깨지 말 것.
- Case Matrix와 validator는 products/parts의 다중 행을 전제로 한다. 단일 값으로 축소하거나 새 행 구조를 도입하면 `geometry_engine.py`, `case_matrix.py`, `chat_patch.py`, `draft_pipeline.py`도 영향권이다.

### 4. 해석조건 UI, 해석유형별 분기, 운전 조건

#### 현재 구현 위치와 상태

- 조건 UI 뼈대: `ui.py` 약 606행의 `conditionFields`; 동적 렌더링·수집은 `renderConditionFields()`, `collectConditionFields()`, `collectConditionValues()`, `collectConditionOptions()` (약 1378–1610행).
- 해석유형 선택:
  - 드롭다운과 추천 UI: `ui.py:setupAnalysisTypes()`, `selectAnalysisType()` (2246행 부근).
  - API: `app.py:/api/analysis-type/select`; 로직: `analysis_type_recommender.py:apply_analysis_type_selection()`.
- 조합 확정에 따른 조건 fieldset: `condition_fieldsets.py:build_condition_fieldset()` (404행 부근).
  - 해석유형별 그룹 사양은 `ANALYSIS_TYPE_GROUP_SPECS`(약 76행 이후): 이슬맺힘, 일반 유동, 열유동, 열교환기 유속 프로파일, 기류 도달 거리, PDB.
  - 확정 fieldset 그룹은 `request_context.condition_fieldset_snapshot`으로 저장하며 `get_active_condition_fields()`가 그 snapshot과 `conditions.condition_options`로 실제 활성 필드를 복원한다.
- 운전 조건(운전 모드):
  - `request_context.operation_mode`, UI 갱신 함수 `ui.py:updateOperationMode()`, API `/api/request-context/fieldset`.
  - `condition_fieldsets.py`의 일체형 제품군(`PRODUCT_GROUP_INTEGRATED = "일체형"`)에서만 실내/실외/동시운전 분기를 한다.
  - 동시운전은 `SIMULTANEOUS_FIELD_MAPS`로 필드를 실내/실외 키로 복제한다. 실내/실외 단일 운전도 대응 키로 치환한다.
- 조건 축: `condition_engine.py:split_condition_fields()`, `generate_condition_axis()`, `state_with_condition_axis()`.
- 조건 추천: `analysis_type_recommender.py:condition_recommendation_payload()` 및 `/api/conditions/recommend`.

#### 후속 수정 시 주의

- 조건 목록의 단일 진실원은 확정 시점 snapshot이다. `CONDITION_FIELD_DEFS`만 변경하면 이미 확정된 문서와 `get_active_condition_fields()` 결과가 바뀌지 않을 수 있다.
- 해석유형 명칭/별칭 변경은 `constants.py:ANALYSIS_TYPE_OPTIONS`, `analysis_type_recommender.py`, `condition_fieldsets.py`의 정규화·사양을 함께 맞춰야 한다.
- `EXCLUDED_LEGACY_FIELD_KEYS`는 legacy 입력을 활성 fieldset/검증에서 제외한다. 제거 또는 복원 시 상태 마이그레이션과 validator 조건을 먼저 확인할 것.
- 운전 모드 selector의 표시·이벤트 위치와 fieldset 재생성은 분리되어 있다. UI만 고치면 서버 snapshot이 갱신되지 않으며, 서버만 고치면 화면에 새 필드가 나오지 않는다.

### 5. 저장/불러오기 및 유효성 검사

#### 현재 구현 위치와 흐름

- 임시 저장: UI `ui.py:saveStateToServer()` → `POST /api/input/save` → `app.py:save_input()`.
  - 현재 서버 상태는 Flask `app.config[STATE_STORE_KEY]`에 보관한다. 저장은 `_derive_state()`로 정규화·파생·검증 후 반영한다.
- 미리보기 갱신: `POST /api/preview`; 저장과 같은 파생 흐름이지만 서버 상태를 저장하지 않는다.
- 최근 의뢰 영속화: UI `saveRecent()`/`loadRecent()`/`deleteRecent()` ↔ `app.py:/api/recent*` ↔ `recent_store.py`.
  - `recent_store_path()`의 JSON에 최근 상태 전체를 저장한다.
  - 불러오기는 `sanitize_state()` 후 `_derive_state()`를 다시 실행하므로 파생 데이터는 복원본이 아니라 현재 로직으로 재생성된다.
  - UI는 해석유형과 요청 번호가 있을 때만 최근 저장을 시도한다.
- 검증: `validator.py:validate_state()` 및 `state_with_validation()`.
  - 필수 기본정보/개요, 형상, context lock, 활성 조건 필수값, 축 존재, Case Matrix 계약/포함 case를 검사한다.
  - 결과는 `review.validator`, `review.submission`, `metadata.issue_registry`에 반영된다.
- 최종 제출: `app.py:/api/submit`에서 validator 결과의 `can_submit`을 기준으로 처리한다.

#### 후속 수정 시 주의

- 저장 API는 클라이언트가 보낸 전체 state를 신뢰하지 않고 `sanitize_state()`로 허용 키만 복원한다. 새 상태 필드는 `state.py` 정규화에 넣지 않으면 저장 후 사라진다.
- `save_input`은 최근 목록 영속 저장과 다르다. “저장”의 의미를 변경할 경우 두 경로를 혼동하지 말고 API/UX 정책을 명시할 것.
- 검증 대상이나 required 조건을 바꾸면 진행률, 조건 fieldset, Case Matrix 생성 가능 여부와 제출 gating을 함께 회귀 검사할 것.

### 6. h2_v2 관련 구현 위치

h2_v2는 상위 형제 프로젝트 `../request_ai_agent_h2_v2/request_ai_agent_h2_v2/`에 있다. 다음 파일들이 h3_v0의 직접적인 선행 구현이다.

| 관심사 | h2_v2 위치 | h3_v0 대응 위치 | 비교 시 유의점 |
| --- | --- | --- | --- |
| Flask API·context confirm·진행률·recent API | `app.py` | `app.py` | 구조가 매우 유사하나 행 입력 및 최신 fieldset 규칙 차이를 확인할 것 |
| 화면 템플릿·조합 카드·동적 조건 UI | `ui.py` | `ui.py` | h2_v2의 geometry 수집/행 렌더링 표현이 h3_v0와 다를 수 있음 |
| 상태 정규화·legacy migration | `state.py` | `state.py` | h3_v0는 `changed_from_part`의 모델링 번호/설명 구조와 legacy 제외 규칙을 재확인할 것 |
| 조건 fieldset·운전 분기 | `condition_fieldsets.py` | `condition_fieldsets.py` | h3_v0 builder version과 catalog/통합 제품군 분기 기준을 우선할 것 |
| 제품 hierarchy | `product_hierarchy.py`, `normalized_product_hierarchy.py` | 같은 파일명 | 데이터 파일/폴백 값 차이를 무단 복사하지 말 것 |
| 형상·조건 축 및 Case Matrix | `geometry_engine.py`, `condition_engine.py`, `case_matrix.py` | 같은 파일명 | products/parts 다중 행과 baseline 포함 규칙을 확인할 것 |
| validator | `validator.py` | `validator.py` | h3_v0의 최신 blocking/warning 계약과 issue path를 보존할 것 |
| recent 저장 | `recent_store.py` | `recent_store.py` | 제목 생성과 저장 경로를 h3_v0 쪽 기준으로 유지할 것 |
| 제목 출력 | `word_export.py`, `preview_document.py` | 같은 파일명 | 제목 필드 도입 시 목록 제목과 문서 제목을 구분할 것 |

### Stage 0 이후 권장 작업 순서

1. 요구사항별 상태 계약(새 필드 여부, 제목의 소유자, 조합 변경 시 값 보존 정책)을 먼저 확정한다.
2. 상태/상수/스키마와 정규화·마이그레이션을 바꾼다.
3. Flask context·저장·진행률·검증·파생 축을 같은 상태 계약에 맞춘다.
4. UI 렌더링·수집·이벤트와 문서/최근 목록 출력을 맞춘다.
5. h3_v0 테스트를 추가 또는 갱신하고, `python tools/check_encoding.py --changed` 및 `git diff --check`를 실행한다.

### Stage 0 검증 기록

- 코드 변경: 없음.
- 문서 변경: `docs/h3_v0_execution_handoff.md` 신규 생성.
- 조사 시 `docs/codex_handoff.md`를 읽었으며 덮어쓰지 않았다.
- 후속 단계에서는 이 문서를 먼저 읽고, 완료한 Stage·변경 파일·검증·커밋 정보를 이어서 기록한다.

## Stage 1 표시/UI 정리

### 변경 파일

- `request_ai_agent_h3_v0/ui.py`
- `request_ai_agent_h3_v0/app.py`
- `docs/h3_v0_execution_handoff.md`

### 변경 내용

- `양산 모델 번호(Model Suffix)`를 `양산 모델 (Model Suffix)`로, `해석 대상 제품`을 `제품`으로 변경했다.
- 제출 결과 표기를 `의뢰서 상태: OK / NG`로 통일했다. OK/NG 판정과 제출 가능 여부 산출 로직은 변경하지 않았다.
- 의뢰 제목 아래 안내 문구와 해석조건의 조건 입력 예시 문구를 제거했다.
- select의 빈값 placeholder를 숨김·비활성 option으로 처리해 목록의 실제 선택 항목으로 노출되지 않게 했다.

### 검증 결과

- `python tools/check_encoding.py --changed`: 통과
- `git diff --check`: 통과
- `python -m py_compile request_ai_agent_h3_v0/ui.py request_ai_agent_h3_v0/app.py`: 통과
- UI 정적 점검(표시 문구·조건 예시 제거·숨김 placeholder): 통과
- `python -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 미실행. 현재 환경에 `pytest`와 Flask가 없어 의존성 import 단계에서 중단됨.

### 남은 이슈 및 다음 단계 주의사항

- 남은 기능 이슈는 확인되지 않았다. 다만 의존성 설치 후 기존 최소 회귀 테스트를 실행할 것.
- select placeholder는 표시 전용이며 실제 옵션으로 선택되거나 상태값으로 저장되지 않아야 한다.
- OK/NG 판정 기능, 상태 계약, validator 및 제출 gating 로직은 변경하지 말 것.

## Stage 2 의뢰 제목 및 조합 변경 UI

### 변경 파일

- `request_ai_agent_h3_v0/ui.py`
- `docs/h3_v0_execution_handoff.md`

### 변경 내용

- 의뢰 제목을 `사업부 / 제품군 / Platform / 해석유형` 순서로 표시하도록 변경했다.
- 제목 우측의 해석유형 선택 입력을 제거하고, 조합이 확정된 경우에만 표시되는 `변경` 버튼을 제목 우측에 배치했다.
- 해석 진행률 아래의 `조합 확인` 버튼과 조합 요약 바의 `변경` 버튼을 제거했다. 조합 확정은 기존 `이 조합으로 의뢰서 작성 시작` 버튼으로 유지했다.
- 제목 우측 `변경` 버튼은 기존 변경 확인 모달과 `continueContextChange()` 흐름을 그대로 사용한다. 따라서 lock 해제 후 네 조합을 다시 선택할 수 있고, 기존 해석조건 입력값 보존 정책도 변경하지 않았다.
- 제품, 진행률, 해석조건 로직은 수정하지 않았다.

### 조합 재선택 흐름 확인

1. 조합 확정 후 제목에 사업부, 제품군, Platform, 해석유형이 순서대로 표시된다.
2. 제목 우측 `변경`을 누르면 기존 변경 확인 모달이 열린다.
3. `변경 계속`을 누르면 기존 조합 값이 선택 카드에 유지된 채 context lock만 해제되어 네 항목을 다시 선택할 수 있다.
4. 조합을 다시 확정하면 기존 조건값을 포함한 state를 `/api/request-context/confirm`으로 전송하므로 기존 데이터 유지 정책을 따른다.

### 검증 결과

- `python -m py_compile request_ai_agent_h3_v0/ui.py`: 통과
- `python tools/check_encoding.py --changed`: 통과
- `git diff --check`: 통과
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (5 passed)
- Flask API 재선택 흐름 확인 스크립트: 통과. 조합 확정 후 `변경`으로 재선택한 Platform 값을 다시 확정했고, 기존 `conditions.condition_values.fan_rpm` 값이 유지됨을 확인했다.

## Stage 3 의뢰서 단계별 진행률 계산

### 변경 파일

- `request_ai_agent_h3_v0/app.py`
- `request_ai_agent_h3_v0/constants.py`
- `request_ai_agent_h3_v0/schema.py`
- `request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`
- `docs/h3_v0_execution_handoff.md`

### 진행률 산정 대상

- 해석 개요는 `ANALYSIS_OVERVIEW_FIELD_DEFS`의 `track_progress=True` 필드만 센다. 현재 대상은 `project_name`, `grade`, `npi_stage`, `model_suffix`, `analysis_type`, `background`, `purpose`, `goal`, `deliverables`의 9개다.
- `analysis_type`은 조합 선택 UI에서 사용자 선택값으로 표시되므로 포함한다. `pms_group`, `analysis_overview.platform`은 현재 해석 개요 입력 UI에 없으므로 제외한다.
- `request_date`와 `due_date`(희망 완료일)는 화면에 표시되더라도 진행률 대상에서 명시적으로 제외한다.
- 형상/모델 정보와 해석조건의 대상 구성(제품, 부품 변경 여부, 활성 필수 조건)은 변경하지 않았다. 다만 기존 대상 값도 아래 사용자 입력 판정을 통과해야 완료로 센다.

### 기본값 및 향후 필드 처리 방식

- 완료 판정은 값이 비어 있지 않고 `status == "provided"`이며 `source == "user"`인 필드에만 적용한다. 따라서 `system`, `legacy_internal` 등 사용자가 직접 입력하지 않은 기본값·초기값은 완료 수에 포함되지 않는다.
- 행 목록(제품/부품/조건 값)도 같은 판정을 사용한다. UI 구조나 제품·부품·해석조건의 표시·입력 방식은 수정하지 않았다.
- `FieldSpec.track_progress`는 기본값이 `False`인 opt-in 메타데이터다. 이후 해석 개요의 화면 입력 필드를 추가할 때만 해당 필드 정의에 `track_progress=True`를 넣고, 자동 기본값은 기존처럼 `source="system"`으로 기록하면 동일한 원칙이 적용된다.

### 검증 결과

- 빈 의뢰서: 해석 개요 `0/9 (0%)`, 형상/모델 정보 `0/2`; 시스템 요청일은 완료에 포함되지 않음을 확인했다.
- 일부 입력 의뢰서: 시스템 기본 프로젝트명과 사용자 입력 해석 목적을 함께 넣어 해석 개요 `1/9 (11%)`만 집계됨을 확인했다.
- 실제 필수값 입력 의뢰서: 해석 개요 `4/9 (44%)`(해석 유형·Model Suffix·목적·목표), 형상/모델 정보 `2/2`, 해석조건 `2/2`를 확인했다.
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (6 passed)
- `..\.venv\Scripts\python.exe -m py_compile request_ai_agent_h3_v0/app.py request_ai_agent_h3_v0/schema.py request_ai_agent_h3_v0/constants.py request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과

## Stage 4 제품 입력 영역

### 변경 파일

- `request_ai_agent_h3_v0/ui.py`
- `request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`
- `docs/h3_v0_execution_handoff.md`

### 변경 내용

- 형상/모델 정보 안의 해석 대상 영역 명칭을 `제품`으로 유지하고, 테두리가 있는 단일 제품 입력 영역으로 구성했다.
- 제품의 각 행은 `도면번호(NPDM MCAD)`와 `설명(Description)` 입력칸 및 행 우측의 `+`/`-` 버튼으로 구성했다.
- `+`는 해당 행 다음에 빈 제품 행을 추가하고, `-`는 클릭한 제품 행 전체를 삭제한다. 모든 행이 삭제된 경우에도 빈 상태에서 `+`로 다시 추가할 수 있다.
- 제품 행 수와 두 입력값은 `geometry.products`에 수집되어 임시 저장, 최근 의뢰 저장, 상태 정규화 및 기존 도면번호 유효성 검사에 반영된다.
- 이번 단계에서는 부품 입력 영역을 구현하지 않았으며, 기존 저장 데이터의 부품 관련 상태는 제품 입력 저장 시 보존한다.

### 검증 결과

- 제품 2행(유효 행 + 잘못된 도면번호 행)을 `/api/input/save`로 저장해 도면번호와 설명이 모두 보존되고 도면번호 유효성 검사 오류가 발생하는 것을 확인했다.
- 두 번째 제품 행을 삭제한 상태로 다시 저장해 삭제 행이 저장 상태에서 제거되고, 삭제된 행의 유효성 검사 오류도 사라지는 것을 확인했다.
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (7 passed)

## Stage 5 변경 부품 있음 및 기존 부품(Base) 입력 영역

### 변경 파일

- `request_ai_agent_h3_v0/ui.py`
- `request_ai_agent_h3_v0/state.py`
- `request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`
- `docs/h3_v0_execution_handoff.md`

### 변경 내용

- 제품 입력 영역 아래에 `변경 부품 있음` 체크와 `기존 부품(Base)` 하위 영역을 추가했다.
- 체크 해제 상태에서는 기존 부품 영역의 도면번호, 설명, 행 추가·삭제 버튼을 모두 입력 불가 상태로 표시한다. 체크하면 해당 영역을 즉시 활성화한다.
- 기존 부품(Base)은 `도면번호(NPDM MCAD)`와 `설명(Description)`의 반복 행 및 각 행 우측 `+`/`-` 버튼을 제공한다. 행 추가는 해당 행 다음에 빈 행을 삽입하고, 행 삭제는 해당 행만 제거한다.
- 기존 부품 반복 행은 새 `geometry.base_parts`에 제품 행과 독립적으로 저장한다. 첫 번째 Base 행은 기존 `geometry.changed_from_part`에도 동기화해 기존 검증 및 파생 로직과 호환되도록 유지했다.
- 기존 `geometry.parts` 및 변경 부품(Variant) UI는 이번 단계에서 구현하거나 노출하지 않았다.

### 검증 결과

- 체크 해제 상태의 Base 영역은 `disabled` 입력·버튼으로 렌더링되고, 체크 시 활성화되는 UI 경로를 정적 회귀 테스트로 확인했다.
- 기존 부품 2행 저장 후 1행 삭제와 체크 해제를 순서대로 저장해, 삭제 행만 제거되고 남은 기존 부품 데이터는 보존되는 것을 API 회귀 테스트로 확인했다.
- 제품 데이터가 기존 부품 데이터와 독립적으로 저장되는 것을 API 회귀 테스트로 확인했다.
- `..\.venv\Scripts\python.exe -m py_compile request_ai_agent_h3_v0/ui.py request_ai_agent_h3_v0/state.py request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (8 passed)

## Stage 6 변경 부품(Variant) 입력 영역

### 변경 파일

- `request_ai_agent_h3_v0/ui.py`
- `request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`
- `docs/h3_v0_execution_handoff.md`

### 변경 내용

- 부품 영역의 두 번째 하위 영역으로 `변경 부품(Variant)`을 추가했다.
- Variant는 기존 부품(Base)과 동일하게 도면번호(NPDM MCAD), 설명(Description)의 반복 입력 행과 각 행의 `+`/`-` 버튼을 제공한다.
- `변경 부품 있음` 체크 상태에 따라 Base와 Variant 입력 영역 및 행 조작 버튼을 함께 활성화 또는 비활성화한다.
- Variant 입력 행은 `geometry.parts`에서 직접 수집·저장하고, 제품은 `geometry.products`, Base는 `geometry.base_parts`에 각각 유지한다. Base 첫 행의 기존 `changed_from_part` 호환 동기화는 보존했다.

### 검증 결과

- 제품, Base, Variant에 각각 두 행의 독립 데이터를 저장한 뒤 각 영역의 두 번째 행을 삭제하여, 남은 행과 다른 두 영역의 데이터가 보존되는 것을 API 회귀 테스트로 확인했다.
- `변경 부품 있음`을 해제한 뒤에도 Base와 Variant의 저장 데이터는 유지되고 UI 입력 영역만 비활성화되는 기존 동작을 확인했다.
- `..\.venv\Scripts\python.exe -m py_compile request_ai_agent_h3_v0/ui.py request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (8 passed)

## Stage 7 해석조건 상위·하위 항목 구조

### 변경 파일

- `request_ai_agent_h3_v0/constants.py`
- `request_ai_agent_h3_v0/condition_fieldsets.py`
- `request_ai_agent_h3_v0/state.py`
- `request_ai_agent_h3_v0/ui.py`
- `request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`
- `docs/h3_v0_execution_handoff.md`

### 변경 내용

- 해석조건 입력을 다음 다섯 상위 항목과 하위 항목으로 재구성했다.
  - `운전 조건`: `팬 회전수(Fan RPM)`(`fan_rpm`), `운전 풍량(CMM)`(`airflow`)
  - `부품 사양`: `열교환기 사양`(`heat_exchanger_spec`)
  - `온·습도 조건`: `취출 온도`(`heat_exchanger_temp`), `취출 상대습도`(`heat_exchanger_rh`), `공간 온도`(`room_temp`), `공간 상대습도`(`room_rh`)
  - `설치 환경`: `설치 환경`(`installation_space`), `제품 설치 위치`(`installation_location`)
  - `결과 요청`: `결과 확인 항목`(`postprocess`), `기류 도달 기준 거리`(`postprocess_air_speed`)
- `condition_fieldsets.py:CONDITION_INPUT_GROUP_SPECS`가 상위·하위 입력 구조의 단일 진실원이다. 해석유형별 기존 필수 여부는 보존하고, 해당 해석유형에서 기존에 쓰지 않던 항목은 선택 입력으로 같은 위치에 배치했다.
- `conditions.input_structure`를 초기 상태와 `sanitize_state()` 결과에 항상 포함했다. 구조는 `version`, `groups`, `pending_behaviors`로 구성하며, 클라이언트가 보낸 임의 구조는 신뢰하지 않고 서버의 정규 구조로 복원한다.
- `pending_behaviors`에는 `cmm_rpm_single_selection`, `temperature_humidity_toggle`, `heat_exchanger_default`를 모두 `not_implemented`로 기록했다. 이번 단계에서는 세 상세 동작을 구현하지 않았다.
- UI는 각 상위 항목을 조건 그룹 카드로 렌더링하고, 카드 머리글에 `상위 항목` 표식을 추가했다. 기존 다중 조건값 입력, 운전 구분, 저장·검증 경로는 유지했다.

### 다음 단계 구현 시 주의사항

- CMM/RPM 단일 선택은 `fan_rpm`과 `airflow`의 값을 삭제하거나 서로 덮어쓰지 말고, 선택 상태를 별도 `conditions.condition_options` 키로 관리한 뒤 활성 필드·validator·Case Matrix에 같은 규칙을 적용할 것.
- 온·습도 토글도 `heat_exchanger_temp`, `heat_exchanger_rh`, `room_temp`, `room_rh`의 기존 값을 보존해야 한다. 토글 해제는 입력 UI와 required 판정만 제어하고 저장값을 제거하지 않는 정책을 먼저 확정할 것.
- 열교환기 기본값은 `source="system"`으로 기록해 Stage 3의 사용자 입력 진행률 원칙을 지켜야 한다. 기본값이 제출 필수값을 자동으로 충족하는지 여부는 validator와 진행률에서 별도로 결정할 것.
- 확정된 의뢰는 `request_context.condition_fieldset_snapshot`을 사용한다. 구조·필수 규칙을 바꿀 때는 신규 조합 확정뿐 아니라 기존 snapshot, `get_active_condition_fields()`, `condition_engine.py`, validator, Case Matrix를 함께 회귀 검사할 것.

### 검증 결과

- `..\.venv\Scripts\python.exe -m py_compile request_ai_agent_h3_v0/constants.py request_ai_agent_h3_v0/condition_fieldsets.py request_ai_agent_h3_v0/state.py request_ai_agent_h3_v0/ui.py request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (9 passed)

## Stage 7-보정 최종 Fieldset 정의 적용

### 변경 파일

- `request_ai_agent_h3_v0/condition_fieldsets.py`
- `request_ai_agent_h3_v0/ui.py`
- `request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`
- `docs/h3_v0_execution_handoff.md`

### 기존 Stage 7과 달라진 사항

- 기존 Stage 7은 공통 상위 항목 아래에 해석유형에서 사용하지 않는 조건도 선택 입력으로 노출했다. 보정 후에는 해석유형별 active fieldset에 정의된 조건만 snapshot, UI, `get_active_condition_fields()`에 포함한다.
- 최종 active fieldset은 다음과 같이 확정했다.
  - `열교환기 유속 프로파일`, `일반 유동 해석`: `fan_rpm`, `heat_exchanger_spec`
  - `PDB`: `airflow`, `heat_exchanger_temp`, `room_temp`, `installation_space`, `installation_location`, 기존 `postprocess` key의 화면 표기 `유선 표기`
  - `기류 도달 거리`: `airflow`, `fan_rpm`, `heat_exchanger_spec`, `heat_exchanger_temp`, `room_temp`, `installation_space`, `installation_location`, 기존 `postprocess_air_speed` key의 화면 표기 `기류 도달 기준 속도`; 상대습도 두 key는 포함하지 않는다.
  - `이슬맺힘`: `fan_rpm`, `heat_exchanger_spec`, `heat_exchanger_temp`, `heat_exchanger_rh`, `room_temp`, `room_rh`
  - `열유동 해석`: `fan_rpm`, `heat_exchanger_spec`, `heat_exchanger_temp`, `room_temp`
- 공통 입력 그룹의 `온·습도 조건` 표기를 `온도 조건`으로 보정했다. 이슬맺힘에서 상대습도 key 자체는 계속 active fieldset에 포함한다.
- 각 fieldset field에 `required_level`, `conditional_group`, `priority`, `unit`, `input_guidance`를 기록했다. 기류 도달 거리의 `airflow`와 `fan_rpm`은 `conditional_required`, 동일한 `reach_airflow_or_fan_rpm` 그룹이며 풍량의 우선순위를 더 높게 설정했다. 두 값은 현 단계에서 삭제·상호 덮어쓰기 없이 보존한다.
- UI는 `required_level=conditional_required`를 `조건부 필수`로 표시하고, 기류 도달 거리의 풍량 우선/팬 회전수 대체 입력 안내를 표시한다.
- 일체형 제품군의 실내/실외/동시운전 key 치환·복제 구조는 유지했다. 해석유형 fieldset을 먼저 만들고 그 결과에만 운전 분기를 적용한다.

### 다음 단계 주의사항

- 이번 보정에서는 `validator`, 진행률, 제출 payload, Case Matrix의 최종 제외·조건부 충족 규칙을 구현하지 않았다. 다음 단계에서 active fieldset의 `required_level`을 단일 판단 기준으로 사용해야 한다.
- `reach_airflow_or_fan_rpm`은 둘 중 하나의 사용자 입력이 있으면 충족으로 처리하되, 둘 다 있을 때 어느 값도 제거하거나 덮어쓰지 않아야 한다. 진행률, validator, 제출 payload, Case Matrix에 같은 규칙을 적용할 것.
- 기존에 확정된 요청은 `condition_fieldset_snapshot`을 사용한다. 최종 정의를 적용하려면 해당 조합을 다시 확정해 새 snapshot을 생성해야 하며, 기존 저장 조건값은 보존 정책을 별도로 검토할 것.

### 검증 결과

- `..\.venv\Scripts\python.exe -m py_compile request_ai_agent_h3_v0/condition_fieldsets.py request_ai_agent_h3_v0/ui.py request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (9 passed)
- 회귀 테스트에서 7개 해석유형별 active fieldset과 `get_active_condition_fields()`의 표시 대상, PDB/기류 도달 거리 화면 label, 조건부 필수 메타데이터, 일체형 동시운전 key 복제를 확인했다.

## Stage 8 해석조건 validator active fieldset 적용

### 변경 파일

- `request_ai_agent_h3_v0/validator.py`
- `request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`
- `docs/h3_v0_execution_handoff.md`

### validator 규칙

- validator는 `get_active_condition_fields(state)`가 반환한 확정 fieldset snapshot의 활성 필드만 검사한다. 따라서 active fieldset에 없는 key는 제출 차단 대상이 아니다.
- `required_level="required"`은 값이 하나도 없으면 기존 `conditions.{key}.required_missing` blocking 오류를 만든다.
- `required_level="conditional_required"`은 같은 `conditional_group`별로 묶어 하나 이상의 값이 있을 때 충족으로 처리한다. 기류 도달 거리의 `reach_airflow_or_fan_rpm`은 `airflow` 또는 `fan_rpm` 중 하나 이상이면 충족하고, 둘 다 비었을 때만 `conditions.reach_airflow_or_fan_rpm.conditional_required_missing` blocking 오류를 만든다. 두 값이 모두 있어도 오류를 만들지 않으며 값을 변경하거나 제거하지 않는다.
- `required_level="optional_non_blocking"`은 값이 없어도 validator 오류를 만들지 않는다. 기류 도달 거리의 `heat_exchanger_temp`, `room_temp`가 이에 해당한다.
- `required_level`이 없는 기존 snapshot은 호환성을 위해 기존 `required` boolean을 기준으로 `required` 또는 `optional_non_blocking`으로 해석한다.
- UI 배치, 진행률, 제출 payload, Case Matrix는 변경하지 않았다.

### 검증 결과

- PDB: 6개 active required key를 각각 누락하면 제출 NG를 확인했다.
- 기류 도달 거리: `airflow`만, `fan_rpm`만, 둘 다 입력한 경우 모두 제출 OK를 확인했다. 둘 다 없으면 제출 NG를 확인했다.
- 기류 도달 거리: `heat_exchanger_temp`, `room_temp`를 입력하지 않아도 제출 OK를 확인했다. active fieldset에 없는 `heat_exchanger_rh`, `room_rh`는 validator 대상이 아니다.
- 이슬맺힘: `heat_exchanger_temp`, `heat_exchanger_rh`, `room_temp`, `room_rh` 각각 누락 시 제출 NG를 확인했다.
- 열유동 해석: `heat_exchanger_temp`, `room_temp` 각각 누락 시 제출 NG를 확인했다.
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (10 passed)

### 다음 단계 API 및 주의사항

- validator/제출 결과는 `review.validator.blocking` 및 `/api/submit`의 `final_review.blocking_reasons`에서 issue code로 확인할 수 있다. 조건부 그룹 미충족 code는 `conditions.{conditional_group}.conditional_required_missing` 형식이다.
- 조건 검증의 유일한 입력 범위는 확정 시 저장된 `request_context.condition_fieldset_snapshot`이다. fieldset 정의를 변경한 뒤에는 조합을 다시 확정해 새 snapshot을 생성해야 새 규칙이 적용된다.
- 진행률, 제출 payload, Case Matrix는 아직 `required_level`의 조건부/비차단 의미를 적용하지 않았으므로, 후속 변경 시 validator와 독립적인 기존 계약을 함께 검토해야 한다.

## Stage 9 해석조건 진행률 active fieldset 적용

### 변경 파일

- `request_ai_agent_h3_v0/app.py`
- `request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`
- `docs/h3_v0_execution_handoff.md`

### 진행률 계산 대상 및 방식

- 해석조건 진행률은 확정된 `request_context.condition_fieldset_snapshot`에서 `get_active_condition_fields()`가 반환한 active fieldset만 계산 대상으로 사용한다. fieldset 밖의 항목은 진행률에 포함하지 않는다.
- `required_level="required"` 항목은 필수 진행률 1건으로 계산한다. `required_level`이 없는 기존 snapshot은 기존 `required` boolean을 기준으로 `required` 또는 `optional_non_blocking`으로 해석해 호환성을 유지한다.
- `required_level="conditional_required"` 항목은 `conditional_group` 단위로 1건만 계산한다. 기류 도달 거리의 `reach_airflow_or_fan_rpm`은 `airflow` 또는 `fan_rpm` 중 하나 이상의 사용자 입력이면 완료이며, 둘 다 입력해도 중복 완료 처리하지 않는다.
- `required_level="optional_non_blocking"` 항목은 필수 진행률에서 제외한다. 기류 도달 거리의 `heat_exchanger_temp`, `room_temp`와 active fieldset 밖의 `heat_exchanger_rh`, `room_rh`는 진행률에 영향을 주지 않는다.
- Stage 3 원칙을 유지해 `status="provided"`이고 `source="user"`인 사용자 입력만 완료로 센다. 자동 기본값·초기값, 요청일, 희망 완료일, UI 비노출 해석 개요 항목은 완료 처리하지 않는다.

### 확인 결과

- 7개 해석유형을 전환해 진행률 전체 항목 수가 각 active fieldset의 required 항목 및 conditional group 수와 일치함을 확인했다. 기류 도달 거리는 5건(필수 4건 + 운전 조건 그룹 1건), 이슬맺힘은 6건이다.
- 기류 도달 거리에서 `airflow`만 또는 `fan_rpm`만 입력한 경우 모두 운전 조건 그룹이 완료되어 전체 `5/5`가 되는 것을 확인했다.
- 기류 도달 거리에서 선택 온도(`heat_exchanger_temp`, `room_temp`)와 active fieldset 밖의 상대습도 두 항목을 비워도 필수 진행률 및 누락 항목에 영향이 없음을 확인했다.
- 이슬맺힘은 온도·습도 네 항목(`heat_exchanger_temp`, `heat_exchanger_rh`, `room_temp`, `room_rh`)이 모두 진행률에 포함되고, 전체 입력 시 `6/6`이 되는 것을 확인했다.

### 다음 단계 주의사항

- 이번 단계는 진행률 계산만 수정했다. validator, 제출 payload, Case Matrix, UI 구조는 변경하지 않았다.
- fieldset 정의를 변경한 뒤에는 조합을 다시 확정해 snapshot을 재생성해야 새 진행률 규칙이 적용된다. 제출 payload 또는 Case Matrix에 `required_level` 의미를 적용하는 후속 작업에서는 validator와 동일한 active fieldset·conditional group 계약을 별도로 검증할 것.

## Stage 10 제출 payload 및 Case Matrix active fieldset 필터링

### 변경 파일

- `request_ai_agent_h3_v0/condition_engine.py`
- `request_ai_agent_h3_v0/case_matrix.py`
- `request_ai_agent_h3_v0/review_pipeline.py`
- `request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`
- `docs/h3_v0_execution_handoff.md`

### 필터링 위치 및 규칙

- Case Matrix 조건 축의 입력 필터는 `condition_engine.py:split_condition_fields()`에 둔다. `get_active_condition_fields()`가 반환한 확정 fieldset snapshot의 활성 필드만 common/variable 조건 축으로 분해한다.
- `case_matrix.py:_condition_axis_from_state()`는 저장된 과거 축을 재사용하지 않고 현재 state에서 조건 축을 다시 생성한다. 따라서 기존 상태에 남아 있는 비활성 key가 Case Matrix 조건 축으로 되살아나지 않는다.
- 제출 payload용 입력 필터는 `condition_engine.py:state_with_active_submission_conditions()`에 두고 `review_pipeline.py:build_final_review()`가 제출 계약을 만들기 직전에 적용한다. `conditions.fields`, `condition_values`, common/variable 조건, 조건 축, `input_structure`를 값이 있는 active fieldset 항목으로만 복사한다. `optional_non_blocking`은 값이 있을 때만 포함하며 validator의 제출 차단 규칙은 변경하지 않았다.
- 기류 도달 거리의 `heat_exchanger_temp`, `room_temp`는 값이 있을 때만 제출 payload 및 Case Matrix에 포함한다. `heat_exchanger_rh`, `room_rh`는 기존 상태에 값이 남아 있어도 active fieldset 밖이므로 어느 경로에도 포함하지 않는다.
- 기류 도달 거리에서 `airflow`와 `fan_rpm`이 모두 입력된 경우 두 key를 모두 조건 축 및 제출 payload에 유지한다.

### 검증 결과

- 7개 해석유형 모두에 전체 조건값을 주입해 제출 payload와 Case Matrix 조건 key가 각각의 active fieldset key와 정확히 일치함을 확인했다.
- 기류 도달 거리에서 선택 온도를 비우면 두 온도 key가 제출 payload 및 Case Matrix에서 제외되고, 입력하면 두 key가 포함됨을 확인했다.
- 기류 도달 거리의 상대습도 key 두 개는 값이 있어도 제출 payload와 Case Matrix 조건 축에 포함되지 않음을 확인했다.
- 기류 도달 거리에서 `airflow`와 `fan_rpm`을 함께 입력하면 두 key가 모두 유지됨을 확인했다.
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (13 passed)

### 다음 단계 주의사항

- UI, validator, 진행률 계산은 이번 단계에서 변경하지 않았다. 후속 fieldset 정의 변경 시에도 확정된 `request_context.condition_fieldset_snapshot`을 다시 생성해야 제출 payload와 Case Matrix가 새 규칙을 사용한다.
- 제출 계약은 조건 입력을 필터링하지만 저장 state 자체의 기존 비활성 값은 보존한다. 상태 정리 정책이 필요하면 최근 의뢰 복원 및 legacy migration과의 호환성을 별도 단계에서 검토할 것.
- h2_v2 및 Preview, Word, Export, PPT, 이미지 관련 기능은 수정하지 않았다.

## Stage 11 기류 도달 거리 해석조건 UI 정비

### 변경 파일

- `request_ai_agent_h3_v0/ui.py`
- `request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`
- `docs/h3_v0_execution_handoff.md`

### 변경 내용

- 기류 도달 거리의 확정 fieldset(`reach_required`)만 UI에서 운전 조건, 부품 사양, 온도 조건, 설치 환경, 결과 요청으로 표시한다. 이 UI 분리는 snapshot의 필드값·수집 구조를 바꾸지 않는다.
- 온도 조건에는 `heat_exchanger_temp`(취출 온도), `room_temp`(공간 온도)만 표시한다. 상대습도 두 항목은 기류 도달 거리 UI에 포함하지 않는다.
- 온도 조건에 “해당 값이 있으면 입력해주세요. 모르는 경우 비워두어도 제출할 수 있습니다.” 안내를 표시한다. 두 온도 항목에는 추천 문구를 추가하지 않는다.
- 운전 조건에는 운전 풍량(CMM)을 우선 입력으로 안내하고, 팬 회전수(Fan RPM)는 운전 풍량이 없을 때 대체 입력할 수 있다고 안내한다.
- 기존 전역 온·습도 조건 토글은 기류 도달 거리 UI 렌더링에 사용하지 않는다.
- validator, 진행률, 제출 payload, Case Matrix 로직은 수정하지 않았다.

### 검증 결과

- 기류 도달 거리 UI 그룹의 온도 입력 key가 `heat_exchanger_temp`, `room_temp`로만 구성되는 회귀 검증을 추가했다.
- 온도 선택 입력 안내와 CMM 우선·RPM 대체 입력 안내 문구가 UI 템플릿에 포함됨을 확인했다.
- `..\.venv\Scripts\python.exe -m py_compile request_ai_agent_h3_v0/ui.py request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (14 passed)

## Stage 12 열교환기 사양 세부 입력 구조

### 변경 파일

- `request_ai_agent_h3_v0/state.py`
- `request_ai_agent_h3_v0/condition_fieldsets.py`
- `request_ai_agent_h3_v0/condition_engine.py`
- `request_ai_agent_h3_v0/ui.py`
- `request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`
- `docs/h3_v0_execution_handoff.md`

### 변경 내용

- 기존 active fieldset key인 `heat_exchanger_spec`와 validator/progress/payload/Case Matrix 연결은 그대로 재사용했다. `PDB` 제출 payload에서는 `hex_spec`도 제거하여 해당 key가 없는 해석유형에 열교환기 사양 연결 데이터가 생기지 않는다.
- `conditions.hex_spec`에 일반 field 구조로 세부값을 보관한다.
  - 핀 종류: `fin_type` = `WIDE LOUVER PLUS`
  - 관 직경: `tube_diameter` = `7PI`
  - 열 수: `row_count` = `3R`
  - FPI: `fpi` = `14FPI`
- UI는 active `heat_exchanger_spec` field에만 네 개의 분리된 입력을 표시한다. 사용자가 하나라도 수정하면 기존 호환 값 `heat_exchanger_spec`을 `WIDE LOUVER PLUS / 7PI / 3R / 14FPI` 형식으로 생성하여 기존 하위 경로가 계속 사용한다.
- 신규 기본값은 모두 `source="system"`으로 기록하고, 기본값만으로는 `condition_values.heat_exchanger_spec`을 만들지 않는다. 이로써 Stage 3/9의 사용자 입력 진행률 원칙을 유지한다.
- `heat_exchanger_default` pending behavior는 `implemented`로 갱신했다.

### 제출 처리 판단

- required `heat_exchanger_spec`의 validator는 기존처럼 active condition value가 실제로 존재하는지만 검사한다. 기본값을 자동으로 제출 충족 값으로 주입하지 않았으므로, 기본값만 있는 신규 의뢰서는 required 누락으로 제출할 수 없다.
- 이는 기본값을 화면에 표시하면서도 사용자 입력 완료로 간주하지 않는 Stage 3/9 원칙과 충돌하지 않는다. validator 정책 자체는 변경하지 않았다.

### 검증 결과

- `열교환기 유속 프로파일`, `이슬맺힘`, `일반 유동 해석`, `열유동 해석`, `기류 도달 거리`의 active fieldset에 `heat_exchanger_spec`이 포함되고, `PDB`에는 포함되지 않는 기존 fieldset/payload/Case Matrix 회귀 검증을 통과했다.
- 세부값을 사용자가 수정하면 기존 `heat_exchanger_spec` 호환 값으로 합성되고 진행률에 반영됨을 확인했다.
- `..\.venv\Scripts\python.exe -m py_compile request_ai_agent_h3_v0/state.py request_ai_agent_h3_v0/condition_fieldsets.py request_ai_agent_h3_v0/ui.py request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (16 passed)

## Stage 13 최종 Fieldset 수용 기준 회귀 검증

### 수정 파일

- `docs/h3_v0_execution_handoff.md`

### 수정 이유 및 범위

- 최종 Fieldset 수용 기준에 대한 회귀 검증 결과를 기록했다.
- 기능 소스와 테스트 소스는 수정하지 않았다. 수용 기준을 충족하는 기존 구현과 최소 회귀 테스트(16개)를 확인했으며, 명확한 회귀 오류는 발견되지 않았다.
- h2_v2, Preview, Word, Export, PPT, 이미지 관련 기능은 수정하지 않았다.

### 수용 기준 검증 결과

- `열교환기 유속 프로파일`, `일반 유동 해석`: `fan_rpm`, `heat_exchanger_spec`이 각각 필수이며 하나라도 누락하면 제출 NG임을 확인했다.
- `PDB`: 운전 풍량, 취출 온도, 공간 온도, 설치 환경, 제품 설치 위치, 유선 표기가 모두 필수이며 각각 누락 시 제출 NG임을 확인했다.
- `기류 도달 거리`: 운전 풍량 또는 팬 회전수 중 하나 이상이면 제출 가능하고, 둘 다 없으면 제출 NG이며, 둘 다 입력하면 두 값이 보존됨을 확인했다. 취출/공간 온도는 선택 입력이고, 취출/공간 상대습도는 UI·validator·진행률·제출 payload·Case Matrix에서 제외됨을 확인했다.
- `이슬맺힘`: 팬 회전수, 열교환기 사양, 취출/공간 온도·습도가 모두 필수임을 확인했다.
- `열유동 해석`: 팬 회전수, 열교환기 사양, 취출 온도, 공간 온도가 모두 필수임을 확인했다.
- 활성 fieldset 밖 항목은 진행률, validator, 제출 payload, Case Matrix에 포함되지 않음을 확인했다. UI도 확정 fieldset snapshot만 렌더링한다.
- 일체형 제품군의 실내·실외·동시운전 key 치환/복제 구조를 별도 assertion으로 확인했다.

### validator/진행률 반영 여부

- 반영됨. validator와 진행률은 확정 fieldset snapshot의 `required_level` 및 `conditional_group`을 사용한다.
- 제출 payload와 Case Matrix는 값이 있는 활성 fieldset key만 사용한다. 기류 도달 거리의 선택 온도는 값이 있을 때만 포함하고, 상대습도 key는 값이 있어도 제외한다.

### 검증 결과

- `python tools/check_encoding.py --changed`: 통과
- `git diff --check`: 통과
- `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h3_v0/tests/test_task12_minimal_regression.py`: 통과 (16 passed)
- 일체형 제품군 실내/실외/동시운전 fieldset assertion: 통과
- Preview, Word, Export, PPT, 이미지 관련 기능의 기능 소스 변경 없음: 현재 Git diff 기준 확인

### 남은 리스크

- 추적 중인 `__pycache__` 바이너리 변경과 pytest가 만든 untracked pyc 파일은 이번 작업 범위 밖이므로 보존했다. 커밋에는 포함하지 않는다.
- 확정된 기존 의뢰는 `condition_fieldset_snapshot`을 계속 사용하므로, 이후 fieldset 정의를 변경하면 해당 의뢰의 조합을 다시 확정해 snapshot을 재생성해야 한다.
