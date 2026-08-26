# Stage 03 — 해석 제품 모델

## 새 채팅에 붙여 넣을 프롬프트

```text
request_ai_agent_h5_v0의 Stage 03만 수행해 주세요.

AGENTS.md, docs/h5_v0_execution_handoff.md와 Stage 02 기록을 먼저 읽으세요. Stage 02가 완료되지 않았으면 구현하지 마세요.

제품형상만 새 canonical 구조로 전환하세요.
- Base 제품은 정확히 1개, 비교 제품은 0..N이다.
- 각 제품은 안정적 geometry_id, 도면번호, 선택 표시명, 역할(base/comparison)을 가진다.
- 비교 제품은 Base 제품 대비 형상 차이를 가진다.
- 비교 제품 추가 한 번은 빈 제품 카드 정확히 1개만 만든다.
- h3 카드 스타일과 입력 밀도는 유지한다.
- 기존 Base/Variant, has_changed_part, base_parts, parts, changed_from_part는 새 UI·Case 원본으로 사용하지 않는다. 기존 저장본 migration도 구현하지 않는다.
- 미등록 제품 조합이나 부품 조립 기반 제품을 자동 생성하지 않는다.

새 제품 원본을 사용하는 최소 State/validator/progress 계약과 테스트를 함께 변경하세요. 조건조합, Case 생성, Word는 다음 단계에서 변경하므로 이 단계에서 구현하지 마세요. 검증 결과와 다음 단계 영향 사항을 인수인계에 기록하세요.
```

## 완료 기준

- 기준 1개와 비교 0..N 카드가 UI·State에서 일치한다.
- 기존 Base/Variant가 새 화면과 완료율의 원본이 아니다.
