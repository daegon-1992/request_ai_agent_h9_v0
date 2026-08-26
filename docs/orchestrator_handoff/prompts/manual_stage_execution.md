# H5-ORCH 수동 단계 실행·재계획 절차

자동 Runner를 사용하지 않고 한 단계씩 실행할 때의 표준 절차다. 이 문서는 최초 단계별 기준 카드를 실제 결과에 따라 갱신 가능한 실행 프롬프트로 바꾸기 위한 것이다.

## 기준과 우선순위

1. `AGENTS.md`
2. `orchestrator_master_plan.md`
3. `orchestrator_roadmap.md`
4. 완료된 단계의 인수인계 문서와 실제 코드·테스트 결과
5. `common_stage_contract.md`
6. `baseline_prompts.md`

상위 문서와 실제 결과가 충돌하면 범위를 추측하여 넓히지 않는다. Roadmap 변경 이력에 근거를 기록하고, 사용자 결정 또는 안전 중단 조건에 해당하면 중단한다.

## 한 단계의 수동 실행 순서

1. Roadmap에서 선행 조건을 충족한 현재 단계를 고른다.
2. 기준 카드와 공통 계약, 필요한 인수인계 문서로 Worker 실행 프롬프트를 만든다.
3. Worker가 구현·검증·인수인계 문서를 작성한다. Worker는 Roadmap 완료 상태를 확정하지 않는다.
4. 별도 Reviewer 요청으로 실제 diff, 테스트, 완료 조건, State 안전성, 인수인계 정확성을 검토한다.
5. Reviewer가 `safe_to_continue=true`를 명시한 경우에만 Planner 요청으로 Roadmap과 미완료 단계 프롬프트를 갱신한다.
6. 갱신된 다음 단계 최종 프롬프트를 확인한 뒤 사용자가 다음 Worker 실행을 시작한다.

## Worker 실행 프롬프트 양식

```text
H5-ORCH-<ID>를 실행하라.

먼저 AGENTS.md, orchestrator_roadmap.md, prompts/common_stage_contract.md,
prompts/baseline_prompts.md 및 이 단계의 선행 인수인계 문서를 읽어라.

현재 단계의 기준 카드를 최신 실제 코드와 완료된 인수인계 문서에 맞게 구체화하되,
이번 단계의 범위 밖 기능은 구현하지 마라. 공통 계약의 안전 원칙, 수정 금지 범위,
검증 및 중단 조건을 따른다.

완료 시 지정된 인수인계 문서를 작성하고 Worker 결과 보고서에 변경 파일, 검증 결과,
미해결 위험, 다음 단계 영향, Git 상태를 기록하라. Roadmap 상태나 다음 단계 프롬프트는
확정하지 말고 Reviewer 검토 대기로 남겨라.
```

## Reviewer 실행 프롬프트 양식

```text
H5-ORCH-<ID> Worker 결과를 독립적으로 검토하라.

AGENTS.md, 최신 Roadmap, 기준 카드, 공통 계약, Worker 인수인계 문서, 실제 git diff 및
테스트 결과를 직접 비교하라. Worker 보고만 신뢰하지 마라.

완료 조건, 필수 검증, 기존 UI/API 호환성, Request State 직접 변경 금지, Request version과
stale/중복 Proposal 처리, Conversation과 Request 분리, 조건부 필드 데이터 유실 위험을
확인하라.

결과에 다음을 명시하라: approved/rejected, safe_to_continue=true/false, 근거, 필수 보완,
Roadmap 상태, 다음 단계 선행 조건. Roadmap과 다음 프롬프트의 실제 갱신은 하지 마라.
```

## Planner·프롬프트 갱신 프롬프트 양식

```text
H5-ORCH-<ID>의 Reviewer 결과가 safe_to_continue=true인지 먼저 확인하라.
false이면 Roadmap을 중단 또는 부분 완료 상태로만 갱신하고, 필요한 사용자 결정 또는
최소 보완 작업을 보고하라.

true이면 최신 Roadmap, 해당 단계 인수인계 문서, Reviewer 결과, 실제 diff·테스트 결과를
기준으로 다음을 수행하라.
1. 해당 단계의 상태와 Roadmap 변경 이력을 갱신한다.
2. 이후 미완료 단계 중 실제 결과의 영향을 받는 단계만 식별한다.
3. 영향을 받는 기준 카드를 최신 실행 프롬프트로 구체화한다.
4. 새 보완 단계가 안전하고 필요한 경우에만 보조 ID(예: 017A)를 추가하고 근거를 남긴다.
5. 완료된 단계 ID·결과는 변경하지 않는다.
6. 다음에 실행할 단계 ID, 최종 Worker 프롬프트, 선행 조건과 검증 명령을 제시한다.

사용자 결정, DB migration, API 호환성 파괴, 데이터 손실 위험, 추가 권한, 요구사항 충돌은
자동 결정하지 말고 중단 사유로 기록한다.
```

## 수동 진행의 중단 기준

`common_stage_contract.md`의 중단 조건에 더해, Reviewer가 거절했거나 인수인계 문서·필수 검증·Roadmap 갱신 중 하나가 빠진 경우 다음 단계 Worker를 시작하지 않는다. Codex 실행 환경 권한 문제는 모델을 낮춰 해결하려 하지 말고 원인을 기록한 뒤 환경을 바로잡은 후 재개한다.
