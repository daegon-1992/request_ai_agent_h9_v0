# H5-ORCH 자동화 Runner 정책

## 1. 목적

Worker 실행, 독립 Reviewer 검토, Roadmap 재계획과 다음 단계 실행을 사용자 반복 요청 없이 연결한다.

## 2. 실행 상태 머신

```text
NOT_BUILT
→ MOCK_VALIDATING
→ READY
→ RUNNING_WORKER
→ RUNNING_REVIEWER
→ REPLANNING
→ RUNNING_WORKER
...
→ COMPLETE

어느 상태에서든 안전 문제 발생
→ BLOCKED
```

## 3. Worker와 Reviewer 분리

- Worker는 한 단계의 구현·테스트·인수인계만 담당한다.
- Worker는 자신의 단계를 Roadmap에서 `완료`로 확정하지 않는다.
- Reviewer는 Worker 결과, 실제 diff, 테스트 결과, 인수인계 문서를 확인한다.
- Reviewer만 `continue`, `repair`, `blocked`, `complete`를 판정한다.
- Planner 역할은 Reviewer 결과에 따라 Roadmap과 다음 프롬프트를 갱신한다.

각 역할은 새로운 `codex exec` 세션으로 실행한다.

## 4. 자동 계속 조건

다음을 모두 만족할 때만 다음 단계를 실행한다.

- Reviewer `safe_to_continue=true`
- Reviewer decision이 `continue` 또는 안전한 `repair`
- 필수 인수인계 문서 존재
- 필수 테스트가 통과했거나 단계 성격상 미실행 사유가 타당함
- Roadmap 갱신 성공
- 다음 완성형 프롬프트 생성 성공
- 승인 우회, State 손상, 호환성 파괴 위험 없음
- 사용자 기존 변경과 충돌 없음
- 자동 실행 한도 미초과

## 5. 보완 단계

작고 안전한 누락은 `017A` 같은 보조 단계로 자동 삽입할 수 있다.

다음 경우 자동 보완을 허용한다.

- 수정 범위가 현재 또는 바로 다음 단계 책임 안에 있음
- 데이터 migration이 없음
- 기존 API를 파괴하지 않음
- 새 사용자 선택이 필요하지 않음
- 직접 테스트로 완료 여부를 확인할 수 있음

보완 단계는 최대 2회까지만 자동 재시도한다.

## 6. 강제 중단 조건

- 승인 전 Request State 변경 발견
- Request version 원자성 미보장
- stale 또는 중복 Proposal 적용 가능성
- 조건부 필드 데이터 유실 가능성
- 기존 API 또는 저장 형식의 파괴적 변경 필요
- DB migration 또는 실제 데이터 변환 필요
- 사용자의 기존 변경과 충돌
- workspace 밖 쓰기 또는 추가 권한 필요
- destructive command, commit history 변경, push, 배포 필요
- 비밀값 또는 인증정보 필요
- 테스트 환경 부족으로 핵심 안전 검증 불가
- 같은 단계 또는 보완 단계가 2회 연속 실패
- Worker 결과와 실제 diff가 일치하지 않음
- Reviewer 출력 Schema 오류가 재시도 후에도 지속
- Roadmap 또는 다음 프롬프트 갱신 실패
- Codex 인증·사용량·rate limit·네트워크 문제
- 작업이 최초 목표를 넘어서는 대규모 리팩터링으로 확대

## 7. 중단 시 산출물

Runner는 다음을 기록하고 종료한다.

- 마지막 안전 체크포인트
- 현재 단계와 상태
- 중단 이유
- 마지막 Worker/Reviewer 실행 ID
- 변경 파일
- 통과·실패한 테스트
- 재개 전 필요한 사용자 결정 또는 외부 조건
- 안전한 재개 명령

## 8. Git 정책

- 기존 사용자 변경을 되돌리거나 포함하지 않는다.
- `git reset`, `git checkout --`, force push를 사용하지 않는다.
- 자동 push와 배포를 하지 않는다.
- 프로젝트 `AGENTS.md`의 Commit 규칙을 따른다.
- Commit할 경우 해당 단계 파일만 명시적으로 포함하고 실행 ID와 단계 ID를 기록한다.
- Commit 실패가 코드 안전성 문제이면 중단하고, 단순 Git 설정 문제이면 변경을 보존한 채 중단한다.

## 9. 권한 정책

- 기본 sandbox: `workspace-write`
- `danger-full-access` 금지
- 자동 승인 우회 플래그 금지
- 네트워크와 workspace 외부 접근은 기본 금지
- 추가 권한이 필요하면 Runner는 `BLOCKED`로 종료

## 10. 실행 한도

초기 기본값:

- 단계당 Worker 재시도: 1회
- 단계당 Reviewer Schema 재시도: 1회
- 자동 보완 단계: 원단계당 최대 2개
- 연속 실패 허용: 2회 미만
- 동시 Worker 실행: 1개
- 동시 Reviewer 실행: 1개

독립 단계의 병렬 실행은 초기 버전에서 사용하지 않는다.

## 11. 모델 프로필

Runner는 부모 채팅이나 사용자 전역 기본 모델에 의존하지 않는다. 모든 Worker, Reviewer, Planner `codex exec` 호출에 모델과 reasoning을 명시적으로 전달한다.

PowerShell 호출 형태:

```powershell
& codex exec `
  --model $selectedModel `
  -c "model_reasoning_effort=$selectedReasoning" `
  --sandbox workspace-write `
  --cd $projectRoot `
  $prompt
```

Runner는 전용 `model_profiles.json`을 생성하고 역할·단계별 선택을 데이터로 관리해야 한다. 각 실행 결과에 실제 선택한 model과 reasoning을 기록한다.

선택 우선순위:

1. 단계 카드와 현재 Roadmap에서 위험 등급 결정
2. 역할별 권장 프로필 선택
3. 설치된 Codex CLI와 계정에서 model/effort 사용 가능 여부 확인
4. 권장값을 사용할 수 없으면 최소 프로필로 명시적 fallback
5. 최소 프로필도 사용할 수 없으면 자동 중단

모델 미지원 오류가 발생했을 때 Codex 기본 모델로 조용히 재실행해서는 안 된다.

### 최소 프로필

- Worker: `gpt-5.6-terra`, reasoning `medium`
- Reviewer: `gpt-5.6-terra`, reasoning `medium`
- Planner: `gpt-5.6-terra`, reasoning `medium`
- 안전 핵심 단계 007~009, 016~017, 020~021, 024, 030~032: reasoning `high`

### 권장 혼합 프로필

- 일반 Worker: `gpt-5.6-terra`, reasoning `high`
- 조사·단순 연결 Worker: `gpt-5.6-terra`, reasoning `medium`
- 설계·State 안전·통합 Worker: `gpt-5.6-sol`, reasoning `high`
- Reviewer: `gpt-5.6-sol`, reasoning `high`
- Planner: `gpt-5.6-terra`, reasoning `medium`
- 반복 실패 또는 치명적 안전 검토 1회: `gpt-5.6-sol`, reasoning `xhigh`

현재 Codex CLI의 `model_reasoning_effort` 공식 설정 범위는 `minimal`, `low`, `medium`, `high`, `xhigh`다. API 모델이 별도의 더 높은 effort를 지원하더라도 이 Runner에서는 CLI가 공식적으로 지원하는 범위를 넘기지 않는다.

공식 기준:

- 모델 선택: https://developers.openai.com/api/docs/models
- GPT-5.6 모델 가이드: https://developers.openai.com/api/docs/guides/latest-model
- Codex 비대화형 실행: https://developers.openai.com/codex/noninteractive
