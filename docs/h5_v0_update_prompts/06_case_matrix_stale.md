# Stage 06 — Case Matrix와 stale 재생성

## 새 채팅에 붙여 넣을 프롬프트

```text
request_ai_agent_h5_v0의 Stage 06만 수행해 주세요.

AGENTS.md, docs/h5_v0_execution_handoff.md와 Stage 05 기록을 먼저 읽으세요. Stage 05가 완료되지 않았으면 구현하지 마세요.

Case Matrix를 조건조합의 생성 결과로 구현하세요.
- Matrix는 읽기 전용 검토 화면이다. Case 포함/제외, 상세 보기, 원본 조건 이동만 제공한다.
- 제품, Condition Set, 조합 포함 여부, 적용 제품, Case 포함 상태가 바뀌면 generation_status를 stale로 전환하고 원인을 보존한다.
- stale 화면은 이전 Matrix를 최신 결과처럼 표시하지 않고 원인, 원본 이동, Case 다시 생성 행동을 제공한다.
- 재생성 시 동일 case_signature의 Case ID와 포함/제외 상태만 유지한다. 서명이 달라진 새 Case에는 이전 제외 상태를 승계하지 않는다.
- Case 수에 따른 사용자 확인, 관리자 확인, Tier/숫자 구간 정책은 구현하지 않는다.
- stale 여부는 미리보기와 Word 생성을 차단하지 않는다. 다음 단계들이 stale 경고를 그대로 표현할 수 있는 State 계약만 제공한다.

Case engine, validator/progress, UI와 관련 최소 테스트만 변경·실행하세요. preview/Word는 구현하지 마세요. 결과를 인수인계에 기록하세요.
```

## 완료 기준

- 조건조합에서 생성된 Case만 Matrix에 표시된다.
- 변경→stale→재생성의 ID/포함 상태 규칙이 테스트로 검증된다.
