# Stage 07 — 상시 Agent와 단계 Summary

## 새 채팅에 붙여 넣을 프롬프트

```text
request_ai_agent_h5_v0의 Stage 07만 수행해 주세요.

AGENTS.md, docs/h5_v0_execution_handoff.md와 Stage 06 기록을 먼저 읽으세요. Stage 06이 완료되지 않았으면 구현하지 마세요.

우측 Agent만 h5_v0 계약에 맞춰 보강하세요.
- Agent는 모든 표준 단계에서 항상 표시한다. 별도 진입 버튼이나 별도 Workspace 전환은 만들지 않는다.
- 우측 Summary는 해석개요·제품형상·해석조건·조건조합·Case Matrix별 완료 수/전체 수, 입력 여부, 오류만 표시한다.
- Summary에는 실제 텍스트 값, 도면번호, Fan 값, 조건값을 반복하지 않는다.
- Agent 제안은 승인 전 State를 변경하지 않는다.
- 원본 Field, 해석유형, 조건 Snapshot, 조합 또는 Case generation이 바뀌어 오래된 제안이 되면 반영을 차단하고 무효화 사유와 새 제안 받기 행동을 제공한다.
- unknown, none, skipped의 의미를 구분하며 동일 질문을 반복하지 않는다.
- 사용자가 선택한 해석유형은 Agent가 자동 변경하지 않는다.
- PDB와 기류 도달 거리 관련 Agent 경로는 제거한다.

Agent 대화의 모델/RAG 구조를 리팩터링하거나 새 외부 의존성을 추가하지 마세요. 관련 proposal/UI 테스트만 실행하고 인수인계를 갱신하세요.
```

## 완료 기준

- Agent는 상시 표시되고 Summary에 실제 값이 없다.
- stale Proposal 반영이 차단된다.
