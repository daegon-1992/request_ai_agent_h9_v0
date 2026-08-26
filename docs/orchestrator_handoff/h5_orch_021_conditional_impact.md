# H5-ORCH-021 조건부 필드 영향 안내

## 단계 정보

- 단계 ID: `H5-ORCH-021`
- 상태: Worker 완료, Reviewer 검토 대기
- 프로젝트 루트: `request_ai_agent_h5_v0`
- 기준선: `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply -> latest GET sync`
- Roadmap, 기준 카드 및 다음 단계 프롬프트는 변경하지 않았다.

## 선택한 기존 authority

조건부 필드의 activation과 required 여부는 서버가 State에 기록한 기존
`request_context.condition_fieldset_snapshot`만 사용한다. 이 snapshot은 기존
Fieldset 결과이며, 값 표시는 동일한 서버 latest State의 기존
`conditions.condition_sets`를 읽기 전용으로 참조한다. UI는 Fieldset, Field
Registry, validator, Case Matrix, Preview 또는 Word 규칙을 복제하거나 대체하지
않는다.

`orchestratorPanelState.latestApprovedState`에는 이미 승인 latest-read로 채택된
서버 상태의 복사본만 보관한다. 따라서 이후의 legacy form draft 편집은 다음
영향 비교의 기준이 되지 않는다.

## approved-only 영향 경계

Proposal decision 응답이 해당 서버 Proposal id의 `approved`이고, 이어진 기존
`GET /api/request/versioned/<panel-local request_id>`가 유효한 `state`와
`request_version`을 반환한 경우에만 다음 순서로 동작한다.

GET 응답은 panel-local server `request_id`가 일치하고 숫자 `request_version` 및
기존 canonical State의 object section(`metadata`, `request_context`, `basic_info`,
`analysis_overview`, `geometry`, `conditions`, `case_matrix`, `review`,
`legacy_internal`)을 모두 가져야
한다. 빈 State 또는 section 누락 State는 malformed로 거부한다. 이 검사는
renderer 안전 경계일 뿐 Fieldset/Registry/validator 규칙을 복제하지 않는다.

1. GET의 State/version을 기존 form 및 Fieldset 렌더 경로에 채택한다.
2. 이전의 승인 latest-read snapshot과 이번 GET State의 authoritative Fieldset
   결과를 비교한다.
3. 읽기 전용 한국어 안내로 활성화, 비활성화, 새 필수 입력, 값이 있는
   비활성화의 보존 안내를 panel log에 표시한다.

첫 승인 latest-read에는 이전 서버 기준이 없으므로 영향 안내를 만들지 않고,
그 GET State만 다음 승인 sync의 기준으로 저장한다. pending diff, Proposal
operation, client draft, cached approval result는 영향 계산 authority가 아니다.

## 값 보존 규칙과 오류 경계

비활성 전환 전의 Fieldset 활성 값이 있으면 `값 보존 안내`에 해당 값을 표시하고
`자동으로 삭제하거나 정리하지 않습니다.`라고 안내한다. 이 UI 코드는 State,
version, Proposal, Conversation, workflow를 쓰지 않으며 값을 삭제·정리·정규화하지
않는다.

`pending`, `rejected`, `expired`, `conflicted`, `failed`, `unknown`, replay,
malformed/network decision 결과, malformed latest GET 및 GET 실패는 영향 안내,
form sync, Fieldset 재계산을 수행하지 않는다. GET 실패 뒤에는 cached/client
데이터를 채택하지 않는다. H5-018~020의 Request id, decision double-click guard,
loading, close/reopen 및 legacy chat/form 격리는 유지된다.

## 변경 파일

- `request_ai_agent_h5_v0/ui.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py`
- `request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py`
- `docs/orchestrator_handoff/h5_orch_021_conditional_impact.md`

## focused 검증

새 UI mock은 서버 Fieldset snapshot의 activation/required 결과로 활성화,
비활성화, 새 필수 입력과 값이 있는 비활성화 보존 안내를 확인한다. 또한
rejected 및 malformed approved/latest-read(빈 State와 필수 section 누락 State 포함)
경로가 안내·form sync·derived render를 수행하지 않음을 확인한다. 기존 H5-020 mock은 pending/rejected/conflicted/unknown,
decision/network/GET failure의 no-sync와 approved GET exact-once를 계속 확인한다.

```powershell
& ..\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_orchestrator_conditional_impact.py request_ai_agent_h5_v0/tests/test_orchestrator_mvp_sync.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_ui.py request_ai_agent_h5_v0/tests/test_orchestrator_chat_panel.py request_ai_agent_h5_v0/tests/test_orchestrator_backend_vertical_slice.py request_ai_agent_h5_v0/tests/test_orchestrator_request_version.py request_ai_agent_h5_v0/tests/test_orchestrator_proposal_store.py
python tools/check_encoding.py --changed
git diff --check
```

실제 pytest 결과: `63 passed in 1.73s`.

## H5-022~023 경계와 runtime 한계

이 단계는 clarification, correction, undo, next-question/message, workflow dispatch를
추가하지 않는다. Request, Conversation, Proposal은 계속 process-local runtime-only
store다. 재시작 또는 multi-worker 환경에서는 shared identity, durable transaction/CAS,
durable exactly-once를 제공하지 않는다. `latestApprovedState`와 refresh guard도 panel
runtime 한정이다.

## Worker 보고

승인 server latest-read 이후에만 기존 Fieldset snapshot을 비교하는 읽기 전용 조건부
필드 영향 안내를 추가했다. 값 있는 비활성 필드는 자동 삭제하지 않는다는 보존 안내만
표시하며, 기존 lifecycle과 form renderer의 authority를 변경하지 않았다. Roadmap과
다음 프롬프트는 수정하지 않고 Reviewer 검토 대기로 남긴다.
