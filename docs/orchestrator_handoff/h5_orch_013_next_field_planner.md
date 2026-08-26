# 단계 정보

- 단계 ID: `H5-ORCH-013`
- 단계명: Next Field Planner
- 수행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: `69f9374`, H5-ORCH-006 Field Registry, H5-ORCH-007 latest-read/version, H5-ORCH-010/011 Conversation, H5-ORCH-012 Workflow State Machine
- Roadmap 버전: `1.6` (2026-08-01)
- 작업 상태: 완료 후보 — Worker는 Roadmap, 기준 카드, 다음 단계 프롬프트를 변경하지 않고 Reviewer 검토를 대기한다.

# 이번 단계 목표

호출자가 제공한 최신 Request State, read-only Registry snapshot, bounded question history, validation/review snapshot, 현재 workflow label만으로 최대 두 개의 다음 질문 field 또는 `validation_ready` 판단을 순수·결정론적으로 만든다.

# 사전 입력 문서

- `AGENTS.md`, 최신 Roadmap, `common_stage_contract.md`, `baseline_prompts.md`, `manual_stage_execution.md`
- `h5_orch_001_repo_map.md`부터 `h5_orch_012_workflow_machine.md`까지

# 실제 수행 내용

- `next_field_planner.py`에 immutable input, history, planned-field, validation-ready, stable failure DTO와 pure `plan_next_fields()`를 추가했다.
- `planner_input_from_state()`는 caller가 가진 State에서 기존 `get_field_registry(state)` snapshot만 만들 수 있는 convenience helper다. Request/Conversation/Proposal store를 읽지 않는다.
- active이면서 비어 있는 Registry field만 대상으로 하며, Registry dependency → existing validation blocker → required → optional 순으로 고정 정렬한다. 같은 우선순위에서는 이미 질문한 field를 뒤로 보내고 field ID로 안정 정렬한다.
- existing `review.submission`, `review.final_review`, 또는 validation summary가 ready이면 field 없이 `validation_ready`를 반환한다. 활성 미입력 후보가 없을 때도 같은 판단 DTO를 반환한다.
- malformed input, oversized/malformed history, invalid registry snapshot, Registry 또는 State 내부 validation/review read failure, invalid workflow label은 stable failure DTO만 반환한다.

# 변경 파일

- `request_ai_agent_h5_v0/next_field_planner.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_next_field_planner.py`
- `docs/orchestrator_handoff/h5_orch_013_next_field_planner.md`

# 신규 또는 변경된 데이터 구조

| DTO | caller-provided/read-only 계약 | 결과 |
|---|---|---|
| `NextFieldPlannerInput` | `request_state`, Registry tuple, 최대 100개의 `QuestionHistoryDTO`, workflow state, optional validation snapshot | persistence/store reference 없음 |
| `PlannedFieldDTO` | selected `field_id`, machine-readable ordered `reasons` | 최대 두 개만 `NextFieldPlanDTO`에 포함 |
| `ValidationReadyDecisionDTO` | 기존 validation/review ready 또는 질문 후보 없음 | workflow caller가 `validation_ready` event를 선택할 근거 |
| `PlannerFailureDTO` | malformed/read failure | no field, no mutation의 stable code |

## 결정 순서

| 순서 | 후보 조건 | 이유 코드 |
|---|---|---|
| 1 | 다른 미입력 후보의 Registry dependency | `unmet_dependency` |
| 2 | 기존 validation blocking path와 Registry binding이 일치 | `validation_blocker` |
| 3 | active required/conditional-required | `required` |
| 4 | active optional | `optional` |

동일 순위의 previously asked field는 `previously_asked` 이유를 남기고 뒤로 간다. inactive field는 후보가 아니다. 이 과정은 Fieldset/normalizer/Validator 규칙을 재구현하지 않고 Registry activation/dependency와 기존 validation 결과를 읽기만 한다.

# 신규 또는 변경된 API

없음. public HTTP endpoint나 기존 API를 추가·변경하지 않았다.

# 중요 설계 결정

- Planner는 `planning_next_question` 읽기 전용 label에서만 성공 판단을 한다. `question_planned`/`validation_ready` event 선택과 dispatch는 H5-ORCH-016 caller 책임이다.
- Request authority는 H5-ORCH-007 `RequestStateStore.read()`가 제공하는 latest State/version에 있고, Planner는 caller가 넘긴 snapshot만 본다. State/version을 저장하거나 변경하지 않는다.
- Conversation authority는 H5-ORCH-010/011 record/history와 H5-ORCH-012 dispatch에 있고, Planner는 bounded history value와 workflow label을 읽을 뿐 record를 변경하지 않는다.
- Proposal authority는 H5-ORCH-008/009 ledger/lifecycle에 있고, Planner는 proposal을 읽거나 생성·승인·거절·만료·적용하지 않는다.

# 기존 기능 재사용 지점

- H5-ORCH-006 `get_field_registry()`와 `FieldRegistryDTO`의 active/required/dependencies/binding metadata를 사용한다.
- H5-ORCH-007 latest State snapshot 및 H5-ORCH-010/011 bounded history는 caller가 제공하는 입력 경계로만 사용한다.
- existing `review.validator`, `review.submission`, `review.final_review` validation/review 결과를 재사용한다. Validator 또는 final-review pipeline을 호출·복제하지 않는다.
- H5-ORCH-012 vocabulary의 `planning_next_question`, `question_planned`, `validation_ready`를 handoff label로만 사용한다.

# 수행하지 않은 작업

- HTTP/message/LLM/RAG/external DB, Intent Router, Orchestrator service, UI, Proposal lifecycle을 추가하지 않았다.
- Request State mutation, persistence, version 변경, client State/Proposal payload 수용을 하지 않았다.
- Conversation lifecycle/workflow status 변경과 workflow dispatch를 하지 않았다.
- Fieldset, normalizer, Validator, Case Matrix, Preview, Word, renderer, regex/alias extraction 또는 keyword intent router를 변경·복제하지 않았다.

# 최소 검증

실행 명령:

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_next_field_planner.py request_ai_agent_h5_v0/tests/test_orchestrator_field_registry.py request_ai_agent_h5_v0/tests/test_orchestrator_workflow_machine.py
python tools/check_encoding.py --changed
git diff --check
```

Planner focused coverage:

- identical State/Registry/history/validation input의 동일 최대 두 field와 reason 및 3개 후보의 두 개 상한
- dependency/blocker/required가 optional, inactive candidate보다 앞서는 순서와 동순위 previously asked 후보의 후순위
- no candidate 및 existing ready validation의 `validation_ready`
- malformed history, bad State, Registry/validation read failure의 stable failure와 Request State/version·Conversation record·Proposal ledger 불변
- 서로 다른 Request/history isolation 및 Request/Conversation/Proposal store·workflow dispatch 호출 부재의 focused inspection

# 실패하거나 실행하지 못한 검증

전체 E2E, 전체 suite, 실제 LLM/RAG/external DB, multi-worker deployment는 범위 밖이므로 실행하지 않는다.

# 알려진 문제와 제한사항

- Planner는 process-local stores의 durable replacement가 아니다. caller가 supplied snapshot이 최신인지 보장해야 하며, restart/multi-worker/shared transaction semantics는 제공하지 않는다.
- Registry가 표현하지 않는 geometry/Case Matrix/review blocker는 새 질문 field로 추정하지 않는다. no Registry candidate면 workflow handoff용 readiness 판단만 반환한다.

# 발견된 위험

| 위험 | 현재 경계 | 후속 처리 |
|---|---|---|
| stale Request/validation snapshot | Planner가 latest-read를 하지 않음 | H5-ORCH-016이 Request latest-read/version 및 validation result를 다시 공급 |
| history replay | previously asked는 tie-breaker일 뿐 dedupe ledger가 아님 | H5-ORCH-016 Conversation service가 bounded history를 관리 |
| runtime-only durability | stores/planner 모두 durable하지 않음 | 별도 승인된 storage/transaction 설계 필요 |

# 다음 단계에서 반드시 참고할 내용

| 후속 단계 | 제공 model/test 계약 |
|---|---|
| H5-ORCH-015 | intent 결과는 Planner DTO를 바꾸지 않고 workflow event 후보만 정한다. |
| H5-ORCH-016 | Request latest-read/version, Registry snapshot, bounded history, validation/review을 읽은 뒤 `plan_next_fields()`를 호출하고 결과에 따라 machine dispatch를 한 번 수행한다. |
| H5-ORCH-018~020 | UI/API는 selected field/reasons를 표시할 수 있으나 form State 또는 Conversation workflow를 optimistic하게 직접 변경하지 않는다. |

# 다음 단계 수정이 예상되는 파일

- H5-ORCH-015 intent router와 focused tests
- H5-ORCH-016 orchestration service 및 focused tests
- H5-ORCH-018~020 UI/API integration tests

# 후속 개선 후보

H5-ORCH-016에서 only server latest reads를 조합하고 planner result를 H5-ORCH-012 event boundary에 전달하는 test를 추가한다. Durable multi-worker history/idempotency는 배포 요구가 확정된 뒤 별도 승인된 단계에서 설계한다.

# Roadmap 변경 필요 여부

없음. Worker는 Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 수정하지 않으며 Reviewer 검토를 대기한다.
