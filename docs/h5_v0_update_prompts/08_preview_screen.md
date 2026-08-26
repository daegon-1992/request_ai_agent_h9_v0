# Stage 08 — 실제 화면 기반 미리보기

## 새 채팅에 붙여 넣을 프롬프트

```text
request_ai_agent_h5_v0의 Stage 08만 수행해 주세요.

AGENTS.md, docs/h5_v0_execution_handoff.md와 Stage 07 기록을 먼저 읽으세요. Stage 07이 완료되지 않았으면 구현하지 마세요.

제출 기능과 무관한 미리보기 화면을 구현하세요.
- 상단 우측 미리보기 버튼으로 중앙 영역을 미리보기 화면으로 전환한다. 우측 Agent는 유지한다.
- 미리보기는 현재 화면 State를 사람이 읽는 의뢰서 섹션·표로 렌더링한다.
- 렌더링 항목은 새 해석개요, 해석 제품, 조건 카드, 조건조합, Case Matrix다.
- Matrix가 stale이면 이전 Case를 최종 결과처럼 쓰지 말고 stale 원인과 재생성 필요 안내를 미리보기에 표시한다.
- 이 단계에서 preview_document라는 별도 State 계약, 제출 검증, 임시저장, 최종확인 State를 만들지 않는다.
- 미리보기의 DOM 구조는 다음 Stage의 Word export가 그대로 직렬화할 수 있도록 안정적 section/label/value/table 식별자를 둔다.

기존 비활성 preview API를 재활용할 필요가 없다면 제거하지 말고 호출하지 마세요. UI 중심 최소 테스트와 인코딩/diff 검사만 실행하고 인수인계를 갱신하세요.
```

## 완료 기준

- 미리보기는 현재 화면 정보와 Matrix stale 경고를 중앙에 표시한다.
- 별도 preview_document State가 생성되지 않는다.
