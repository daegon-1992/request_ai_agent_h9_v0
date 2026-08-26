# Stage 02 — 해석개요 State와 UI 계약

## 새 채팅에 붙여 넣을 프롬프트

```text
request_ai_agent_h5_v0의 Stage 02만 수행해 주세요.

AGENTS.md, docs/h5_v0_execution_handoff.md, Stage 01 기록을 먼저 읽으세요. Stage 01이 완료되지 않았으면 구현하지 마세요.

해석개요만 h5_v0 결정으로 전환하세요. 기존 h3 저장본 migration은 구현하지 않습니다.
- project_name의 화면 문구를 프로젝트명(PMS)로 쓴다.
- grade 키를 development_grade로 바꾸고 개발 등급으로 표시한다.
- model_suffix의 문구를 모델명(Model Suffix)로 바꾼다.
- request_date의 문구를 의뢰 요청일로 바꾼다.
- due_date 키를 desired_completion_date로 바꾸고 희망 완료일로 표시한다.
- background, purpose, goal, deliverables 입력을 제거한다.
- request_description, decision_use, additional_result_request를 추가한다.
- 해석 결과 안내는 선택 해석유형의 Master에서 읽기 전용으로 표시한다. 안내 조회 실패는 재시도 안내만 보이고 완료·검증을 차단하지 않는다.
- pms_group, platform, analysis_type은 해석개요 원본에서 제거하고 request_context의 제품군, Platform, 해석유형만 사용한다.
- 요청 내용 완료율은 request_description과 유효한 decision_use를 기준으로 계산한다. additional_result_request와 결과 안내는 완료율 분모에 넣지 않는다.

기존 h3 저장본, 과거 key 호환, 자동 제목, 제출 흐름을 되살리지 마세요. State, validator, 진행률, UI, 최소 회귀 테스트를 이 계약에 맞춰 함께 변경하세요. 해당 테스트와 인코딩/diff 검사만 실행하고 인수인계를 갱신하세요.
```

## 완료 기준

- 해석개요에 과거 배경·목적·목표·산출물 입력이 없다.
- 새 요청 내용 필드와 Context 분리가 State·UI·진행률에서 일치한다.
