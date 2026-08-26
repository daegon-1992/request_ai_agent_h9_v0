# H5-ORCH 단계별 기준 카드

이 파일은 최초 계획의 기준선이다. 자동 Runner 또는 수동 Planner는 최신 Roadmap, 선행 인수인계 문서와 실제 결과를 반영해 각 카드를 완성형 실행 프롬프트로 확장한다. 수동 실행의 현재 프롬프트는 `current_stage.md`에, 검토 프롬프트는 `review_current_stage.md`에 둔다. 완료된 단계의 카드는 다시 실행하지 않는다.

## H5-ORCH-001 저장소·실행 구조 조사

- 선행 단계: 없음
- 목표: 프로젝트 경계, 런타임 구성, 진입점, API/UI 경계, 테스트 명령을 읽기 전용으로 파악한다.
- 범위: 최상위 manifest, README, 실행점, 라우팅, 테스트 설정, 주요 상위 모듈 위치, Git 상태.
- 허용: 인수인계 문서와 Roadmap만 수정.
- 금지: 앱·설정·테스트 코드, 대용량 데이터·모델·벡터 DB.
- 필수 검증: 기록한 진입점과 테스트 명령이 실제 존재하는지 확인.
- 완료 조건: 후속 단계가 저장소 전체를 재조사하지 않아도 되는 저장소 지도.
- 인수인계: `docs/orchestrator_handoff/h5_orch_001_repo_map.md`

## H5-ORCH-002 Request State·Proposal 경로 조사

- 선행 단계: 001
- 목표: 공식 Request State와 모든 주요 mutation 및 기존 Proposal 승인 경로를 추적한다.
- 범위: 모델, 직렬화, 저장소, 폼 mutation, Agent Proposal, 승인·거절·적용, 우회 경로, 동시성.
- 허용: 문서만 수정.
- 금지: State/API/UI/DB schema 코드.
- 필수 검증: 폼 변경과 Agent 변경 경로를 각각 호출자부터 저장 계층까지 1개 이상 추적.
- 완료 조건: 공식 State 기준점과 승인 전 불변 여부 및 안전 공백 문서화.
- 인수인계: `docs/orchestrator_handoff/h5_orch_002_state_proposal_survey.md`

## H5-ORCH-003 Fieldset·Validation·출력 구조 조사

- 선행 단계: 001
- 목표: 필드 정의, 조건 규칙과 기존 Validation, Case Matrix, Preview, Word 진입점을 파악한다.
- 범위: 필드 원천, 조건부 활성·필수, Validator 입출력, 기존 엔진 진입점, Registry 후보.
- 허용: 문서만 수정.
- 금지: 규칙과 엔진 코드.
- 필수 검증: 대표 조건부 필드 하나의 계산 경로 확인.
- 완료 조건: 공통 Registry 원천과 모든 기존 엔진 재사용 지점 식별.
- 인수인계: `docs/orchestrator_handoff/h5_orch_003_rules_engines_survey.md`

## H5-ORCH-004 Agent·Q&A·RAG·추출·UI 조사

- 선행 단계: 001
- 목표: 기존 LLM 기능과 대화 UI의 재사용 지점 및 권한 위험을 파악한다.
- 범위: LLM client, structured output, 자연어 추출, Q&A/RAG 분기, Proposal UI, 세션 상태.
- 허용: 문서만 수정.
- 금지: Prompt/API/UI/RAG index/환경 설정.
- 필수 검증: 대표 입력이 후보값과 Proposal 또는 State로 이어지는 호출 흐름 확인.
- 완료 조건: 교체 없이 Adapter로 재사용할 지점 식별.
- 인수인계: `docs/orchestrator_handoff/h5_orch_004_agent_ui_survey.md`

## H5-ORCH-005 최소 변경 아키텍처 확정

- 선행 단계: 002, 003, 004
- 목표: 실제 구조에 맞는 최소 변경 데이터·API 계약과 MVP 순서를 확정한다.
- 범위: Adapter 경계, Request version, Proposal, Conversation, Workflow, Planner, 메시지 DTO, 실패 처리.
- 허용: 설계 문서와 Roadmap.
- 금지: 앱 코드와 프로토타입.
- 필수 검증: 정상·stale·중복 승인, 조건부 비활성화, 재개, 승인 전 불변의 설계 검토.
- 완료 조건: 후속 단계가 핵심 계약을 다시 설계하지 않고 구현 가능.
- 인수인계: `docs/orchestrator_handoff/h5_orch_005_target_architecture.md`

## H5-ORCH-006 공통 Field Registry

- 선행 단계: 005
- 목표: 기존 필드 정의와 동적 Fieldset 결과를 공유하는 Registry 또는 Adapter를 구현한다.
- 범위: field_id, State 경로, UI metadata, 조건·필수·의존·검증 metadata, 질문 우선순위.
- 금지: 폼 전면 리팩터링과 조건 규칙 복제.
- 필수 검증: 일반·조건부·조건부 필수 필드 각 1개가 기존 결과와 일치.
- 완료 조건: 폼과 Planner가 동일 필드 의미와 기존 계산 결과를 조회.
- 인수인계: `docs/orchestrator_handoff/h5_orch_006_field_registry.md`

## H5-ORCH-007 Request State version

- 선행 단계: 005
- 목표: Request mutation에 단조 version 또는 동등한 낙관적 동시성 토큰을 도입한다.
- 범위: 초기화, 조회 응답, expected version, 원자 갱신, 충돌 오류, 호환 전략.
- 금지: Proposal, Conversation, UI 구현.
- 필수 검증: 신규·기존 Request, 정상 갱신, stale 거절, 실패 시 State/version 불변.
- 완료 조건: 승인 서비스가 원자적으로 기대 version을 검사 가능.
- 인수인계: `docs/orchestrator_handoff/h5_orch_007_request_version.md`

## H5-ORCH-008 Proposal 계약·저장 구조

- 선행 단계: 006, 007
- 목표: 승인 전 후보 변경을 표준 Proposal로 안전하게 저장한다.
- 범위: ID, request_id, base_version, 정규화 patch, diff 요약, source, status, validation, 시각.
- 금지: Request mutation, 승인 API, Conversation, UI.
- 필수 검증: 유효 생성, 미지원 경로·타입 거절, 생성 후 Request/version 불변.
- 완료 조건: 승인 생명주기가 사용할 안전한 저장 계약.
- 인수인계: `docs/orchestrator_handoff/h5_orch_008_proposal_contract.md`

## H5-ORCH-009 Proposal 승인 생명주기

- 선행 단계: 008
- 목표: Proposal 승인·거절·만료·충돌을 원자적으로 처리한다.
- 범위: 최신 State 재조회, base_version 검사, 재검증, patch 적용, version 증가, Fieldset 재계산.
- 금지: Conversation, Orchestrator, UI와 기존 엔진 재구현.
- 필수 검증: 정상·거절·stale·중복 승인, validation 실패와 모든 실패의 State 불변.
- 완료 조건: 승인된 Proposal만 정확히 한 번 적용.
- 인수인계: `docs/orchestrator_handoff/h5_orch_009_proposal_lifecycle.md`

## H5-ORCH-010 Conversation State 모델

- 선행 단계: 005
- 목표: Request와 분리되고 request_id로만 연결되는 최소 대화 상태를 저장한다.
- 범위: session, workflow, 질문·승인 대기, pending Proposal, 질문 이력, pause, 요약, version.
- 금지: Request snapshot, 공개 API, Workflow 전이, UI.
- 필수 검증: 생성·조회·격리와 Request 전체 미복제.
- 완료 조건: 공식 Request와 독립적인 대화 진행 상태.
- 인수인계: `docs/orchestrator_handoff/h5_orch_010_conversation_state.md`

## H5-ORCH-011 Conversation Session API

- 선행 단계: 010
- 목표: 세션 생성·조회·중지·재개·종료의 최소 API를 제공한다.
- 금지: 메시지 처리, LLM, Workflow, Proposal 승인 재구현.
- 필수 검증: 생명주기, 종료 후 갱신 거절, request/session 격리.
- 완료 조건: 프런트엔드가 세션 생명주기를 안전하게 관리.
- 인수인계: `docs/orchestrator_handoff/h5_orch_011_conversation_api.md`

## H5-ORCH-012 Workflow State Machine

- 선행 단계: 009, 011
- 목표: 작성 단계와 허용 전이를 결정론적 상태 머신으로 구현한다.
- 범위: 시작, 답변 대기, 승인 대기, 계획, 완료 후보, validation 준비, pause, 완료, 오류.
- 금지: LLM 기반 전이, Planner, UI.
- 필수 검증: 정상 흐름, 승인 대기 우회 금지, pause/resume, 종료 후 변경 금지.
- 완료 조건: MVP 전이가 명시적 이벤트로만 수행.
- 인수인계: `docs/orchestrator_handoff/h5_orch_012_workflow_machine.md`

## H5-ORCH-013 Next Field Planner

- 선행 단계: 006, 012
- 목표: 최신 Request와 Registry로 다음 질문 필드 1~2개를 결정한다.
- 범위: 활성·미입력, 필수, 의존, validation 차단, 단계, 질문 이력, 그룹화.
- 금지: LLM 필드 선택, Request mutation, UI.
- 필수 검증: 필수·상위 의존 우선, 비활성 제외, 반복 후순위, 최대 2개.
- 완료 조건: 동일 입력에 동일 필드와 선택 이유 반환.
- 인수인계: `docs/orchestrator_handoff/h5_orch_013_next_field_planner.md`

## H5-ORCH-014 자연어 추출 Tool Adapter

- 선행 단계: 008
- 목표: 기존 추출 기능을 검증 가능한 후보값 생성 Tool로 래핑한다.
- 범위: 허용 field_id, 후보, confidence, 근거 구문, 모호성, 단위, 오류.
- 금지: State mutation, 임의 값 보완, 일반 Q&A/RAG 재작성.
- 필수 검증: 정상, 값 없음, 타입 오류, 모호성, 단위 누락, 호출 실패와 State 불변.
- 완료 조건: Proposal 입력으로 안전하게 사용할 후보 계약.
- 인수인계: `docs/orchestrator_handoff/h5_orch_014_extraction_tool.md`

## H5-ORCH-015 Intent Router

- 선행 단계: 004, 012
- 목표: 작성 시작·답변·Proposal 제어·Q&A·RAG·pause/resume 의도를 안전하게 분류한다.
- 금지: State/Workflow 직접 변경과 기존 Q&A/RAG 대체.
- 필수 검증: 대표 의도와 불명확 명령의 안전한 기본 분기.
- 완료 조건: 입력마다 다음 처리 범주와 분류 이유 반환.
- 인수인계: `docs/orchestrator_handoff/h5_orch_015_intent_router.md`

## H5-ORCH-016 Orchestrator 메시지 서비스

- 선행 단계: 009, 011, 012, 013, 014, 015
- 목표: 최신 Request 조회부터 Proposal 또는 다음 질문 생성까지 application service로 조합한다.
- 범위: Conversation 조회, intent, extraction, validation, Proposal, Planner, 질문 표현.
- 금지: 직접 patch, 공개 endpoint, UI, 기존 엔진 재구현.
- 필수 검증: 시작 Proposal, 승인 전 불변, 승인 후 최신 조회, 다음 질문, Q&A 분기 보존.
- 완료 조건: API 독립적인 MVP 핵심 조합.
- 인수인계: `docs/orchestrator_handoff/h5_orch_016_orchestrator_service.md`

## H5-ORCH-017 Orchestrator API·백엔드 수직 흐름

- 선행 단계: 016
- 목표: 메시지 API와 자연어 시작부터 다음 질문까지 백엔드 수직 흐름을 완성한다.
- 금지: endpoint business rule, 프런트엔드, 기존 endpoint 삭제.
- 필수 검증: 시작→기본값 Proposal→승인→version 변경→Fieldset→개요 질문→Proposal→승인→다음 질문.
- 완료 조건: mock LLM 기반 백엔드 MVP 통합 테스트 통과.
- 인수인계: `docs/orchestrator_handoff/h5_orch_017_backend_vertical_slice.md`

## H5-ORCH-018 대화 패널 기본 UI

- 선행 단계: 017
- 목표: 기존 폼 옆에 비파괴적인 대화 패널과 메시지 전송을 추가한다.
- 범위: shell, 세션, 메시지, 입력, 로딩, 기본 오류.
- 금지: 폼 대체, Proposal 승인, 직접 State mutation.
- 필수 검증: 열기·닫기, 세션, 전송, 오류, 기존 폼 기능 유지.
- 완료 조건: 폼과 대화 패널 동시 사용.
- 인수인계: `docs/orchestrator_handoff/h5_orch_018_chat_panel.md`

## H5-ORCH-019 Proposal 카드·승인 UI

- 선행 단계: 009, 018
- 목표: diff를 표시하고 승인·거절하는 UI를 기존 Proposal 구조와 연결한다.
- 금지: 프런트 직접 patch와 승인 전 낙관적 폼 변경.
- 필수 검증: 정상 승인, 거절, 중복 클릭, stale, validation 오류, 승인 전 폼 불변.
- 완료 조건: 사용자가 변경 내용을 확인하고 명시적으로 승인·거절.
- 인수인계: `docs/orchestrator_handoff/h5_orch_019_proposal_ui.md`

## H5-ORCH-020 폼·대화 동기화와 MVP E2E

- 선행 단계: 017, 018, 019
- 목표: 승인 후 공식 Request 재조회와 기존 폼·Fieldset 동기화로 사용자 MVP를 완성한다.
- 범위: refresh, form store, Fieldset 재계산, Conversation, 다음 질문, draft 충돌.
- 금지: patch 중복 적용, 미저장 폼 값 묵시적 덮어쓰기.
- 필수 검증: 두 차례 승인, 승인 전 불변, 양쪽 UI 일치, stale, 기존 폼 수동 편집.
- 완료 조건: 사용자 사용 가능 MVP 수직 흐름.
- 인수인계: `docs/orchestrator_handoff/h5_orch_020_mvp_sync.md`

## H5-ORCH-021 조건부 필드 영향 안내

- 선행 단계: 020
- 목표: 변경 전후 활성 필드와 신규 필수·비활성·보유값 영향을 안내한다.
- 금지: 조건 규칙 복제와 값의 묵시적 삭제.
- 필수 검증: 활성화, 비활성화, 신규 필수, 값 있는 비활성 필드 보존.
- 완료 조건: 영향이 결정론적으로 계산되고 데이터가 유실되지 않음.
- 인수인계: `docs/orchestrator_handoff/h5_orch_021_conditional_impact.md`

## H5-ORCH-022 모호한 답변·재질문

- 선행 단계: 020
- 목표: 다중 후보·단위 누락·무관 답변에서 Proposal 대신 명확화 질문을 제공한다.
- 금지: 후보 임의 선택과 수치 추정.
- 필수 검증: 다중 후보, 단위 누락, 무관·빈 답변, 연속 실패와 State 불변.
- 완료 조건: 모호한 입력에서 Proposal 미생성과 안전한 재질문.
- 인수인계: `docs/orchestrator_handoff/h5_orch_022_clarification.md`

## H5-ORCH-023 기존 값 수정 흐름

- 선행 단계: 020
- 목표: 자연어 수정도 기존 값과 새 후보의 diff가 있는 Proposal로 처리한다.
- 금지: 직접 patch와 다중 대상 임의 해석.
- 필수 검증: 단일 수정, 동일 값, 미지원 필드, 모호한 대상, stale와 승인 전 불변.
- 완료 조건: 수정이 일반 Proposal 생명주기를 재사용.
- 인수인계: `docs/orchestrator_handoff/h5_orch_023_correction.md`

## H5-ORCH-024 Undo

- 선행 단계: 023
- 목표: 직접 snapshot 복원 대신 현재 version 기준 역Proposal로 되돌린다.
- 금지: DB rollback, 이후 변경 덮어쓰기, 승인 우회.
- 필수 검증: 정상 Undo, 승인 전 불변, 이후 변경 충돌, 중복 Undo, version 증가.
- 완료 조건: Undo가 일반 Proposal 안전 규칙을 우회하지 않음.
- 인수인계: `docs/orchestrator_handoff/h5_orch_024_undo.md`

## H5-ORCH-025 Case Matrix 연결

- 선행 단계: 021
- 목표: readiness 후 명시적 사용자 Action으로 기존 Case Matrix 엔진을 호출한다.
- 금지: LLM 계산, 자동 생성, 계산식·편집 UI 재작성.
- 필수 검증: 준비 전 차단, 정상 호출, 기존 결과 동일성, 엔진 오류 전달.
- 완료 조건: 대화에서 기존 Case Matrix 기능으로 안전하게 진입.
- 인수인계: `docs/orchestrator_handoff/h5_orch_025_case_matrix.md`

## H5-ORCH-026 Validation 연결

- 선행 단계: 021
- 목표: 기존 Validator 결과를 보존하며 실행·설명·다음 질문과 연결한다.
- 금지: LLM 검증 결과 생성, 오류 숨김, 규칙 재작성.
- 필수 검증: 성공, 오류, 경고, field 연결, 설명 실패 시 원본 표시.
- 완료 조건: 원본 검증 결과가 손실 없이 대화와 연결.
- 인수인계: `docs/orchestrator_handoff/h5_orch_026_validation.md`

## H5-ORCH-027 Preview 연결

- 선행 단계: 026
- 목표: readiness에 따라 기존 Preview 경로를 안내·호출한다.
- 금지: renderer 복제와 LLM 문서 생성.
- 필수 검증: 준비 전 안내, 정상 진입, 공식 Request 사용, 오류 표시.
- 완료 조건: 기존 Preview 기능과 호환되는 대화 Action.
- 인수인계: `docs/orchestrator_handoff/h5_orch_027_preview.md`

## H5-ORCH-028 Word 출력 연결

- 선행 단계: 026, 027
- 목표: 명시적 사용자 Action으로 기존 Word 출력 API를 호출한다.
- 금지: Word renderer/template 변경과 자동 다운로드 강제.
- 필수 검증: 준비 전 차단, 대표 출력 1건, 기존 폼 호환, 오류·취소.
- 완료 조건: 대화와 폼이 동일 Word 출력 기능 사용.
- 인수인계: `docs/orchestrator_handoff/h5_orch_028_word_export.md`

## H5-ORCH-029 RAG 근거 안내 연결

- 선행 단계: 015, 020
- 목표: 기존 RAG를 재사용해 출처가 있는 설명과 workflow 복귀를 제공한다.
- 금지: RAG 답변 자동 patch, 벡터 DB 재구축, prompt 전면 개편.
- 필수 검증: 근거 있음, 결과 없음, 검색 실패, workflow 복귀, State 불변.
- 완료 조건: 기존 RAG가 근거 안내 기능으로 안전하게 동작.
- 인수인계: `docs/orchestrator_handoff/h5_orch_029_rag_guidance.md`

## H5-ORCH-030 Audit·최소 관측성

- 선행 단계: 024~029
- 목표: Proposal, version, Workflow, Undo와 기존 기능 Action을 ID 단위로 추적한다.
- 금지: 전체 원문·Request snapshot·비밀값 로그와 대규모 관측 플랫폼.
- 필수 검증: 성공·stale·거절·Undo·검증 실패 이벤트 순서와 redaction.
- 완료 조건: 주요 변경을 request/session/proposal ID로 추적.
- 인수인계: `docs/orchestrator_handoff/h5_orch_030_audit.md`

## H5-ORCH-031 핵심 회귀 검증

- 선행 단계: 030
- 목표: State 안전성과 기존 폼·API 호환성을 제한된 회귀 Matrix로 검증한다.
- 범위: 테스트와 원인이 명확한 최소 결함 수정만 허용.
- 금지: 신규 기능, 광범위 리팩터링, 전체 조합.
- 필수 검증: 승인 전 불변, stale·중복 승인, 세션 격리, 최신 조회, 필드 유실, Undo, 기존 기능 경로.
- 완료 조건: 치명적 결함 없이 핵심 위험 결과와 미검증 영역 기록.
- 인수인계: `docs/orchestrator_handoff/h5_orch_031_regression.md`

## H5-ORCH-032 제한적 안정화

- 선행 단계: 031
- 목표: MVP 운영을 막는 재현 가능한 필수 결함만 수정하고 초기 구현을 마감한다.
- 금지: 기능 확장, 성능 최적화, 대규모 리팩터링, 미관 개선.
- 필수 검증: 수정 결함 재현 테스트와 관련 안전 테스트.
- 완료 조건: 치명적 미해결 결함 없음, 잔여 제한과 후속 backlog 기록.
- 인수인계: `docs/orchestrator_handoff/h5_orch_032_stabilization.md`
