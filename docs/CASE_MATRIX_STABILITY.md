# Case Matrix 안정성 원칙과 고정 회귀 세트

이 문서는 `case-matrix-stable-20260920` 기준의 Case Matrix 상태관리와 검증
원칙을 기록한다. 이후 Case Matrix 변경은 이 문서의 lifecycle 계약과 고정 회귀
세트를 기본 완료 조건으로 사용한다.

## 상태관리 원칙

### REVIEW

- `reviewImpactedCaseIds` is supplemental information for showing the presence of REVIEW by scope on tabs, including the RAC Window `both` composite state where REBUILD takes precedence. It does not replace existing REVIEW completion decisions, `renderedScopes`, or the baseline lifecycle.

- 최초로 사용자가 확인한 Case Matrix 상태가 이후 변경 비교의 baseline이다.
- 기존 Case가 실제 참조하는 **유효 source**의 후속 내용 변경만 REVIEW 대상이다.
  신규 작성 source나 기존 Case가 참조하지 않는 source의 변경은 REVIEW가 아니다.
- REVIEW는 기존 Case 선택을 자동으로 바꾸지 않는다.
- 영향 Case와 scope를 실제로 확인한 뒤 SCREEN-05를 벗어나면 REVIEW가 완료되며,
  그 시점의 상태가 새 baseline이 된다.
- 동일 REVIEW의 preview refresh 또는 재평가는 이미 확인한 scope와 navigation 상태를
  초기화하지 않는다. 실제로 새 변경이 생겼을 때만 새 REVIEW로 처리한다.

### REBUILD

- Case가 참조하던 source를 더 이상 사용할 수 없으면 REBUILD이다.
- impact 판정의 유효성 기준은 normalization 및 dropdown source의 유효성 기준과
  일치해야 한다.
- 무효 선택을 다른 option, 특히 첫 option으로 자동 대체하지 않는다.
- 기존 value와 사용자에게 보였던 label을 보존하고, 사용자가 직접 새 유효값을
  선택하게 한다.
- `선택 필요`는 placeholder이며 실제 데이터 option이 아니다.
- REBUILD의 진행 차단과 복구는 기존 Required validation을 사용한다.

### Render와 navigation

- `refreshPreview()`는 SCREEN-05가 활성 상태가 아니어도 Matrix를 미리 렌더링할 수
  있다. Matrix 렌더링과 사용자의 실제 확인은 같은 사건이 아니다.
- REVIEW 확인은 SCREEN-05가 활성 상태이고 해당 scope Matrix가 실제 표시된 경우에만
  인정한다.
- 일반 의뢰의 공통 scope와 RAC Window의 `indoor`/`outdoor` scope key를 구분한다.

### 상태 덮어쓰기 방지

> 앞 단계에서 결정된 REVIEW/REBUILD 및 사용자 확인 상태가 이후 normalization,
> preview refresh, render, navigation 과정에서 자동 보정·초기화·덮어쓰기되지 않는지
> 확인한다.

특히 동일 REVIEW의 재평가와 실제 새로운 REVIEW 발생을 구분한다.

## 고정 회귀 테스트

다음 파일은 향후 Case Matrix 변경 시 우선 실행하는 집중 회귀 세트다.

| 테스트 파일 | 보호하는 핵심 흐름 |
| --- | --- |
| `test_rac_window_outdoor_matrix_review.py` | RAC `both` REVIEW/REBUILD lifecycle, 영향 scope 확인, 재평가 상태 보존, 오류 이동 |
| `test_rac_window_analysis_scope.py` | RAC `indoor`/`outdoor`/`both` Matrix·validation 경계와 scope별 Word 출력 |
| `test_case_matrix_coverage.py` | 정상 Case 추가·삭제, coverage, Case validation, preview/Word 차단 |
| `test_case_matrix_condition_groups.py` | 조건 그룹 선택, label 유지, 중복 조건 validation |
| `test_t204_case_impact_classification.py` | 참조 source만 impact로 분류하고 Case 선택을 보존하는 계약 |
| `test_t203_condition_card_workflow.py` | 조건 카드 변경과 live Case Matrix option 갱신 |
| `test_t102_navigation_gate_focus.py` | SCREEN-04/05/06 navigation gate와 validation focus |
| `test_task12_minimal_regression.py` | 기본 Case Matrix state, normalization, validation 회귀 |
| `test_final_review_preview.py` | SCREEN-06 최종 검토와 의뢰서 preview 모달 |

집중 회귀 명령:

```powershell
& ..\.venv\Scripts\python.exe -m pytest -q request_ai_agent_h9_v0/tests/test_rac_window_outdoor_matrix_review.py request_ai_agent_h9_v0/tests/test_rac_window_analysis_scope.py request_ai_agent_h9_v0/tests/test_case_matrix_coverage.py request_ai_agent_h9_v0/tests/test_case_matrix_condition_groups.py request_ai_agent_h9_v0/tests/test_t204_case_impact_classification.py request_ai_agent_h9_v0/tests/test_t203_condition_card_workflow.py request_ai_agent_h9_v0/tests/test_t102_navigation_gate_focus.py request_ai_agent_h9_v0/tests/test_task12_minimal_regression.py request_ai_agent_h9_v0/tests/test_final_review_preview.py
```

Case Matrix production code를 수정한 작업의 기본 완료 조건은 다음과 같다.

1. 위 집중 회귀 세트 통과
2. 전체 `pytest -q` 통과
3. 인코딩 검사 통과
4. `git diff --check` 통과
5. 실제 navigation/state 흐름에 영향을 주는 변경이면 해당 사용자 시나리오를
   브라우저에서도 확인

## 향후 개발 원칙

- 수정 전 실제 `입력 → impact → normalization → preview/render → navigation → validation`
  흐름을 확인한다.
- lifecycle 기능은 문자열 또는 함수 존재 검사만으로 완료 판단하지 않고, 연결된
  state/navigation 사용자 흐름을 최소 한 번 검증한다.
- 기존 테스트를 우선 재사용하고, 같은 의미의 테스트를 불필요하게 중복 추가하지
  않는다.
- Case Matrix 변경 후에는 고정 회귀 세트를 반드시 실행한다.
- 작은 기능 변경을 이유로 Case Matrix 전체를 리팩터링하지 않는다.
- 구조 변경이 필요하면 기능 패치와 분리해 별도 작업으로 수행한다.
