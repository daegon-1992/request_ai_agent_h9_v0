# h5_v0 오케스트레이터 Roadmap

## 문서 정보

- Roadmap 버전: 3.6
- 최종 갱신일: 2026-08-01
- 기준 Commit: `69f9374`
- 프로젝트 루트: `request_ai_agent_h5_v0`
- 현재 단계: 없음 — H5-ORCH-032 Reviewer 승인 후 초기 MVP 단계 완료
- 자동화 Runner 상태: 구축됨. Codex 상태 DB 쓰기 권한 부족으로 H5-ORCH-001 Worker 시작 전 중단됨.

## 전체 목표

기존 h5_v0 폼과 API를 유지하면서 승인 기반 워크플로 오케스트레이터를 안전하게 추가한다.

## 단계 목록

| ID | 단계명 | 상태 | 선행 단계 | 인수인계 문서 |
|---|---|---|---|---|
| 001 | 저장소·실행 구조 조사 | 완료 | 없음 | `h5_orch_001_repo_map.md` |
| 002 | Request State·Proposal 경로 조사 | 완료 | 001 | `h5_orch_002_state_proposal_survey.md` |
| 003 | Fieldset·Validation·출력 구조 조사 | 완료 | 001 | `h5_orch_003_rules_engines_survey.md` |
| 004 | Agent·Q&A·RAG·추출·UI 조사 | 완료 | 001 | `h5_orch_004_agent_ui_survey.md` |
| 005 | 최소 변경 아키텍처 확정 | 완료 | 002,003,004 | `h5_orch_005_target_architecture.md` |
| 006 | 공통 Field Registry | 완료 | 005 | `h5_orch_006_field_registry.md` |
| 007 | Request State version | 완료 | 005 | `h5_orch_007_request_version.md` |
| 008 | Proposal 계약·저장 구조 | 완료 | 006,007 | `h5_orch_008_proposal_contract.md` |
| 009 | Proposal 승인 생명주기 | 완료 | 008 | `h5_orch_009_proposal_lifecycle.md` |
| 010 | Conversation State 모델 | 완료 | 005 | `h5_orch_010_conversation_state.md` |
| 011 | Conversation Session API | 완료 | 010 | `h5_orch_011_conversation_api.md` |
| 012 | Workflow State Machine | 완료 | 009,011 | `h5_orch_012_workflow_machine.md` |
| 013 | Next Field Planner | 완료 | 006,012 | `h5_orch_013_next_field_planner.md` |
| 014 | 자연어 추출 Tool Adapter | 완료 | 008 | `h5_orch_014_extraction_tool.md` |
| 015 | Intent Router | 완료 | 004,012 | `h5_orch_015_intent_router.md` |
| 016 | Orchestrator 메시지 서비스 | 완료 | 009,011,012,013,014,015 | `h5_orch_016_orchestrator_service.md` |
| 017 | Orchestrator API·백엔드 수직 흐름 | 완료 | 016 | `h5_orch_017_backend_vertical_slice.md` |
| 018 | 대화 패널 기본 UI | 완료 | 017 | `h5_orch_018_chat_panel.md` |
| 019 | Proposal 카드·승인 UI | 완료 | 009,018 | `h5_orch_019_proposal_ui.md` |
| 020 | 폼·대화 동기화와 MVP E2E | 완료 | 017,018,019 | `h5_orch_020_mvp_sync.md` |
| 021 | 조건부 필드 영향 안내 | 완료 | 020 | `h5_orch_021_conditional_impact.md` |
| 022 | 모호한 답변·재질문 | 완료 | 020 | `h5_orch_022_clarification.md` |
| 023 | 기존 값 수정 흐름 | 완료 | 020 | `h5_orch_023_correction.md` |
| 024 | Undo | 완료 | 023 | `h5_orch_024_undo.md` |
| 025 | Case Matrix 연결 | 완료 | 021 | `h5_orch_025_case_matrix.md` |
| 026 | Validation 연결 | 완료 | 021 | `h5_orch_026_validation.md` |
| 027 | Preview 연결 | 완료 | 026 | `h5_orch_027_preview.md` |
| 028 | Word 출력 연결 | 완료 | 026,027 | `h5_orch_028_word_export.md` |
| 029 | RAG 근거 안내 연결 | 완료 | 015,020 | `h5_orch_029_rag_guidance.md` |
| 030 | Audit·최소 관측성 | 완료 | 024,025,026,027,028,029 | `h5_orch_030_audit.md` |
| 031 | 핵심 회귀 검증 | 완료 | 030 | `h5_orch_031_regression.md` |
| 032 | 제한적 안정화 | 완료 | 031 | `h5_orch_032_stabilization.md` |

상태 값은 `예정`, `진행 중`, `완료`, `조건부 완료`, `부분 완료`, `중단`, `검증 불가`, `삭제`, `대체됨`을 사용한다.

## 완료된 단계

| ID | 단계명 | 완료일 | 인수인계 문서 |
|---|---|---|---|
| 001 | 저장소·실행 구조 조사 | 2026-07-31 | `h5_orch_001_repo_map.md` |
| 002 | Request State·Proposal 경로 조사 | 2026-07-31 | `h5_orch_002_state_proposal_survey.md` |
| 003 | Fieldset·Validation·출력 구조 조사 | 2026-07-31 | `h5_orch_003_rules_engines_survey.md` |
| 004 | Agent·Q&A·RAG·추출·UI 조사 | 2026-07-31 | `h5_orch_004_agent_ui_survey.md` |
| 005 | 최소 변경 아키텍처 확정 | 2026-07-31 | `h5_orch_005_target_architecture.md` |
| 006 | 공통 Field Registry | 2026-07-31 | `h5_orch_006_field_registry.md` |
| 007 | Request State version | 2026-07-31 | `h5_orch_007_request_version.md` |
| 008 | Proposal 계약·저장 구조 | 2026-07-31 | `h5_orch_008_proposal_contract.md` |
| 009 | Proposal 승인 생명주기 | 2026-07-31 | `h5_orch_009_proposal_lifecycle.md` |
| 010 | Conversation State 모델 | 2026-07-31 | `h5_orch_010_conversation_state.md` |
| 011 | Conversation Session API | 2026-07-31 | `h5_orch_011_conversation_api.md` |
| 012 | Workflow State Machine | 2026-08-01 | `h5_orch_012_workflow_machine.md` |
| 013 | Next Field Planner | 2026-08-01 | `h5_orch_013_next_field_planner.md` |
| 014 | 자연어 추출 Tool Adapter | 2026-08-01 | `h5_orch_014_extraction_tool.md` |
| 015 | Intent Router | 2026-08-01 | `h5_orch_015_intent_router.md` |
| 016 | Orchestrator 메시지 서비스 | 2026-08-01 | `h5_orch_016_orchestrator_service.md` |
| 017 | Orchestrator API·백엔드 수직 흐름 | 2026-08-01 | `h5_orch_017_backend_vertical_slice.md` |
| 018 | 대화 패널 기본 UI | 2026-08-01 | `h5_orch_018_chat_panel.md` |
| 019 | Proposal 카드·승인 UI | 2026-08-01 | `h5_orch_019_proposal_ui.md` |
| 020 | 폼·대화 동기화와 MVP E2E | 2026-08-01 | `h5_orch_020_mvp_sync.md` |
| 021 | 조건부 필드 영향 안내 | 2026-08-01 | `h5_orch_021_conditional_impact.md` |
| 022 | 모호한 답변·재질문 | 2026-08-01 | `h5_orch_022_clarification.md` |
| 023 | 기존 값 수정 흐름 | 2026-08-01 | `h5_orch_023_correction.md` |
| 024 | Undo | 2026-08-01 | `h5_orch_024_undo.md` |
| 025 | Case Matrix 연결 | 2026-08-01 | `h5_orch_025_case_matrix.md` |
| 026 | Validation 연결 | 2026-08-01 | `h5_orch_026_validation.md` |
| 027 | Preview 연결 | 2026-08-01 | `h5_orch_027_preview.md` |
| 028 | Word 출력 연결 | 2026-08-01 | `h5_orch_028_word_export.md` |
| 029 | RAG 근거 안내 연결 | 2026-08-01 | `h5_orch_029_rag_guidance.md` |
| 030 | Audit·최소 관측성 | 2026-08-01 | `h5_orch_030_audit.md` |
| 031 | 핵심 회귀 검증 | 2026-08-01 | `h5_orch_031_regression.md` |
| 032 | 제한적 안정화 | 2026-08-01 | `h5_orch_032_stabilization.md` |

## 현재 단계

없음 — 초기 MVP Roadmap의 032개 단계가 모두 완료됨.

## 남은 단계

없음.

## MVP 완료 기준

### 백엔드 MVP

017 완료 후 자연어 시작부터 Proposal 승인과 다음 질문까지 백엔드 통합 흐름이 검증되어야 한다.

### 사용자 사용 가능 MVP

020 완료 후 기존 폼과 대화 패널에서 승인 전 불변, 승인 후 공식 Request 재조회, Fieldset 재계산, 폼 동기화가 검증되어야 한다.

## 계획 변경 이력

| 버전 | 변경 시점 | 변경 내용 | 변경 이유 | 근거 문서 |
|---|---|---|---|---|
| 0.1 | 2026-07-31 | 최초 32단계 기준 계획 생성 | 자동 재계획의 기준선 마련 | `orchestrator_master_plan.md` |
| 0.2 | 2026-07-31 | 수동 단계 실행·Reviewer·다음 프롬프트 갱신 절차 추가, Runner 실제 상태 반영 | 자동 실행 환경이 중단되어도 동일한 기준 문서로 수동 진행 가능하게 함 | `prompts/manual_stage_execution.md`, `runs/H5-ORCH-001_20260731_144234/blocked_report.md` |
| 0.3 | 2026-07-31 | 001 완료 및 기준 Commit 갱신 | 실제 프로젝트 루트·실행 구조 조사 완료 | `h5_orch_001_repo_map.md` |
| 0.4 | 2026-07-31 | 002 완료 처리, 003 Worker·Reviewer 프롬프트 갱신, 조사로 확인된 State·Proposal 위험 기록 | 002 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 최소 회귀 테스트 16건이 통과함 | `h5_orch_002_state_proposal_survey.md`, Reviewer 결과 |
| 0.5 | 2026-07-31 | 003 완료 처리, 004 Worker·Reviewer 프롬프트 갱신, 조건부 card/Matrix 정규화·출력 계약 위험 기록 | 003 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 독립 최소 회귀 테스트 16건이 통과함 | `h5_orch_003_rules_engines_survey.md`, Reviewer 결과 |
| 0.6 | 2026-07-31 | 004 완료 처리 및 005 Worker·Reviewer 프롬프트 갱신; LLM-only structured output과 geometry Adapter 기준선 확정 | 004 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 mock 기반 전체 회귀 테스트 23건이 통과함 | `h5_orch_004_agent_ui_survey.md`, `69f9374`, Reviewer 결과 |
| 0.7 | 2026-07-31 | 005 완료 처리 및 006 Worker·Reviewer 프롬프트 갱신; LLM-only structured output, canonical geometry Adapter, Proposal-first 경계를 후속 Registry 기준으로 확정 | 005 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 독립 mock 회귀 테스트 23건이 통과함. 006은 canonical binding registry만 추가하고 기존 Fieldset/normalizer/Validator/Case Matrix/Preview/Word 권위를 재사용해야 함 | `h5_orch_005_target_architecture.md`, Reviewer 결과 |
| 0.8 | 2026-07-31 | 006 완료 처리 및 007 Worker·Reviewer 프롬프트 갱신; read-only Field Registry/geometry Adapter 경계와 normalizer·Validator 최종 권위를 확정 | 006 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 Registry/Fieldset/Validator focused test와 기존 최소 회귀 26건이 통과함. 007은 Registry를 version/Proposal/apply 권한으로 바꾸지 않고 request version/latest-read/CAS 계약만 추가해야 함 | `h5_orch_006_field_registry.md`, Reviewer 결과 |
| 0.9 | 2026-07-31 | 007 완료 처리 및 008 Worker·Reviewer 프롬프트 갱신; runtime request identity/latest-read/CAS와 additive versioned API를 Proposal base-version 기준으로 확정 | 007 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 independent focused Registry/version tests 7건이 통과함. `c1ab16f`는 process-local Request store만 제공하므로 008은 server-side Proposal DTO/ledger를 같은 bounded runtime scope에서 만들되 Request/version을 생성 시 바꾸지 않아야 함 | `h5_orch_007_request_version.md`, Reviewer 결과, `c1ab16f` |
| 1.0 | 2026-07-31 | 008 완료 처리 및 009 Worker·Reviewer 프롬프트 갱신; server-issued Proposal ledger의 internal-write authority와 bounded 저장 실패 불변 계약을 승인 lifecycle의 기준으로 확정 | 008 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 Proposal/Request/Registry focused tests 14건이 통과함. 009는 server ledger만 사용해 latest-read/CAS 승인·terminal lifecycle·exactly-once를 구현해야 하며 durable multi-worker semantics는 추가하지 않음 | `h5_orch_008_proposal_contract.md`, Reviewer 결과 |
| 1.1 | 2026-07-31 | 009를 부분 완료 및 Reviewer 보완 대기로 기록; 다음 Worker/Reviewer 프롬프트는 갱신하지 않음 | Reviewer가 lifecycle 구현과 재실행 focused tests 24건을 확인했으나, 009 handoff 문서의 `23 passed` 기록이 실제 `24 passed`와 불일치하여 `rejected`, `safe_to_continue=false`로 판정함. 최소 보완은 handoff의 테스트 결과를 정정하고 encoding/diff 검사를 다시 기록하는 것임 | `h5_orch_009_proposal_lifecycle.md`, H5-ORCH-009 Reviewer 결과 |
| 1.2 | 2026-07-31 | 009 완료 처리 및 010 Worker·Reviewer 프롬프트 갱신; 012·016·019가 server Proposal lifecycle 계약을 소비하도록 후속 경계를 확정 | 보완된 handoff의 `24 passed` 기록과 독립 focused 재검증을 Reviewer가 확인하여 `approved`, `safe_to_continue=true`로 판정함. 010은 Request와 분리된 Conversation State만 구현하며 012는 011 완료 후 lifecycle terminal snapshot을 소비함 | `h5_orch_009_proposal_lifecycle.md`, H5-ORCH-009 Reviewer 결과 |
| 1.3 | 2026-07-31 | 010을 부분 완료 및 Reviewer 보완 대기로 기록; 다음 Worker/Reviewer 프롬프트는 갱신하지 않음 | Reviewer가 model/store 경계와 focused test `5 passed`를 확인했으나, bounded 저장 실패 후 기존 record 불변, 실제 Request State/version에 대한 pause/resume 불변, Proposal expire/reject 등 terminal 참조 및 invalid transition 실패 불변의 focused 증명이 빠져 `rejected`, `safe_to_continue=false`로 판정함 | `h5_orch_010_conversation_state.md`, H5-ORCH-010 Reviewer 결과 |
| 1.4 | 2026-07-31 | 010 완료 처리 및 011 Worker·Reviewer 프롬프트 갱신; Conversation API가 010의 server-issued reference-only 모델을 노출하도록 확정 | 보완 focused test `7 passed`와 독립 재검토가 Conversation/Request 분리, bounded failure·pause/resume·terminal Proposal reference-only 불변을 확인하여 `approved`, `safe_to_continue=true`로 판정함. 011은 Request latest State/version 또는 Proposal lifecycle을 API payload 권위로 복제하지 않아야 함 | `h5_orch_010_conversation_state.md`, H5-ORCH-010 Reviewer 결과 |
| 1.5 | 2026-07-31 | 011 완료 처리 및 012 Worker·Reviewer 프롬프트 갱신; Conversation API lifecycle 위에 deterministic Workflow State Machine을 추가하는 순서를 확정 | H5-ORCH-011 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 독립 focused Flask/store tests `11 passed` 및 encoding/diff 검사를 확인함. 012는 Conversation의 opaque workflow metadata와 pause/closed lifecycle을 소비하되 Request State/version, Proposal lifecycle, public message/API/UI를 확장하지 않아야 함 | `h5_orch_011_conversation_api.md`, H5-ORCH-011 Reviewer 결과 |
| 1.6 | 2026-08-01 | 012 완료 처리 및 013 Worker·Reviewer 프롬프트 갱신; deterministic workflow event boundary를 다음 field planning의 lifecycle guard로 확정 | H5-ORCH-012 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 focused workflow/Conversation API/store tests `18 passed` 및 encoding/diff 검사를 확인함. 013은 latest Request와 read-only Registry를 사용해 최대 2개 다음 질문 field를 결정하되 Request mutation, Planner 외 orchestration, workflow direct mutation을 추가하지 않아야 함 | `h5_orch_012_workflow_machine.md`, H5-ORCH-012 Reviewer 결과 |
| 1.7 | 2026-08-01 | 013 완료 처리 및 014 Worker·Reviewer 프롬프트 갱신; Planner의 validation read failure와 bounded deterministic selection 계약을 확정 | H5-ORCH-013 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 Planner/Registry/Workflow focused tests `15 passed` 및 encoding/diff 검사를 확인함. 014는 existing LLM structured output과 sanitizer를 감싸는 read-only 후보 Tool만 추가하며 Proposal 생성·Request mutation·workflow dispatch를 수행하지 않아야 함 | `h5_orch_013_next_field_planner.md`, H5-ORCH-013 Reviewer 결과 |
| 1.8 | 2026-08-01 | 014 완료 처리 및 015 Worker·Reviewer 프롬프트 갱신; structured-output candidate/failure Tool의 read-only·deterministic 경계를 확정 | H5-ORCH-014 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 Tool/Proposal/Registry focused tests `29 passed`와 encoding/diff 검사를 확인함. 015는 기존 LLM intent vocabulary를 read-only router DTO로 보존하며, Tool candidate/failure·Request/Conversation/Proposal/workflow 경계를 변경하지 않아야 함 | `h5_orch_014_extraction_tool.md`, H5-ORCH-014 Reviewer 결과 |
| 1.9 | 2026-08-01 | 015 완료 처리 및 016 Worker·Reviewer 프롬프트 갱신; invalid Tool DTO를 stable failure로 차단하는 read-only Intent Router 계약을 orchestration 입력 경계로 확정 | H5-ORCH-015 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 Router/Tool/Workflow focused tests `35 passed`와 encoding/diff 검사를 확인함. 016은 Router 결과와 H5-ORCH-014 후보를 소비하되 최신 Request/version, Conversation/Workflow, Proposal lifecycle의 기존 authority를 조합만 해야 하며 직접 patch·공개 API/UI를 추가하지 않음 | `h5_orch_015_intent_router.md`, H5-ORCH-015 Reviewer 결과 |
| 2.0 | 2026-08-01 | 016 완료 처리 및 017 Worker·Reviewer 프롬프트 갱신; server-owned message service를 API adapter와 mock-LLM backend vertical slice로 연결 | H5-ORCH-016 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 service/Router/Tool/Workflow/Proposal/Planner focused suite `69 passed` 및 encoding/diff 검사를 확인함. 017은 `OrchestratorMessageInput`과 service result만 HTTP로 변환하고, client State/version/operation/Proposal/event 권위 또는 optimistic apply를 추가하지 않아야 함 | `h5_orch_016_orchestrator_service.md`, H5-ORCH-016 Reviewer 결과 |
| 2.1 | 2026-08-01 | 017 완료 처리 및 018 Worker·Reviewer 프롬프트 갱신; fresh Conversation의 first patch message를 server-owned start sequence로 Proposal까지 연결 | H5-ORCH-017 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 backend vertical focused suite `71 passed`와 encoding/diff 검사를 확인함. 018은 existing Conversation/message API와 server-issued IDs만 사용해 비파괴적 panel을 추가하며, client workflow event·Request mutation·Proposal lifecycle UI를 추가하지 않아야 함 | `h5_orch_017_backend_vertical_slice.md`, H5-ORCH-017 Reviewer 결과 |
| 2.2 | 2026-08-01 | 018 완료 처리 및 019 Worker·Reviewer 프롬프트 갱신; panel-local server ID bootstrap과 display-only Proposal boundary를 explicit approval UI 단계로 인계 | H5-ORCH-018 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 Node mock DOM/fetch를 포함한 focused suite `46 passed` 및 encoding/diff 검사를 확인함. 019는 server Proposal id만 기존 lifecycle 승인·거절 action에 전달하고, pending diff를 form에 적용하거나 Request refresh/sync를 수행하지 않아야 함 | `h5_orch_018_chat_panel.md`, H5-ORCH-018 Reviewer 결과 |

| 2.3 | 2026-08-01 | 019 완료 처리 및 020 Worker·Reviewer 프롬프트 갱신; server-ledger 승인 UI와 read-only diff 경계를 승인 후 동기화 단계로 인계 | H5-ORCH-019 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 API/UI/vertical/lifecycle focused suite `66 passed` 및 encoding/diff 검사를 재확인함. 020은 approved terminal 결과에 한해 existing versioned Request latest GET으로 form/Fieldset 동기화를 수행하며 pending diff 재적용, client lifecycle authority, RAG/LLM, durable storage를 추가하지 않아야 함 | `h5_orch_019_proposal_ui.md`, H5-ORCH-019 Reviewer 결과 |
| 2.4 | 2026-08-01 | 020 완료 처리 및 021 Worker·Reviewer 프롬프트 갱신; 승인 후 server latest-read form/Fieldset 동기화 경계를 조건부 필드 영향 안내 단계로 인계 | H5-ORCH-020 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 focused suite `60 passed`와 encoding/diff 검사를 직접 확인함. 021은 기존 Fieldset/Registry 결과를 재사용해 활성·비활성·신규 필수·보유값 영향을 안내하되, 조건 규칙 복제·값의 묵시적 삭제·Request/Proposal/workflow authority 확장을 하지 않아야 함 | `h5_orch_020_mvp_sync.md`, H5-ORCH-020 Reviewer 결과 |
| 2.5 | 2026-08-01 | 021 완료 처리 및 022 Worker·Reviewer 프롬프트 갱신; approved latest-read의 canonical State/Fieldset snapshot만 조건부 영향 안내 authority로 확정 | H5-ORCH-021 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 focused suite `63 passed` 및 encoding/diff 검사를 재확인함. 빈 State·필수 section 누락 latest GET은 sync/안내 없이 거부한다. 022는 기존 Tool/Router의 모호성 결과를 server-owned 재질문으로 표현하되 Proposal·Request/version·workflow authority를 만들거나 H5-ORCH-023 수정 흐름을 앞당기지 않아야 함 | `h5_orch_021_conditional_impact.md`, H5-ORCH-021 Reviewer 결과 |
| 2.6 | 2026-08-01 | 022 완료 처리 및 023 Worker·Reviewer 프롬프트 갱신; Tool/Router ordered reason을 재사용하는 server-owned clarification/no-Proposal 경계를 확정 | H5-ORCH-022 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 독립 focused suite `87 passed`와 encoding/diff 검사를 확인함. 다중 후보·단위 누락·무관·빈 입력·Tool/LLM failure는 Proposal/Request/version/form/Fieldset/workflow 변경 없이 결정론적 Korean 재질문을 반환한다. 023은 이 clarification 경계를 보존하고, 명확한 기존 값 수정만 기존 Proposal lifecycle로 처리해야 한다 | `h5_orch_022_clarification.md`, H5-ORCH-022 Reviewer 결과 |

| 2.7 | 2026-08-01 | 023 완료 처리 및 024 Worker·Reviewer 프롬프트 갱신; server latest correction의 version-fence와 Registry/geometry canonical binding 경계를 Undo 선행 조건으로 확정 | H5-ORCH-023 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했다. server version race는 no-Proposal stable failure로, 조건값은 legacy transport가 아닌 Registry canonical condition set으로 판정하며, focused suite `91 passed`와 encoding/diff 검증을 재확인했다. 024는 이 server Proposal/CAS 경계를 우회하지 않는 역Proposal Undo만 구현해야 한다 | `h5_orch_023_correction.md`, H5-ORCH-023 Reviewer 결과 |
| 2.8 | 2026-08-01 | 024 완료 처리 및 025 Worker·Reviewer 프롬프트 갱신; server-recorded inverse evidence와 Request version fence를 사용하는 inverse Proposal Undo 경계를 확정 | H5-ORCH-024 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 inverse ledger 기록 직전 queued Request write를 차단하는 version-fence test를 포함한 focused suite `57 passed` 및 encoding/diff 검사를 재확인함. 025는 승인된 latest Request만 사용해 기존 Case Matrix engine으로 명시적 Action을 연결하며 Undo/CAS/sync 경계를 우회하지 않아야 함 | `h5_orch_024_undo.md`, H5-ORCH-024 Reviewer 결과 |
| 2.9 | 2026-08-01 | 025 완료 처리 및 026 Worker·Reviewer 프롬프트 갱신; 승인 H5-020 latest GET 영수증이 있는 panel-local Request만 read-only Case Matrix Action에 진입하도록 확정 | H5-ORCH-025 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 focused suite `81 passed`, encoding/diff 검사를 확인함. 026은 기존 Validator 결과를 별도 권위나 LLM 판정 없이 server latest canonical Request에서 read-only로 연결해야 하며, 025 Matrix Action의 sync gate·normalizer/Validator authority·legacy UI 격리를 변경하지 않아야 함 | `h5_orch_025_case_matrix.md`, H5-ORCH-025 Reviewer 결과 |
| 3.0 | 2026-08-01 | 026 완료 처리 및 027 Worker·Reviewer 프롬프트 갱신; 승인 H5-020 latest GET 영수증이 있는 panel-local Request를 existing canonical Validator의 read-only Action으로 연결 | H5-ORCH-026 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 독립 재실행 focused suite `86 passed` 및 encoding/diff 검사를 확인함. 027은 이 영수증·server latest 경계를 재사용해 existing Preview 경로만 read-only로 연결해야 하며, Validator 결과를 Preview/form authority로 승격하거나 renderer·Fieldset·Matrix 규칙을 복제하지 않아야 함 | `h5_orch_026_validation.md`, H5-ORCH-026 Reviewer 결과 |

| 3.1 | 2026-08-01 | 027 완료 처리 및 028 Worker/Reviewer 프롬프트 갱신; H5-020 영수증과 fenced server latest snapshot을 기존 browser Preview 진입점에 read-only로 연결 | H5-ORCH-027 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 독립 재실행 focused suite `91 passed` 및 encoding/diff 검증을 확인함. 028은 기존 browser Preview DOM → Word endpoint 계약만 explicit action으로 연결하며 Preview snapshot을 새 Word renderer/template/자동 다운로드 authority로 확장하지 않아야 함 | `h5_orch_027_preview.md`, H5-ORCH-027 Reviewer 결과 |
| 3.2 | 2026-08-01 | 028 완료 처리 및 029 Worker/Reviewer 프롬프트 갱신; H5-020 latest-GET 영수증과 H5-027 fenced Preview DOM 영수증을 기존 Word DOM serializer/endpoint에만 연결 | H5-ORCH-028 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 focused suite `95 passed`, encoding 및 diff 검증을 직접 확인함. 029는 Word/Preview/Request authority를 확장하지 않고 기존 RAG의 근거 안내와 workflow 보기를 읽기 전용으로 연결해야 함 | `h5_orch_028_word_export.md`, H5-ORCH-028 Reviewer 결과 |
| 3.3 | 2026-08-01 | 029 완료 처리 및 030 Worker/Reviewer 프롬프트 갱신; server-issued panel Request id와 existing `run_rag_qa()` evidence DTO를 쓰는 read-only RAG guidance Action을 확정 | H5-ORCH-029 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 focused suite `99 passed`, encoding 및 diff 검증을 직접 확인함. 030은 RAG DTO·Request snapshot·원문을 audit authority나 로그 payload로 넓히지 않고, process-local runtime 한계 안에서 ID·code·순서·redaction만 최소 관측해야 함 | `h5_orch_029_rag_guidance.md`, H5-ORCH-029 Reviewer 결과 |
| 3.4 | 2026-08-01 | 030 완료 처리 및 031 Worker/Reviewer 프롬프트 갱신; existing authority 뒤의 redacted process-local audit observer와 stable audit-read failure 경계를 확정 | H5-ORCH-030 Reviewer가 보완 후 `approved`, `safe_to_continue=true`로 판정했고 focused suite `103 passed`, encoding 및 diff 검증을 직접 확인함. H5-031은 이 observer와 H5-009~029의 기존 경계를 확장하지 않고 승인 전 불변, stale/replay, Conversation 격리, approved sync, Undo, explicit Action 및 legacy UI 격리를 제한된 회귀 Matrix로 검증해야 함 | `h5_orch_030_audit.md`, H5-ORCH-030 Reviewer 결과 |
| 3.5 | 2026-08-01 | 031 완료 처리 및 032 Worker/Reviewer 프롬프트 갱신; H5-009~030 server-authority 경계의 핵심 회귀를 재확인하고 제한적 안정화만 남김 | H5-ORCH-031 Reviewer가 `approved`, `safe_to_continue=true`로 판정했고 Worker `159 passed in 6.71s`, Reviewer 독립 재실행 `159 passed in 6.67s`, encoding 및 diff 검증을 확인함. 재현된 MVP 차단 결함은 없으므로 H5-032는 새 기능·보조 ID 없이, 명확히 재현된 최소 결함만 수정할 수 있음 | `h5_orch_031_regression.md`, H5-ORCH-031 Reviewer 결과 |
| 3.6 | 2026-08-01 | 032 완료 처리 및 실행 프롬프트 종료 상태 갱신; 새 Worker/보조 ID를 만들지 않음 | H5-ORCH-032 Reviewer가 `approved`, `safe_to_continue=true`로 판정함. H5-032는 handoff 메타데이터의 Roadmap 버전을 3.5로 정정한 문서 변경만 수행했고, 독립 Matrix는 `159 passed in 6.80s`, encoding 및 diff 검증을 통과함. 모든 Roadmap 단계가 완료되어 후속 구현은 별도 사용자 승인·범위 정의가 필요함 | `h5_orch_032_stabilization.md`, H5-ORCH-032 Reviewer 결과 |

## 현재 알려진 위험

| ID | 위험 | 영향 | 대응 단계 | 상태 |
|---|---|---|---|---|
| R-001 | Agent의 승인 전 State 직접 변경 | 공식 데이터 손상 | 009,031 | 확인됨 |
| R-002 | stale Proposal 적용 | 최신 사용자 입력 덮어쓰기 | 009,031 | 확인됨 |
| R-003 | Conversation에 Request snapshot 저장 | 오래된 데이터 사용 | 010,016,031 | 미확인 |
| R-004 | 조건부 필드 비활성화 시 값 유실 | 사용자 데이터 손실 | 021,031 | 확인됨 |
| R-005 | UI·백엔드 Fieldset 규칙 불일치 | 질문과 폼 불일치 | 003,031 | 미확인 |
| R-006 | 중복 승인·재시도 | Patch 중복 적용 | 009,019,031 | 확인됨 |
| R-007 | 기존 기능 대체 구현 | 문서와 계산 결과 변경 | 025~029,031 | 미확인 |
| R-008 | legacy chat geometry patch 경로와 h5 공식 geometry State 불일치 | Proposal 적용 후 공식 형상·Case Matrix에 미반영 또는 값 유실 | 009,031 | 부분 완화됨 |

## 공통 구현 원칙

- 기존 폼과 API 유지
- 공식 Request State를 단일 진실 원천으로 유지
- Conversation에 Request 전체 미복제
- 모든 Agent 변경은 Proposal과 사용자 승인 필요
- 승인 시 Request version 재확인
- LLM의 조건·필수·계산·검증 결정 금지
- 기존 Fieldset, Validator, Case Matrix, Preview, Word, RAG 재사용
- 관련 없는 리팩터링과 전체 반복 조사 금지

## 2026-07-31 LLM-only/geometry Adapter 정합화 (우선 적용)

`69f9374 feat: adapt LLM geometry proposals safely` 이후 H5-ORCH-004의
기준선은 다음과 같다. 이 절은 기존 카드의 규칙 기반 추출 재사용 문구와 충돌할 경우
우선한다.

- H5-ORCH-004 상태: **완료 (Reviewer approved, safe_to_continue=true)**. 인수인계 문서는
  `h5_orch_004_agent_ui_survey.md`의 구현 정합화 부록을 사용한다.
- 자연어의 intent와 값 추출은 LLM structured output만 사용한다. regex/alias 기반
  extraction 또는 intent fallback을 새 Orchestrator에 복제하지 않는다.
- LLM 권한은 intent와 후보 operation DTO까지다. allowlist sanitizer, geometry Adapter,
  Fieldset, normalizer, Validator, Case Matrix는 기존 구조 authority로 남는다.
- `geometry.products`는 LLM-facing legacy DTO로만 허용한다. Adapter가 canonical
  `base_product`/`comparison_products`로 변환하고, Preview/Word/Case Matrix는 오직
  canonical state를 소비한다.
- Proposal/dry-run과 모든 Q&A/RAG 실패 응답은 `state_changed=false`다. 승인 apply만
  state 변경 경계이며, H5-ORCH-007~009는 이를 server latest-read/version/CAS 계약으로
  강화한다.

### 후속 카드 보정

| 단계 | 보정된 목표와 금지 사항 |
|---|---|
| H5-ORCH-005 | 최소 아키텍처에 `LLM intent -> sanitized operation -> geometry Adapter -> Proposal/dry-run -> approved apply`를 명시한다. legacy `geometry.products`의 state 저장이나 규칙 extractor 재도입을 금지한다. |
| H5-ORCH-014 | LLM extraction Tool Adapter는 현재 `extract_form_patch_with_llm` DTO와 sanitizer를 감싸며, 실제 LLM 호출 없이 mock contract test를 제공한다. |
| H5-ORCH-015 | Intent Router는 LLM의 `patch/general_qa/rag_qa/current_input/needs_clarification`을 보존한다. keyword/regex intent router를 새로 만들지 않는다. |
| H5-ORCH-016 | Orchestrator service는 read-only Q&A와 Proposal 생성 경계를 보존하고, 최신 Request/version 검증은 apply lifecycle에 위임한다. |
| H5-ORCH-018~020 | UI는 pending Proposal/dry-run을 표시만 하고 form state로 낙관 적용하지 않는다. Yes 승인 응답의 server state만 채택한다. |

### 후속 단계 공통 focused test

1. LLM unavailable/error/invalid operation은 Request State를 변경하지 않는다.
2. `geometry.products=[A100,B200]` dry-run과 승인 apply는 canonical card 및 Case Matrix에
   같은 값을 반영한다.
3. `current_input`, RAG disabled, RAG error는 read-only이며 외부 검색/Request mutation을
   수행하지 않는다.
4. stale/replay/client-supplied Proposal/version authority는 H5-ORCH-002의 조사 결과를
   재사용하여 H5-ORCH-007~009에서 구현한다.

R-008의 legacy geometry 저장 불일치는 현재 Adapter로 완화되었지만, client-supplied
Proposal/state와 latest-read/version authority는 H5-ORCH-007~009 전까지 미해결이다.
