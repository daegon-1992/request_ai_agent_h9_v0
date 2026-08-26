# Stage 09 — 미리보기 DOM 기반 Word export

## 새 채팅에 붙여 넣을 프롬프트

```text
request_ai_agent_h5_v0의 Stage 09만 수행해 주세요.

AGENTS.md, docs/h5_v0_execution_handoff.md와 Stage 08 기록을 먼저 읽으세요. Stage 08이 완료되지 않았으면 구현하지 마세요.

상단 우측 의뢰서 생성(Word) 기능만 구현하세요.
- Word는 제출·검증·저장 기능이 아니며 항상 실행 가능해야 한다.
- Word 원본은 Stage 08에서 브라우저에 실제로 렌더링한 미리보기 DOM이다. 별도 preview_document State, 기존 Word 템플릿, 과거 Base/Variant·배경/목적/목표 필드 매핑을 사용하지 않는다.
- 미리보기의 섹션 순서, 제목, 라벨, 값, 표, Matrix stale 경고를 같은 순서로 DOCX에 넣는다.
- 문서용 기본 제목·표 서식은 허용하지만 화면에 없는 내용을 Word에 추가하지 않는다.
- Matrix가 stale이거나 입력이 미완성이어도 Word 버튼을 비활성화하거나 export를 막지 않는다.
- 다운로드 파일명은 안전한 기본 파일명을 사용하되 자동 의뢰 제목 기능을 다시 만들지 않는다.

새 API나 최소한의 직렬화 경로가 필요하면 현재 렌더링 DOM에서 필요한 정보만 전달한다. 별도 문서 모델이나 대형 클라이언트 라이브러리를 도입하지 마세요. Word 생성 관련 최소 테스트와 인코딩/diff 검사를 실행하고 인수인계를 갱신하세요.
```

## 완료 기준

- 미리보기와 Word의 정보·순서·Matrix 경고가 일치한다.
- export는 제출, validator, stale 상태에 의해 차단되지 않는다.
