# h5_v0 단계별 작업 인수인계

## 사용 방법

- 각 새 채팅은 작업할 단계의 프롬프트 문서, 이 문서, `AGENTS.md`를 먼저 읽는다.
- 이전 단계가 `완료`가 아니거나 검증 결과가 기록되지 않았으면 구현을 시작하지 않는다.
- 한 단계에서는 그 단계의 목표만 변경한다. 다음 단계의 구조를 미리 구현하거나 대규모 리팩터링하지 않는다.
- 단계가 끝나면 아래 작업 이력 형식으로 이 문서를 갱신한다. 다음 작업자는 이 기록을 기준으로 이어서 작업한다.

## 확정 적용 범위

- 화면은 좌측 진행률 Rail, 중앙 h3 스타일 폼 또는 미리보기, 우측 상시 Agent의 3열 구조다.
- 최근 의뢰 목록 Rail, 상단 진행률, 임시저장, 제출, 제출 전 최종확인, 제출 후 상태 UI는 제거한다.
- 상단 우측 행동은 `미리보기`, `의뢰서 생성(Word)`만 제공한다.
- 중앙 단계는 해석개요, 제품형상, 해석조건, 조건조합, Case Matrix다.
- 해석개요는 새 요청 내용 계약과 `프로젝트명(PMS)`, `모델명(Model Suffix)` 표기를 사용한다.
- 제품은 기준 1개와 비교 제품 0..N의 완성 제품 구조를 사용한다.
- 조건은 운전 조건, 열교환기 사양, 취출 공기 조건, 공간 환경 조건 카드만 사용한다. 첫 기본 카드는 삭제할 수 없고, 추가 카드는 삭제할 수 있으며, 복제는 제공하지 않는다.
- 설치 조건, 기류 도달 거리, PDB, Case 수 기반 사용자/관리자 확인은 구현하지 않는다.
- 조건조합은 생성 기준과 적용 제품을 확정하고, Case Matrix는 읽기 전용 결과 검토와 stale/재생성을 담당한다.
- Agent는 항상 우측에 표시하며, 승인 전 자동 State 변경을 하지 않는다.
- Word는 제출 기능이 아니다. 미리보기 화면에 렌더링된 내용과 순서를 원본으로 DOCX를 생성하며 validator, 제출 상태, Matrix stale 여부로 생성 버튼을 막지 않는다.
- 기존 h3 저장본은 복원 또는 migration 대상이 아니다.
- 원본 명세 문서는 수정하지 않는다. 이 범위와 명세가 충돌하면 이 범위가 우선한다.

## 단계 상태

| 단계 | 문서 | 상태 | 완료 기록 |
|---|---|---|---|
| 00 | `h5_v0_update_prompts/00_preflight.md` | 완료 | 2026-07-27 |
| 01 | `h5_v0_update_prompts/01_shell_and_navigation.md` | 완료 | 2026-07-27 |
| 02 | `h5_v0_update_prompts/02_overview_contract.md` | 완료 | 2026-07-27 |
| 03 | `h5_v0_update_prompts/03_product_geometry.md` | 완료 | 2026-07-27 |
| 04 | `h5_v0_update_prompts/04_condition_cards.md` | 완료 | 2026-07-27 |
| 05 | `h5_v0_update_prompts/05_condition_combinations.md` | 완료 | 2026-07-27 |
| 06 | `h5_v0_update_prompts/06_case_matrix_stale.md` | 완료 | 2026-07-27 |
| 07 | `h5_v0_update_prompts/07_agent_summary.md` | 완료 | 2026-07-27 |
| 08 | `h5_v0_update_prompts/08_preview_screen.md` | 완료 | 2026-07-27 |
| 09 | `h5_v0_update_prompts/09_word_export.md` | 완료 | 2026-07-27 |
| 10 | `h5_v0_update_prompts/10_cleanup_and_integration.md` | 완료 | 2026-07-27 |

## 작업 이력 형식

각 단계 종료 시 아래 형식을 복사해 최신 항목을 맨 위에 추가한다.

```md
### Stage NN — YYYY-MM-DD

- 상태: 완료 | 보류 | 실패
- 변경 파일: `path/to/file`
- 구현 요약:
- 의도적으로 제외한 내용:
- 실행한 검증:
- 검증 결과:
- 커밋: 해시와 메시지 | 없음 및 사유
- 다음 단계 전달사항:
- 남은 리스크:
```

## 현재 작업 이력

### Stage 10 — 2026-07-27

- 상태: 완료
- 변경 파일: `request_ai_agent_h5_v0/app.py`, `request_ai_agent_h5_v0/ui.py`, `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`, `docs/h5_v0_execution_handoff.md`
- 구현 요약:
  - Stage 00~09의 완료 상태와 각 검증 기록을 모두 확인한 뒤 통합을 수행했다.
  - 활성 UI와 bootstrap 공개 계약에서 최근 의뢰, 임시저장, 제출/제출 상태/최종 검토, 자동 제목·의뢰번호, Case 수 기반 최종 제출 제안을 분리했다. 과거 API·State는 호환 경로로 남아 있어도 새 UI와 canonical 흐름의 입력·표시 원본으로 사용하지 않는다.
  - 좌측 Rail과 우측 Agent Summary는 동일한 `state.stage_progress`를 사용하고, 중앙 폼·미리보기는 동일한 현재 `requestState`를 렌더링한다. 미리보기와 Word는 `data-preview-document`의 현재 DOM 직렬화만 사용하며 `preview_document`나 기존 Word 템플릿에 의존하지 않는다.
  - Stage 10 회귀 테스트로 활성 템플릿/Bootstrap 계약에서 제외 항목이 빠지고 Word DOM 계약이 유지되는지 확인했다.
- 의도적으로 제외한 내용: 과거 recent/submit/draft/review API 및 State의 삭제·migration·대규모 리팩터링, 기존 Word DOCX 형식 확장은 수행하지 않았다.
- 실행한 검증:
  - `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0\tests\test_task12_minimal_regression.py -q`
  - `..\.venv\Scripts\python.exe -m pytest -q`
  - `..\.venv\Scripts\python.exe tools\check_encoding.py --all`
  - `git diff --check`
- 검증 결과: 관련 회귀 15개 통과, 전체 기존 테스트 15개 통과, 전체 인코딩 검사 및 diff whitespace 검사 통과.
- 커밋: `chore: complete h5 stage 10 integration`.
- 다음 단계 전달사항: h5_v0의 활성 원본은 현재 canonical State와 렌더링된 preview DOM이다. 호환 API/State를 다시 연결하려면 별도 범위와 계약을 정의해야 한다.
- 남은 리스크: 과거 recent/submit/draft/review 및 `preview_document` API·State 구현은 호환 목적으로 저장소에 남아 있다. 현재 UI/Bootstrap/Word 흐름에서는 참조하지 않으며, 실제 브라우저 E2E 자동화는 수행하지 않았다.

### Stage 09 — 2026-07-27

- 상태: 완료
- 변경 파일: `request_ai_agent_h5_v0/app.py`, `request_ai_agent_h5_v0/ui.py`, `request_ai_agent_h5_v0/word_export.py`, `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`, `docs/h5_v0_execution_handoff.md`
- 구현 요약:
  - 상단 우측 `의뢰서 생성(Word)` 버튼은 제출·validator·Matrix stale 상태와 독립적으로 항상 실행되며, 현재 브라우저의 `data-preview-document` DOM을 최소 JSON으로 직렬화해 DOCX를 다운로드한다.
  - Word는 DOM 순서의 section 제목, label/value, 표 caption·header·행, Matrix stale 경고만 담는다. 별도 document State, 기존 Word 템플릿, 과거 Base/Variant·배경/목적/목표 매핑은 사용하지 않는다.
  - 템플릿·대형 클라이언트 라이브러리 없이 최소 DOCX XML을 생성하고, 자동 의뢰 제목 없이 안전한 기본 파일명 `analysis_request.docx`를 사용한다.
- 의도적으로 제외한 내용: 제출·검증·저장·최종확인 State 연동, 자동 의뢰 제목, 화면 밖 문서 내용 추가.
- 실행한 검증:
  - `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0\tests\test_task12_minimal_regression.py -q`
  - `python tools/check_encoding.py --changed`
  - `git diff --check`
- 검증 결과: DOM 직렬화 계약 및 stale 표기 포함 DOCX 응답 테스트 14개 통과. 인코딩·diff 검사는 통과.
- 커밋: `feat: export rendered preview to word`.
- 다음 단계 전달사항: Stage 10은 Word export가 현재 렌더링된 preview DOM만 입력으로 사용한다는 계약과 `analysis_request.docx` 기본 파일명을 유지해야 한다.
- 남은 리스크: 브라우저 실상호작용 자동화는 실행하지 않았으며, 최소 DOCX의 표 스타일은 Word 기본 `TableGrid`에 의존한다.

### Stage 08 — 2026-07-27

- 상태: 완료
- 변경 파일: `request_ai_agent_h5_v0/ui.py`, `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`, `docs/h5_v0_execution_handoff.md`
- 구현 요약:
  - 상단 우측 `미리보기` 버튼으로 중앙 Workspace를 현재 화면 State 기반 의뢰서 미리보기로 전환하고, 같은 버튼으로 작성 화면으로 돌아오게 했다. 우측 Agent는 그대로 유지한다.
  - 별도 `preview_document` State나 비활성 preview API 호출 없이 해석개요, 해석 제품, 조건 카드, 조건조합, Case Matrix를 section/label/value/table 식별자가 있는 안정적인 DOM으로 렌더링한다.
  - Matrix가 stale이면 이전 Case 표를 렌더링하지 않고 stale 원인과 `Case 다시 생성` 필요 안내를 표시한다.
- 의도적으로 제외한 내용: Word export, 제출 검증, 임시저장, 최종확인 State 및 기존 비활성 preview API의 활성화/변경.
- 실행한 검증:
  - `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0\tests\test_task12_minimal_regression.py -q`
  - `python tools\check_encoding.py --changed`
  - `git diff --check`
- 검증 결과: UI 중심 최소 회귀 테스트 12개, 변경 파일 인코딩 검사, diff whitespace 검사 통과.
- 커밋: `feat: build stage 08 preview screen`.
- 다음 단계 전달사항: Stage 09는 `data-preview-document`, `data-preview-section`, `data-preview-label`, `data-preview-value`, `data-preview-table` DOM을 Word 직렬화 입력으로 사용할 수 있다. stale Matrix에는 `data-preview-matrix-stale="true"`만 존재하며 이전 Case 표가 없다.
- 남은 리스크: 실제 브라우저 상호작용 자동화는 실행하지 않았고, UI 템플릿 최소 회귀 테스트로 전환/DOM 계약을 확인했다.

### Stage 07 — 2026-07-27

- 상태: 완료
- 변경 파일: `request_ai_agent_h5_v0/app.py`, `request_ai_agent_h5_v0/ui.py`, `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`, `docs/h5_v0_execution_handoff.md`
- 구현 요약:
  - 우측 Agent를 모든 표준 단계에 상시 노출되는 Summary와 대화 영역으로 유지하고, Summary는 해석개요·제품형상·해석조건·조건조합·Case Matrix의 완료 수/전체 수, 입력 여부, 오류 수만 표시하도록 변경했다.
  - Agent 제안은 기준 State fingerprint를 함께 보관하고, 원본 Field, 선택 해석유형, 조건 Snapshot, 조건조합, Case generation이 달라지면 승인 반영을 차단한다. 무효화 사유와 새 제안 받기 동작을 제공한다.
  - 즉시 Agent 경로도 승인 전 State를 바꾸지 않도록 proposal-only로 전환했다. Agent는 해석유형을 자동 변경하지 않으며 PDB/기류 도달 거리 경로를 추가하지 않았다.
- 의도적으로 제외한 내용: Agent 대화 모델/RAG 구조 변경, 외부 의존성 추가, preview/Word 구현 및 전체 테스트 실행.
- 실행한 검증:
  - `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0\tests\test_task12_minimal_regression.py -q`
  - `python tools/check_encoding.py --changed`
  - `git diff --check`
- 검증 결과: 관련 proposal/UI 최소 회귀 테스트 11개, 변경 파일 인코딩 검사, diff whitespace 검사 통과.
- 커밋: `feat: complete stage 07 agent summary`.
- 다음 단계 전달사항: Stage 08은 우측 Agent Summary의 count-only 계약과 proposal invalidation을 유지한다. `case_matrix.stale`은 preview/Word 차단 사유로 사용하지 않는다.
- 남은 리스크: proposal fingerprint는 서버에 보관된 pending proposal ID만 승인할 수 있으므로, 새로고침 뒤 과거 제안은 의도적으로 새 제안을 받아야 한다.

### Stage 06 — 2026-07-27

- 상태: 완료
- 변경 파일: `request_ai_agent_h5_v0/case_matrix.py`, `request_ai_agent_h5_v0/state.py`, `request_ai_agent_h5_v0/validator.py`, `request_ai_agent_h5_v0/app.py`, `request_ai_agent_h5_v0/ui.py`, `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`, `docs/h5_v0_execution_handoff.md`
- 구현 요약:
  - Case Matrix는 포함된 Condition Set/적용 제품 조합에서만 Case를 생성하며, Matrix는 포함/제외, 상세 서명 확인, 원본 조건 이동만 제공하는 읽기 전용 검토 화면으로 구성했다.
  - 생성 시 입력 스냅샷과 Case signature를 저장한다. 제품, Condition Set, 조합, 적용 제품 또는 Case 포함 상태 변경은 `generation_status`를 보존한 채 `stale` 및 구체적 원인으로 전환한다.
  - stale 화면은 이전 Matrix를 표로 표시하지 않고 원인, 원본 이동, Case 다시 생성 행동을 제공한다. 재생성은 동일 signature의 Case ID·포함 상태만 유지하고, 새 signature에는 제외 상태를 승계하지 않는다.
  - validator/progress는 stale을 경고 계약으로 노출하며 stale 자체로 이후 preview/Word 단계를 차단하지 않는다.
- 의도적으로 제외한 내용: Case 수 확인, 관리자 확인, Tier/숫자 구간 정책, preview/Word 구현은 추가하지 않았다.
- 실행한 검증:
  - `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0\tests\test_task12_minimal_regression.py -q`
  - `python tools\check_encoding.py --changed`
  - `git diff --check`
- 검증 결과: 최소 회귀 10개 통과, 인코딩 및 diff 검사 통과.
- 커밋: Stage 06 구현 변경으로 함께 커밋.
- 다음 단계 전달사항: Stage 07 이상은 `case_matrix.stale`, `stale_reasons`, `generation_status`를 그대로 경고 표시에 사용하고 stale을 preview/Word 차단 사유로 만들지 않는다.
- 남은 리스크: Case signature는 제품 ID와 Condition Set ID의 조합이다. 같은 ID의 내용 수정은 stale을 유발하지만 재생성 시 동일 Case로 유지한다.

### Stage 05 — 2026-07-27

- 상태: 완료
- 변경 파일: `request_ai_agent_h5_v0/state.py`, `request_ai_agent_h5_v0/validator.py`, `request_ai_agent_h5_v0/app.py`, `request_ai_agent_h5_v0/ui.py`, `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`, `docs/h5_v0_execution_handoff.md`
- 구현 요약:
  - 조건카드는 제품 선택 없이 `conditions.condition_sets`만 유지하고, 조건조합은 Condition Set ID 참조·포함 여부·적용 제품 ID를 `conditions.combinations`에서 한 번만 확정한다.
  - 포함 조합은 최소 하나의 Condition Set과 제품을 요구하며, 정확히 같은 Condition Set/제품 참조 조합은 정규화 단계에서 하나만 남긴다. 표현상 의미 비교는 하지 않는다.
  - 조합 수에 따라 Compact Summary, 카드 목록, 전체 표를 선택해 h3 밀도로 표시하고, 조건조합 진행률을 추가했다.
  - 조합 구조가 바뀌면 Case Matrix를 생성하지 않고 `case_matrix.stale_reasons`에 `condition_combinations_changed`만 남긴다.
- 의도적으로 제외한 내용: 설치 조건, Cartesian/Pairwise 선택, Case 수 승인 정책, Case Matrix 결과 표·생성·재생성은 구현하지 않았다.
- 실행한 검증:
  - `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0\tests\test_task12_minimal_regression.py -q`
- 검증 결과: 조건조합 참조·제품 필수·정확 일치 중복 제거·stale 사유·UI 계약을 포함한 최소 회귀 테스트 8개 통과.
- 커밋: `7afe645` (`feat: build stage 05 condition combinations`).
- 다음 단계 전달사항: Stage 06은 `conditions.combinations`의 포함 조합만 사용해 Matrix 결과와 재생성을 구현하고, Stage 05의 stale 사유를 해소해야 한다.
- 남은 리스크: 이전 Case 축/Matrix 보조 모듈은 호환 코드로 남아 있지만, Stage 05의 validator와 상태 갱신은 이를 호출하거나 결과를 생성하지 않는다.

### Stage 04 — 2026-07-27

- 상태: 완료
- 변경 파일: `request_ai_agent_h5_v0/condition_fieldsets.py`, `request_ai_agent_h5_v0/state.py`, `request_ai_agent_h5_v0/validator.py`, `request_ai_agent_h5_v0/constants.py`, `request_ai_agent_h5_v0/analysis_type_master.py`, `request_ai_agent_h5_v0/ui.py`, `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`, `docs/h5_v0_execution_handoff.md`
- 구현 요약:
  - 해석조건의 canonical 원본을 `conditions.condition_sets` 카드 배열로 바꾸고, 현재 해석유형에서 활성인 네 종류의 첫 기본 카드와 빈 Template 기반 추가 카드를 제공한다.
  - 카드 UI는 운전 조건, 열교환기 사양, 취출 공기 조건, 공간 환경 조건만 표시한다. 열교환기 카드는 Fin type, 관 직경, 행 수, FPI를 사용한다.
  - 단일 Fan은 간결하게 표시하고 복수 Fan만 식별·운전/정지·값을 표시한다. 정지 Fan 값은 active fieldset·진행률·validator에서 제외한다.
  - PDB·기류 도달 거리·설치 조건 경로를 해석유형 Master, fieldset, validator, UI에서 제거했다.
- 의도적으로 제외한 내용: 제품 적용, 조건조합, Case 생성 및 stale 처리는 Stage 05/06 범위로 남겼다.
- 실행한 검증:
  - `..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0\tests\test_task12_minimal_regression.py -q`
  - `python tools/check_encoding.py --changed`
  - `git diff --check`
- 검증 결과: Stage 04 fieldset·State·Fan·validator·UI 계약 테스트 5개 통과.
- 커밋: `feat: build stage 04 condition cards`.
- 다음 단계 전달사항: Stage 05는 조건 카드의 `condition_sets`만 읽고, 이 단계에서 Case 축이나 제품 적용을 추가하지 않는다.
- 남은 리스크: 과거 Condition Set 이외의 legacy helper는 호환 코드로 남아 있을 수 있으나, 새 State 저장 및 UI 제출 원본으로 사용하지 않는다.

### Stage 03 — 2026-07-27

- 상태: 완료
- 변경 파일: `request_ai_agent_h5_v0/constants.py`, `request_ai_agent_h5_v0/state.py`, `request_ai_agent_h5_v0/geometry_engine.py`, `request_ai_agent_h5_v0/validator.py`, `request_ai_agent_h5_v0/app.py`, `request_ai_agent_h5_v0/ui.py`, `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`, `docs/h5_v0_execution_handoff.md`
- 구현 요약:
  - 제품 원본을 `base_product` 1개와 `comparison_products` 0..N으로 교체했다. 각 카드는 안정적인 `geometry_id`, `drawing_no`, 선택 `display_name`, 역할(`base`/`comparison`)을 가진다.
  - 비교 제품은 `difference_from_base`를 별도로 입력하며, 비교 제품 추가는 빈 카드 하나만 추가한다. 기준 카드와 비교 카드 모두 기존 h3 입력 밀도를 유지한다.
  - geometry axis, validator, 진행률은 새 완성 제품만 사용한다. 부품 조립·미등록 조합을 만들지 않으며, 이전 `Base/Variant` 키를 새 저장 State로 migration하지 않는다.
- 의도적으로 제외한 내용: 조건조합, Case 생성 흐름, Word 및 다음 단계의 UI/계약은 변경하지 않았다.
- 실행한 검증:
  - `.\..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0\tests\test_task12_minimal_regression.py -q`
  - `python tools/check_encoding.py --changed`
  - `git diff --check`
- 검증 결과: 최소 회귀 테스트 17개 통과. 인코딩 및 diff 검사는 통과.
- 커밋: 예정 — Stage 03 변경과 인수인계를 함께 커밋한다.
- 다음 단계 전달사항: Stage 04는 제품 State를 `geometry.base_product`와 `geometry.comparison_products`로만 읽어야 한다. Case/조건조합에는 새 product axis를 소비하는 별도 계약을 Stage 05/06에서 확정한다.
- 남은 리스크: 기존 미리보기·RAG·과거 제출 보조 코드에는 이전 제품 표현이 남아 있을 수 있으나, 이번 Stage의 UI·State·geometry axis·validator·progress 원본에는 사용하지 않는다. 이 경로는 Stage 08~10에서 새 제품 계약으로 정리한다.

### Stage 02 — 2026-07-27

- 상태: 완료
- 변경 파일: `request_ai_agent_h5_v0/analysis_type_master.py`, `request_ai_agent_h5_v0/constants.py`, `request_ai_agent_h5_v0/state.py`, `request_ai_agent_h5_v0/app.py`, `request_ai_agent_h5_v0/analysis_type_recommender.py`, `request_ai_agent_h5_v0/chat_patch.py`, `request_ai_agent_h5_v0/ui.py`, `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`, `docs/h5_v0_execution_handoff.md`
- 구현 요약:
  - 해석개요 State를 h5 계약으로 교체했다. `development_grade`, `desired_completion_date`, `request_description`, `decision_use`, `additional_result_request`를 사용하며, 과거 개요의 `pms_group`·`platform`·`analysis_type`과 배경·목적·목표·산출물은 원본 State와 UI에서 제거했다.
  - 제품군·Platform·해석유형은 `request_context`만 사용한다. 개요에서 Context를 되살리거나 과거 개요 값에서 이관하지 않는다.
  - 요청 내용 진행률과 validator는 `request_description` 및 유효한 `decision_use`만 기준으로 한다. 추가 결과 요청과 결과 안내는 완료율·검증을 막지 않는다.
  - 선택 해석유형의 읽기 전용 결과 안내 Master 조회 API와 UI를 추가했다. 조회 실패 시 재시도만 표시하며 완료·검증을 차단하지 않는다.
- 의도적으로 제외한 내용: 기존 h3 저장본 migration, 과거 key 호환, 자동 제목 및 제출 흐름 복원, 다음 단계의 제품·조건·미리보기·Word 구현은 수행하지 않았다.
- 실행한 검증:
  - `.\\..\\.venv\\Scripts\\python.exe -m pytest request_ai_agent_h5_v0\\tests\\test_task12_minimal_regression.py`
  - `python tools/check_encoding.py --changed`
  - `git diff --check`
- 검증 결과: 최소 회귀 테스트 17개 통과. 인코딩 및 diff 검사는 통과.
- 커밋: `4d780ee` (`feat: update h5 overview contract`). 인수인계 갱신은 별도 문서 커밋으로 남긴다.
- 다음 단계 전달사항: Stage 03은 이 h5 해석개요/Context 경계를 유지하고 제품형상만 전환한다.
- 남은 리스크: Stage 01의 과거 보류 중복 기록은 현재 단계 상태 표와 완료 커밋에 반하는 이력이다. 후속 단계는 완료 상태 표와 첫 번째 Stage 01 완료 기록을 기준으로 한다.

### Stage 00 — 2026-07-27

- 상태: 완료
- 변경 파일: `docs/h5_v0_execution_handoff.md`
- 구현 요약:
  - 기준선만 읽기 전용으로 조사했다. 현재 UI는 `ui.py:106-111`의 3열 grid (`250px | minmax(640px,820px) | 390px`)이며, 좌측 Rail의 최근 의뢰는 `ui.py:450-455`, 중앙 상단 진행률은 `ui.py:458-471` 및 `ui.py:1950-1956`, 상단 행동(임시 저장·제출)은 `ui.py:434-446`에 있다.
  - State 원본은 `constants.py:17-20`의 `analysis_overview`·`geometry`·`conditions`·`case_matrix`이고, 초기화/정규화는 `state.py:891-958`, `state.py:1052-1165`에 있다. 공통 State API는 `/api/bootstrap`, `/api/input/save`, `/api/preview` (`app.py:1183-1253`)이며, 해석개요 선택은 `/api/analysis-type/select`, 제품 계층은 `/api/product-hierarchy`, 조건 Fieldset은 `/api/request-context/confirm`·`/api/request-context/fieldset`이다. Case는 `validator.py:626-634`에서 `case_matrix`에 반영되고 `/api/input/save`·`/api/preview`·`/api/review`·`/api/submit` 응답으로 반환된다.
  - Feature Lock은 `app.py:52-62`의 `FEATURE_LOCKS`에서 `preview_screen=False`, `word_export=False`로 선언되고, `/api/document-preview` (`app.py:1328-1330`), `/api/export/word-payload` (`app.py:1347-1349`), `/api/export/word` (`app.py:1384-1386`)가 `_disabled_feature_payload()`로 즉시 403을 반환한다. UI 미리보기도 `ui.py:2533-2536`에서 즉시 반환한다.
  - PDB·기류 도달 거리·설치 조건의 기준 Fieldset은 `condition_fieldsets.py:189-218`에 있다. 기류 도달 거리의 설치 환경·제품 설치 위치·기류 도달 기준 속도는 `:200-202`, PDB의 설치 환경·제품 설치 위치·유선 표기는 `:215-217`이다. 조건 축/Case 연결은 `condition_engine.py:177-189`, `case_matrix.py:145-269`, 검증은 `validator.py:322-418`, `validator.py:492-634`를 참조한다.
  - 가장 가까운 기존 회귀 테스트는 `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`; 실행 명령은 프로젝트 루트에서 `python -m pytest request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`이다. Stage 00은 문서 갱신만 수행하므로 해당 테스트는 실행하지 않았다.
- 의도적으로 제외한 내용: 기능 소스, 명세 원문, 테스트는 수정하지 않았고 전체 테스트 및 리팩터링을 수행하지 않았다.
- 실행한 검증:
  - `python tools/check_encoding.py --changed`
  - `git diff --check`
- 검증 결과: 통과 — `python tools/check_encoding.py --changed`와 `git diff --check`를 새 Git 기준선에서 실행했다.
- 커밋: 초기 기준선 `1d0f7e7` (`chore: establish h5_v0 baseline`) 생성. Stage 00 기록은 `docs: complete h5_v0 stage 00`으로 커밋했다.
- 다음 단계 전달사항: Stage 01은 이 기준선의 3열 shell, 최근 의뢰 Rail, 상단 진행률과 상단 행동 위치를 전제로 구현한다. Preview/Word Feature Lock은 Stage 08/09 전까지 유지한다.
- 남은 리스크: 기존 `preview_document.py`·`word_export.py` 구현은 존재하지만 서버/API Feature Lock으로 도달 불가하므로, 잠금 해제 전 연결 경로와 UI 조기 반환을 함께 점검해야 한다.

### Stage 01 — 2026-07-27

- 상태: 완료
- 변경 파일: `request_ai_agent_h5_v0/ui.py`, `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`, `docs/h5_v0_execution_handoff.md`
- 구현 요약:
  - h3 시각 스타일의 3열 shell은 유지하고, 좌측 최근 의뢰 Rail을 해석개요·제품형상·해석조건·조건조합·Case Matrix의 5단계 진행 Rail로 교체했다. 서버 진행률은 앞의 3개 단계에만 임시 표시하고 조건조합과 Case Matrix는 `준비 중`으로 표시한다.
  - 중앙 상단 진행률 Strip, 좌측 새 의뢰 시작 UI, 상단 임시 저장·제출 UI와 해당 클릭 이벤트를 제거했다. 상단에는 비활성화된 `미리보기`, `의뢰서 생성(Word)` 자리만 남겼다.
  - 중앙에 `section-combinations` 이동 대상을 추가하고, 조건조합 데이터·검증 없이 준비 중 빈 자리로만 표시했다. 중앙 폼과 우측 상시 Agent는 유지했다.
  - 최근 의뢰 API·저장 함수는 삭제하지 않았으며, 템플릿의 초기 최근 의뢰 조회와 Rail 렌더링에서만 분리했다.
- 의도적으로 제외한 내용: State 리팩터링, 조건조합 데이터/검증, Case Matrix 재생성/stale 처리, 실제 미리보기·Word 기능 및 전체 테스트는 수행하지 않았다.
- 실행한 검증:
  - `python -m pytest request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py` (시스템 Python: `pytest` 모듈 없음)
  - `.\\..\\.venv\\Scripts\\python.exe -m pytest request_ai_agent_h5_v0\\tests\\test_task12_minimal_regression.py`
  - `python tools/check_encoding.py --changed`
  - `git diff --check`
- 검증 결과: 가상환경의 최소 회귀 테스트 16개 통과. 인코딩 검사와 diff whitespace 검사 통과. 시스템 Python의 `pytest` 미설치는 가상환경 실행으로 대체했다.
- 커밋: `4ced6ff` (`feat: build stage 01 navigation shell`)
- 다음 단계 전달사항: Stage 02는 5단계 Rail과 `section-combinations` 이동 대상을 유지한 채 해석개요 계약만 변경한다. 미리보기/Word 버튼은 Stage 08/09 전까지 비활성 자리로 유지한다.
- 남은 리스크: 기존 submit/recent 저장 함수는 호환성을 위해 남아 있으나 Stage 01 템플릿에서 노출되지 않는다. 조건조합과 Case Matrix의 실제 진행률·데이터 계약은 이후 단계에서 구현해야 한다.

### Stage 01 — 2026-07-27

- 상태: 보류
- 변경 파일: `docs/h5_v0_execution_handoff.md`
- 구현 요약: Stage 00 기록을 확인한 결과 상태가 `보류`이며, `python tools/check_encoding.py --changed`와 `git diff --check`가 Git 저장소/`HEAD` 부재로 실패한 상태다. Stage 01의 선행조건(완료된 Stage 00)을 충족하지 않아 화면 골격, UI 템플릿 테스트, 기존 UI 이벤트를 변경하지 않았다.
- 의도적으로 제외한 내용: 최근 의뢰 Rail·새 의뢰 시작 UI·상단 진행률·임시저장/제출 UI의 제거, 5단계 진행 Rail과 조건조합 빈 자리의 추가, UI 템플릿 테스트 갱신/실행, preview/Word 구현을 수행하지 않았다.
- 실행한 검증:
  - `python tools/check_encoding.py --changed`
  - `git diff --check`
  - `git -C .. status --short`
  - `git -C .. rev-parse --is-inside-work-tree`
  - `git -C .. rev-parse --verify HEAD`
- 검증 결과: 실패 — 인코딩 검사는 `Could not access 'HEAD'`로 변경 파일을 조회하지 못했고, `git diff --check` 및 Git 저장소 확인 명령은 `fatal: not a git repository`로 종료했다. Stage 00의 보류 원인이 계속되어 Stage 01 구현 검증 및 최소 UI 템플릿 테스트는 실행하지 않았다.
- 커밋: 없음 — Stage 01은 선행조건 미충족으로 문서 기록만 갱신했다.
- 다음 단계 전달사항: Git 저장소 기준선과 `HEAD`를 복구한 뒤 Stage 00의 지정 검증을 재실행해 완료로 갱신해야 한다. 그 후에만 Stage 01 화면 골격 변경과 최소 UI 템플릿 테스트를 수행할 수 있다.
- 남은 리스크: Stage 00이 완료되지 않은 상태에서 Stage 01 UI를 변경하면 단계별 실행 순서와 검증 기준을 위반한다.
