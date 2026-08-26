# h5_v0 오케스트레이터 단계 실행·재계획 문서

이 디렉터리는 h5_v0 워크플로 오케스트레이터의 단계별 구현과 재계획을 위한 단일 기준 문서 모음이다. 자동 Runner와 수동 단계 실행 모두 이 문서 체계를 사용한다.

새 채팅은 이전 대화를 알지 못한다고 가정한다. 다음 문서를 순서대로 읽으면 자동 Runner 또는 수동 단계 실행을 안전하게 시작할 수 있다.

1. `orchestrator_master_plan.md`
2. `orchestrator_roadmap.md`
3. `h5_orch_000_automation_preparation.md`
4. `prompts/common_stage_contract.md`
5. `prompts/baseline_prompts.md`
6. `automation/runner_policy.md`
7. `automation/reviewer_result.schema.json`
8. `NEW_CHAT_AUTONOMOUS_START.md`
9. `prompts/manual_stage_execution.md` (수동 실행 시)
10. `MANUAL_CHAT_START.md`, `prompts/current_stage.md` (현재 수동 실행 프롬프트)

## 현재 상태

- 준비 문서 버전: 1.1
- 실제 애플리케이션 코드 변경: 없음
- 자동화 Runner: 작업 트리에 구축됨. 현재 Codex 상태 DB 쓰기 권한 문제로 첫 Worker 실행 전 중단 기록이 있음.
- 실제 오케스트레이터 단계: `H5-ORCH-001` 조사 완료 기록이 작업 트리에 있음
- 현재 예정 단계: `H5-ORCH-002`

## 단일 진실 원천

- 전체 단계 상태와 의존관계: `orchestrator_roadmap.md`
- 단계별 최초 범위: `prompts/baseline_prompts.md`
- 모든 단계의 공통 안전 규칙: `prompts/common_stage_contract.md`
- 자동 진행·중단 결정 규칙: `automation/runner_policy.md`
- 실행 중 기계 상태: Runner가 생성할 `automation/automation_state.json`
- 수동 단계 실행·검토·다음 프롬프트 갱신 절차: `prompts/manual_stage_execution.md`
- 현재 단계 실행·검토·갱신 프롬프트: `MANUAL_CHAT_START.md`, `prompts/current_stage.md`, `prompts/review_current_stage.md`, `prompts/update_after_review.md`

완료된 단계의 사실은 해당 단계 인수인계 문서가 최우선이다. 최초 계획과 실제 코드가 다르면 실제 코드와 최신 인수인계 문서를 우선하고 Roadmap 변경 이력에 이유를 기록한다.

## 수동 단계 실행 방법

자동 Runner를 사용하지 않을 경우 `prompts/manual_stage_execution.md`의 순서대로 한 단계씩 진행한다. 각 단계에서 Worker 실행 후 독립 Reviewer가 Roadmap 상태와 다음 단계 프롬프트를 확정하며, Planner 역할은 그 갱신만 수행한다. 수동 방식에서도 기준 카드, 공통 계약, 인수인계 문서, 검증 및 중단 조건은 동일하게 적용한다.

## 자동 Runner 시작 방법

새 Codex 채팅의 작업 디렉터리를 이 저장소 루트로 설정하고 `NEW_CHAT_AUTONOMOUS_START.md`의 전체 내용을 첫 요청으로 전달한다.

해당 프롬프트는 다음을 한 번에 승인한다.

1. 자동화 Runner 구축
2. mock 단계로 Runner 검증
3. 검증 성공 시 실제 `H5-ORCH-001` 시작
4. 각 단계 종료 후 독립 Reviewer 실행
5. Roadmap과 다음 실행 프롬프트 자동 갱신
6. 중단 조건이 없으면 마지막 단계까지 계속 실행

자동 실행은 성공을 보장하지 않는다. `runner_policy.md`의 중단 조건, Codex 인증·사용량 제한, 테스트 환경 부족 또는 추가 권한 필요 상황에서는 안전하게 멈추고 재개 가능한 상태를 남겨야 한다.
