# 단계 정보

- 단계 ID: H5-ORCH-000
- 단계명: 자동화 실행 준비 문서 구성
- 수행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 Commit: `252ccb9`
- Roadmap 버전: 0.1
- 작업 상태: 완료

# 이번 단계 목표

새 Codex 채팅이 이전 대화 없이도 자동화 Runner를 구축하고, mock 검증 성공 후 실제 H5-ORCH-001부터 최종 단계까지 자동 진행할 수 있는 파일 기반 준비 상태를 만든다.

# 실제 수행 내용

- 전체 목표와 안전 원칙 문서화
- 32단계 Roadmap 초기화
- 32개 단계별 기준 카드 작성
- 완성형 프롬프트 생성용 공통 실행 계약 작성
- Worker–Reviewer–Planner 자동 진행 정책 작성
- Reviewer 구조화 결과 JSON Schema 작성
- 자동화 상태 예제 작성
- 새 채팅에서 사용할 단일 build-and-run 프롬프트 작성
- 최소 및 권장 모델 프로필과 `codex exec`별 동적 선택 계약 작성

# 변경 파일

| 파일 | 변경 내용 |
|---|---|
| `docs/orchestrator_handoff/README.md` | 준비 문서 진입점 |
| `docs/orchestrator_handoff/orchestrator_master_plan.md` | 전체 목표와 공통 설계 원칙 |
| `docs/orchestrator_handoff/orchestrator_roadmap.md` | 001~032 초기 Roadmap |
| `docs/orchestrator_handoff/prompts/common_stage_contract.md` | 모든 단계의 공통 실행 계약 |
| `docs/orchestrator_handoff/prompts/baseline_prompts.md` | 32개 단계별 기준 카드 |
| `docs/orchestrator_handoff/automation/runner_policy.md` | 자동 진행·보완·중단 정책과 모델 프로필 |
| `docs/orchestrator_handoff/automation/reviewer_result.schema.json` | Reviewer 결과 Schema |
| `docs/orchestrator_handoff/automation/automation_state.example.json` | 초기 실행 상태 예제 |
| `docs/orchestrator_handoff/NEW_CHAT_AUTONOMOUS_START.md` | 새 채팅 단일 실행 프롬프트 |

# 신규 또는 변경된 데이터 구조

애플리케이션 데이터 구조 변경은 없다. 자동화 준비용 Reviewer 결과와 Runner 상태 문서 계약만 추가했다.

# 신규 또는 변경된 API

없음.

# 중요 설계 결정

- 대화 기록 대신 저장소 문서를 자동화의 지속 가능한 Context로 사용한다.
- Worker와 Reviewer를 별도 Codex 세션으로 실행한다.
- Reviewer만 단계 완료와 자동 계속 여부를 확정한다.
- 최초 32단계 프롬프트는 고정 실행문이 아니라 재계획 가능한 기준 카드로 저장한다.
- 실제 단계 실행 전에 mock 단계로 Runner를 검증한다.
- mock 성공 후 별도 사용자 요청 없이 실제 001을 시작하도록 시작 프롬프트에서 명시적으로 승인한다.
- 추가 권한, 데이터 손실, 승인 우회 또는 핵심 검증 불가 상황에서는 자동 중단한다.

# 수행하지 않은 작업

- 자동화 Runner 구현
- mock Runner 실행
- 실제 H5-ORCH-001 실행
- 애플리케이션 코드 조사 또는 수정

# 최소 검증

| 검증 항목 | 결과 |
|---|---|
| Roadmap 단계 수 | 32개 |
| 기준 카드 단계 수 | 32개 |
| JSON 파일 구문 | 정상 |
| 필수 참조 파일 존재 | 정상 |
| `python tools/check_encoding.py --changed` | 통과 |
| `git diff --check` | 통과 |

# 알려진 문제와 제한사항

- 현재 설치된 Codex CLI는 `0.146.0-alpha.3`이다. Runner 구축 시 실제 model 및 reasoning 설정 지원값을 다시 확인해야 한다.
- 저장소에는 이번 작업과 무관한 `__pycache__` 미추적 파일이 있으며 수정하거나 삭제하지 않았다.
- Codex 인증, 사용량 한도, 네트워크 및 관리 정책에 따라 무인 실행이 중단될 수 있다.
- 준비 문서는 자동 실행을 가능하게 하지만 최종 완료 자체를 보장하지 않는다.

# 다음 단계에서 반드시 참고할 내용

- 새 채팅은 `NEW_CHAT_AUTONOMOUS_START.md` 전체를 첫 요청으로 사용한다.
- Runner 구축과 mock 검증 전에는 실제 H5-ORCH-001을 실행하지 않는다.
- mock 검증이 모두 통과하면 같은 자동화 흐름에서 실제 001을 시작한다.
- 각 Worker·Reviewer·Planner 호출은 부모 채팅 모델을 상속하지 않고 선택 모델과 reasoning을 명시해야 한다.

# 다음 단계 수정이 예상되는 파일

- Runner가 선택하는 전용 도구 디렉터리
- `docs/orchestrator_handoff/automation/automation_state.json`
- `docs/orchestrator_handoff/prompts/current_stage.md`
- `docs/orchestrator_handoff/prompts/next_stage.md`
- Runner 전용 `model_profiles.json`
- `docs/orchestrator_handoff/runs/`
- `docs/orchestrator_handoff/reviews/`

# 후속 개선 후보

- 단계별 실제 사용량 집계
- 모델 프로필별 성공률 비교
- 실패한 단계의 안전한 재시도 정책 정교화
- 장기 실행 로그 보존 기간 설정
