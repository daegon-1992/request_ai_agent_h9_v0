# h5_v0 오케스트레이터 자동화 Runner 구축 및 전체 단계 자동 실행

이 채팅은 이전 대화 컨텍스트를 공유하지 않는다. 현재 작업 디렉터리는 h5_v0 저장소 루트여야 한다.

## 1. 기준 문서

다음 문서를 순서대로 읽고 이 작업의 단일 기준으로 사용하라.

1. `AGENTS.md`
2. `docs/orchestrator_handoff/README.md`
3. `docs/orchestrator_handoff/orchestrator_master_plan.md`
4. `docs/orchestrator_handoff/orchestrator_roadmap.md`
5. `docs/orchestrator_handoff/prompts/common_stage_contract.md`
6. `docs/orchestrator_handoff/prompts/baseline_prompts.md`
7. `docs/orchestrator_handoff/automation/runner_policy.md`
8. `docs/orchestrator_handoff/automation/reviewer_result.schema.json`
9. `docs/orchestrator_handoff/automation/automation_state.example.json`

파일이 누락되거나 서로 모순되면 임의로 복구하지 말고 중단 사유를 보고하라.

## 2. 전체 권한과 목표

이번 요청은 다음 전체 흐름을 한 번에 수행하도록 명시적으로 승인한다.

1. Codex CLI `codex exec` 기반 자동화 Runner 구축
2. mock 단계로 Runner 안전성 검증
3. mock 검증 성공 시 실제 `H5-ORCH-001` 자동 시작
4. 각 단계마다 별도 Worker 실행
5. 각 Worker 종료 후 별도 Reviewer 실행
6. Reviewer 결과에 따라 Roadmap과 다음 프롬프트 자동 갱신
7. 작고 안전한 누락은 보조 단계로 자동 보완
8. 중단 조건이 없으면 `H5-ORCH-032`와 최종 완료 검토까지 계속 실행
9. 완료 후 최종 요약과 잔여 backlog 작성

단계마다 사용자에게 계속 여부를 묻지 마라. 안전한 로컬 코드 수정, 문서 작성, 직접 테스트와 제한적 Smoke Test는 계속 수행하라.

이 권한은 `runner_policy.md`의 중단 조건을 무시하거나 외부·파괴적 작업을 허용하지 않는다.

## 3. Runner 구현 요구사항

Windows PowerShell에서 실행 가능하게 구현한다.

Runner는 다음을 수행해야 한다.

- Roadmap에서 다음 실행 가능 단계를 결정
- 부모 채팅 또는 전역 기본 모델에 의존하지 않고 각 `codex exec`에 model과 reasoning을 명시
- 역할·단계별 모델 선택을 전용 `model_profiles.json`으로 관리
- 각 실행 결과에 실제 사용한 model과 reasoning 기록
- 공통 단계 계약과 최신 단계 카드를 결합해 완성형 Worker 프롬프트 생성
- 최신 선행 인수인계 문서를 프롬프트 입력에 포함
- Worker를 새로운 `codex exec` 세션으로 실행
- Worker final message, 실행 ID, 변경 파일, 테스트 결과 저장
- 별도의 Reviewer를 새로운 `codex exec` 세션으로 실행
- Reviewer 결과를 `reviewer_result.schema.json`으로 검증
- Reviewer가 실제 diff와 테스트 근거를 확인하게 함
- Roadmap 버전과 상태 및 변경 이력을 갱신
- 다음 단계 프롬프트를 실제 결과에 맞게 재작성
- 중단 조건이 없으면 다음 단계 실행
- 중단·종료 후 재실행하면 마지막 안전 체크포인트부터 재개
- lock을 사용해 동일 Runner 또는 단계 중복 실행 방지

Runner 소스, 프롬프트, Schema, 상태, 로그와 결과는 저장소 내부의 명확한 전용 디렉터리에 둔다.

## 4. 안전 설정

- 기본 sandbox는 `workspace-write`
- `danger-full-access` 및 승인·sandbox 우회 플래그 금지
- workspace 외부 쓰기 금지
- 자동 push·배포·force 작업 금지
- 사용자 기존 변경 보존
- destructive Git 명령 금지
- 비밀값을 로그·프롬프트·결과에 저장하지 않음
- 동시 Worker 실행 금지
- Worker 자기 완료 판정만으로 자동 진행 금지
- Reviewer와 Worker 세션 분리
- 같은 실패는 제한 횟수 후 중단

프로젝트 `AGENTS.md`의 검증 및 Commit 규칙을 따른다.

## 5. 모델 설정

기본적으로 `runner_policy.md`의 권장 혼합 프로필을 사용하라.

- 일반 Worker: `gpt-5.6-terra`, reasoning `high`
- 조사·단순 연결 Worker: `gpt-5.6-terra`, reasoning `medium`
- 설계·State 안전·통합 Worker: `gpt-5.6-sol`, reasoning `high`
- Reviewer: `gpt-5.6-sol`, reasoning `high`
- Planner: `gpt-5.6-terra`, reasoning `medium`
- 반복 실패 또는 치명적 안전 검토 1회: `gpt-5.6-sol`, reasoning `xhigh`

사용 가능한 Codex CLI 모델명 또는 reasoning 설정이 위 값과 다르면 자동으로 다른 모델을 선택하지 말고 실제 지원 값을 확인하라. 권장 모델을 사용할 수 없으면 최소 프로필까지 하향할 수 있다. 최소 프로필도 사용할 수 없으면 중단한다.

각 실행은 개념적으로 다음 인자를 포함해야 한다.

```text
codex exec --model <선택 모델> -c model_reasoning_effort=<선택 effort> ...
```

모델 미지원 오류가 발생했을 때 Codex 기본 모델로 조용히 fallback하지 마라.

## 6. 구축 순서

1. 기준 문서와 Git 상태 확인
2. 설치된 Codex CLI의 `exec`, model, reasoning 설정 지원 여부 확인
3. Runner·Worker prompt·Reviewer prompt·상태 파일 구현
4. 문서만 수정하는 mock 단계 2개 준비
5. 다음 mock 시나리오 검증
   - 정상 완료 후 자동 진행
   - 부분 완료 후 보완 단계 삽입
   - blocked 판정 시 중단
   - Reviewer JSON 오류 처리
   - 인수인계 누락 시 중단
   - Runner 재실행 시 checkpoint 재개
   - 동일 단계 중복 실행 방지
6. mock 실행 산출물이 실제 Roadmap을 변경하지 않았는지 확인
7. 모든 mock 검증이 통과하면 실제 실행 상태를 `READY`로 전환
8. 실제 `H5-ORCH-001` 시작
9. 중단 조건이 없으면 마지막 단계까지 자동 반복
10. 전체 완료 검토와 최종 보고서 생성

## 7. 자동 중단

`runner_policy.md`의 강제 중단 조건이 발생하면 즉시 다음을 수행하라.

1. 진행 중인 추가 실행 중지
2. 변경을 되돌리지 않고 현재 상태 보존
3. 마지막 안전 체크포인트 기록
4. 중단 이유와 재개 조건 기록
5. 안전한 재개 명령 작성
6. 사용자에게 필요한 단 하나의 결정을 명확히 보고

## 8. 완료 조건

다음을 모두 만족해야 전체 완료다.

- 실제 Roadmap의 모든 필수 단계가 완료 또는 근거 있는 대체·삭제 상태
- 사용자 사용 가능 MVP 검증 통과
- 승인 전 State 불변 검증
- stale·중복 승인 방지 검증
- 조건부 필드 데이터 유실 방지 검증
- 기존 폼·API·Case Matrix·Validation·Preview·Word·RAG 경로 호환 확인
- 핵심 회귀 검증 완료
- 치명적 미해결 결함 없음
- 모든 단계 인수인계 문서와 최종 Roadmap 갱신
- 최종 자동화 실행 보고서 작성

단순히 032 Worker가 실행되었다는 이유로 완료 처리하지 마라. 마지막 독립 Reviewer가 전체 완료 조건을 다시 판정해야 한다.

## 9. 결과 보고

Runner 구축 결과, mock 검증 결과, 실제 단계 진행 현황, 자동 중단 여부, 최종 완료 여부, 변경 파일, 테스트, Commit, 잔여 위험과 재개 방법을 보고하라.
