# Stage 00 — 기준선 확인과 작업 범위 고정

## 새 채팅에 붙여 넣을 프롬프트

```text
request_ai_agent_h5_v0의 Stage 00만 수행해 주세요.

먼저 프로젝트 루트의 AGENTS.md, docs/h5_v0_execution_handoff.md, docs/h5_v0_update_prompts/README.md를 읽으세요. 이후 현재 h5_v0 구현의 기준선을 읽기 전용으로 조사하고, docs/h5_v0_execution_handoff.md의 Stage 00 작업 이력과 상태만 갱신하세요.

확인 대상은 request_ai_agent_h5_v0/ui.py, app.py, state.py, constants.py, condition_fieldsets.py, condition_engine.py, case_matrix.py, validator.py, preview_document.py, word_export.py 및 관련 최소 테스트입니다. 다음을 기록하세요.
1. 현재 3열 레이아웃, 최근 의뢰, 상단 진행률, 상단 행동의 위치
2. 해석개요·제품·조건·Case의 현재 State 원본과 API 경로
3. preview_screen·word_export Feature Lock 위치
4. PDB·기류 도달 거리·설치 조건 참조 위치
5. 가장 가까운 기존 테스트 실행 명령

소스 기능, 명세 원문, 테스트는 수정하지 마세요. 전체 테스트나 리팩터링을 하지 마세요. python tools/check_encoding.py --changed와 git diff --check를 실행하고, Stage 00을 완료 또는 보류로 기록하세요.
```

## 완료 기준

- 이후 단계가 수정할 실제 파일과 Feature Lock 위치가 인수인계에 기록되어 있다.
- 작업 범위 밖 파일은 변경되지 않았다.
