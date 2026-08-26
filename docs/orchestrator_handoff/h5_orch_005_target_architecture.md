# H5-ORCH-005 최소 변경 Orchestrator 아키텍처 확정

# 단계 정보

- 단계 ID: H5-ORCH-005
- 단계명: 최소 변경 아키텍처 확정
- 실행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 실행 기준 코드 버전 또는 Commit: `69f9374` (`feat: adapt LLM geometry proposals safely`)
- Roadmap 버전: 0.6 (2026-07-31)
- 작업 상태: 완료 후보 — Reviewer 검토 대기

# 이번 단계 목표

현재 h5_v0의 안전 경계와 공개 API를 보존하면서, 이후 Orchestrator가 재사용할 최소 계약을 확정한다. 자연어의 intent와 명시 값 후보만 LLM이 판단한다. LLM은 Request State, Fieldset, normalizer, Validator, Case Matrix, Preview, Word 및 RAG의 권위자가 아니다. 구조 안전성과 상태 변경 권한은 기존 경계와 승인 생명주기에 남긴다.

# 사전 입력 문서

- `AGENTS.md`
- `docs/orchestrator_handoff/orchestrator_roadmap.md` (v0.6)
- `docs/orchestrator_handoff/prompts/common_stage_contract.md`
- `docs/orchestrator_handoff/prompts/baseline_prompts.md`
- `docs/orchestrator_handoff/prompts/manual_stage_execution.md`
- `docs/orchestrator_handoff/h5_orch_001_repo_map.md`
- `docs/orchestrator_handoff/h5_orch_002_state_proposal_survey.md`
- `docs/orchestrator_handoff/h5_orch_003_rules_engines_survey.md`
- `docs/orchestrator_handoff/h5_orch_004_agent_ui_survey.md`

# 실제 수행 내용

문서와 기준선 `69f9374`의 정적 호출 경계를 대조하여 최소 계약만 확정했다. 앱, API, UI, 테스트, DB schema, RAG/vector store, Prompt, renderer는 수정하지 않았고 실제 LLM/RAG/외부 DB 호출도 하지 않았다. H5-ORCH-002의 client-held state와 stale/replay/ledger 조사, H5-ORCH-003의 Fieldset·normalizer·Validator·Case Matrix·Preview/Word 조사는 재수행·재구현하지 않고 아래 계약의 외부 권위로만 참조한다.

# 변경 파일

- `docs/orchestrator_handoff/h5_orch_005_target_architecture.md` (이 문서만 추가)

# 현재/목표 component 경계

```text
user message + client-held state
  -> extract_form_patch_with_llm(message, state_summary, public_schema)
     [LLM: intent + explicit operation DTO only; no state mutation]
  -> sanitize_external_operations(operations, source)
     [allowlist, type/merge/dedupe only; no natural-language inference]
  -> geometry Adapter for geometry.products
     [legacy list DTO -> canonical base_product/comparison_products]
  -> proposal_from_operations(...) + preview_patch/apply_patch_operations copy
     [pending Proposal + dry-run; state_changed=false, read_only=true]
  -> explicit approved apply only
     [apply to copy -> sanitize_state -> state_with_validation]
  -> canonical state consumed by existing Fieldset/normalizer/Validator/
     Case Matrix/Preview/Word paths
```

현재 `POST /api/chat/send`도 이 순서를 사용한다. `patch`는 `input_proposal`, `needs_clarification`은 명확화 응답, `current_input`은 canonical state 요약, 그 외는 `general_qa` 또는 `rag_qa` 읽기 전용 응답으로 분기한다. Proposal과 dry-run은 승인 전의 복사본이며, Q&A/RAG 실패도 Request State를 바꾸지 않는다.

## 책임 고정

| Component / DTO | 입력 | 출력 | 권한과 금지 |
|---|---|---|---|
| `llm_client.py:extract_form_patch_with_llm` | message, state summary, public schema | provider metadata + `{intent, operations, summary, warnings, questions}` | `patch`, `general_qa`, `rag_qa`, `current_input`, `needs_clarification`의 분류와 사용자가 명시한 후보값만 판단한다. State mutation, 규칙 계산, RAG 근거값의 patch 편입은 금지한다. |
| LLM operation DTO | `set`, `list_values`, `condition_values`; path/value(s), `replace|append`, label/confidence | 외부 비신뢰 structured data | `patch` 이외 intent는 빈 `operations`여야 한다. 허용되지 않은 op/path/type은 안전하게 폐기된다. regex/alias extractor 또는 keyword/regex intent router는 대체물로 추가하지 않는다. |
| `chat_patch.py:sanitize_external_operations` | 비신뢰 operation list, source | allowlist 통과·dedupe된 `PatchOperation` | 구조 allowlist, 값 존재 여부, confidence/merge 기본값만 결정한다. 자연어/alias 해석, 누락값 보완, Request mutation은 하지 않는다. `geometry.products`에는 Adapter 표식을 붙인다. |
| `chat_patch.py:proposal_from_operations` | message, sanitized candidate, warnings/questions, base state | `PatchProposal` (`pending`/`needs_clarification`/`noop`) | Proposal은 read-only이며 항상 `state_changed=false`. 현재 schema version은 참고 metadata일 뿐 request version/CAS가 아니다. |
| geometry Adapter (`geometry_products_to_complete_product_cards` 계약; 현 helper `_set_canonical_geometry_products`) | legacy `geometry.products` values + merge strategy + canonical geometry | canonical `geometry.base_product`, `geometry.comparison_products` | 아래 geometry 계약을 따른다. legacy key를 Request State에 보관하거나 renderer/Matrix에 전달하지 않는다. |
| `apply_patch_operations` | 승인된 이미-sanitized operation + base state | 새 copy의 `sanitize_state` + `state_with_validation` 결과 | 승인 경계에서만 호출한다. allowlist를 다시 확인하고 canonicalization/validation을 재사용한다. LLM, client Proposal, UI는 이를 직접 mutation 권한으로 사용하지 않는다. |

## canonical geometry Adapter 계약

`geometry.products`는 LLM-facing legacy DTO로 유지한다. 이는 API/LLM 입력 호환성을 위한 list path일 뿐 Request State의 저장 필드가 아니다.

- `list_values(path="geometry.products", merge_strategy="replace")`: sanitize된 dedupe 값의 첫 번째를 `geometry.base_product.drawing_no`로, 나머지를 순서대로 `geometry.comparison_products[].drawing_no`로 만든다.
- `append`: 현재 canonical base + comparison의 drawing number를 먼저 읽고, 새 값을 대소문자 무시 dedupe한 뒤 같은 base/comparison 규칙으로 다시 구성한다.
- 빈 값, 중복 값, 허용되지 않은 DTO는 canonical geometry를 바꾸지 않는다. base/comparison card의 id/role은 Adapter가 안정적으로 구성한다.
- Adapter 결과만 `sanitize_state()`에 전달한다. 기존 normalizer가 활성 Fieldset 및 종속 Case Matrix 값을 재계산·제거할 수 있으며, Adapter/Orchestrator가 이 규칙을 복제하거나 보정하지 않는다.
- Validator와 Case Matrix는 normalized canonical state만 소비한다. Preview/Word도 기존 권위 경로를 재사용한다. 특히 현재 Word의 browser DOM 권위와 readiness/staleness guard는 H5-ORCH-003에서 발견된 제약이며 005가 renderer를 바꾸지 않는다.

# `/api/chat/send` 응답 계약

모든 아래 분기는 승인 전 `state_changed=false`이고, read-only 분기는 Request State 변경 권한이 없다. 응답은 기존의 `ok`, `version`, `stage`, `assistant`, `chat_mode`, `chat_result`, `state_changed` 호환 shape를 유지한다.

| resolved / command | 필수 DTO | `read_only` / `state_changed` | 실패·feature-lock 계약 |
|---|---|---|---|
| `input_proposal` / `patch_proposal` | `proposal`, `dry_run`, `llm_form_extraction` | Proposal은 `read_only=true`; 전체 `state_changed=false` | LLM unavailable/error 또는 invalid/empty operation은 `needs_clarification` Proposal로 축소한다. 저장·apply·optimistic UI 변경은 없다. |
| `general_qa` / `general_qa` | `llm` answer metadata | read-only / false | 일반 답변 LLM 실패는 제한 안내로 끝낸다. answer를 patch로 전환하지 않는다. |
| `rag` / `rag_qa` | `qa`, optional `llm` answer metadata | `qa.read_only=true` / false | RAG Off는 `rag_disabled`, 실행 예외는 `rag_error`; 검색·요약 실패와 RAG answer는 State/Proposal을 만들거나 바꾸지 않는다. |
| `current_input` / `current_input` | `qa.summary` from canonical state | `qa.read_only=true` / false | RAG를 호출하지 않고 state summary만 읽는다. |
| `needs_clarification` / `needs_clarification` | proposal warnings/questions, extraction metadata | read-only / false | 불명확 intent, LLM unavailable/error, invalid operation은 안전한 기본 분기다. 값 추정·규칙 fallback·직접 apply를 금지한다. |

`/api/chat/apply`는 현재 호환 경로로 남기되, 이 목표 계약에서 유일한 상태 변경 지점은 명시적으로 승인된 operation의 apply이다. 현재 client-supplied Proposal 및 fingerprint 보호는 임시 호환 동작이며, 신뢰 가능한 lifecycle 보장은 아니다.

# 신규 또는 변경된 데이터 구조

이번 단계는 코드 DTO를 새로 만들거나 변경하지 않았다. 이후 구현이 준수할 최소 논리 DTO는 다음과 같다.

- `LLMIntentResult`: `intent`, `operations`, `summary`, `warnings`, `questions`, provider metadata. LLM output은 비신뢰 input이다.
- `PatchOperation`: sanitizer가 허용한 `set | list_values | condition_values`와 canonical adapter metadata. `geometry.products`는 transport-only legacy path다.
- `PatchProposal`: `proposal_id`, status, intent/chat_intent, sanitized operations, summary, warnings/questions, extraction source, dry-run의 basis. 생성 시 `read_only=true`, `state_changed=false`다.
- `DryRun`: base state copy에 operation을 적용해 얻는 canonical normalized state, Case Matrix, validation, submission view. 공식 Request를 저장·변경하지 않는다.
- `ChatResult`: 위 응답 분기의 command와 QA/Proposal payload. Q&A/RAG 응답은 PatchOperation을 포함하거나 answer-to-patch로 승격하지 않는다.

H5-ORCH-008에서만 persistent Proposal에 `request_id`, `base_version`, normalized patch, diff, validation, source, status, timestamps를 정한다. H5-ORCH-005는 이를 선행 구현하거나 client payload를 신뢰하지 않는다.

# 신규 또는 변경된 API

없음. 기존 API의 endpoint, request/response shape 및 UI 소비를 변경하지 않는다. 향후 006~020도 기존 form/API를 교체·삭제하지 않고 additive adapter/DTO/service 경로를 택해야 한다.

# 중요 설계 결정

1. **LLM-only structured output 기준선.** 자연어 extractor와 intent 분류의 유일한 의미 판단자는 `extract_form_patch_with_llm`이다. 새 regex/alias extractor나 keyword/regex intent router를 Orchestrator 계약으로 재도입하지 않는다.
2. **구조 권위 분리.** sanitizer가 외부 operation을 제한하고 Adapter가 legacy geometry를 canonical geometry로 바꾸며, existing Fieldset/normalizer/Validator/Case Matrix/Preview/Word가 구조·계산·출력의 권위를 계속 가진다.
3. **Proposal-first.** 추출·proposal·dry-run은 copy-only이며 `state_changed=false`; UI는 pending Proposal을 표시할 수 있어도 form state를 낙관적으로 채택하지 않는다. approved apply 뒤의 공식 결과만 반영한다.
4. **현재 저장 모델의 한계 명시.** H5-ORCH-002가 확인한 대로 현재는 client-held state이고 server latest-read, request version/CAS, Proposal ledger가 없다. stale/replay/forged Proposal/one-time apply 문제는 해결되었다고 선언하지 않는다. client-supplied Proposal/state의 신뢰 경계와 latest-read/version/CAS는 H5-ORCH-007~009의 보류 과제다.
5. **RAG와 Q&A는 읽기 전용.** RAG disabled/error 및 general QA failure도 `state_changed=false`다. RAG answer-to-patch 자동 전환은 비목표이며 H5-ORCH-029 이후에도 명시적 새 입력·Proposal을 우회할 수 없다.

# 기존 기능 재사용 지점

- H5-ORCH-002: client-held canonical state, current fingerprint stale behavior, Proposal ledger 부재를 전제로 한다. 이를 보완하는 version/CAS/ledger를 여기서 만들지 않는다.
- H5-ORCH-003: `sanitize_state()`와 Fieldset recomputation, Validator, Case Matrix 및 실제 Preview-to-Word authority를 재사용한다. conditional inactive value 및 Matrix removal side effect는 dry-run에서 관찰할 대상이지 Orchestrator가 복제할 규칙이 아니다.
- H5-ORCH-004: LLM intent set, read-only Q&A/RAG, `/api/chat/send` 응답 분기 및 feature-lock failure behavior를 그대로 기준으로 쓴다.
- 기준 코드: `request_ai_agent_h5_v0/llm_client.py:251`, `chat_patch.py:99,186,325`, `app.py:1087,1749,1834`의 호출/책임 연결만 확인했다.

# 수행하지 않은 작업

- H5-ORCH-006 이후 구현, DB migration, schema/API/UI/test 변경, Prompt 변경, renderer 변경을 하지 않았다.
- 실제 LLM, RAG, vector store, 외부 DB 호출을 하지 않았다.
- Fieldset, normalizer, Validator, Case Matrix, Preview/Word, state storage/concurrency를 재조사하거나 재구현하지 않았다.
- Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 수정하지 않았다.

# H5-ORCH-006~016 및 018~020 후속 순서

| 단계 | 선행 조건 | 최소 component/DTO 범위와 권위 | 금지 사항 | 예상 파일 / focused test 위치 |
|---|---|---|---|---|
| 006 Field Registry | 005 | existing schema/canonical binding을 하나의 registry adapter로 노출; normalizer가 최종 결정 | Fieldset/Case Matrix 규칙 복제, state mutation | `schema.py`, `state.py`, adapter module; `tests/test_task12_minimal_regression.py` 또는 새 `tests/test_orchestrator_field_registry.py` |
| 007 Request version | 005 | request id/version, latest-read, atomic expected-version/CAS 계약 | Proposal/Conversation/UI 구현, migration를 자동 결정 | state/store boundary와 focused version tests |
| 008 Proposal contract | 006, 007 | persistent Proposal DTO: request_id, base_version, normalized patch/diff, validation, status | Request mutation, client Proposal 신뢰 | proposal service/store; forged/invalid DTO, creation-is-read-only tests |
| 009 Proposal lifecycle | 008 | latest read + CAS + revalidation + exactly-once approve/reject/expire | Conversation/UI, approval bypass | approval service; stale/replay/duplicate/validation-failure invariant tests |
| 010 Conversation state | 005 | Request와 분리된 session/workflow/pending reference state | Request snapshot 복제, public API/workflow 구현 | conversation model/store; isolation tests |
| 011 Conversation API | 010 | session lifecycle API | message/LLM/workflow/Proposal 재구현 | API module; terminal/isolated session tests |
| 012 Workflow machine | 009, 011 | deterministic event/state DTO | LLM-based transition, Planner/UI | workflow module; approval-wait bypass tests |
| 013 Next Field Planner | 006, 012 | Registry + latest Request를 읽는 deterministic next 1–2 field DTO | LLM field selection, Request mutation | planner module; inactive/required/dependency ordering tests |
| 014 Extraction Tool Adapter | 008 | existing LLM result + sanitizer를 candidate tool DTO로 감싼다 | direct mutation, value invention, Q&A/RAG rewrite | `llm_client.py`, `chat_patch.py` adapter boundary; mock normal/ambiguous/error tests |
| 015 Intent Router | 004, 012 | existing LLM intent result를 workflow action category로 map | keyword/regex router, direct State/Workflow change | router service; five intent plus unclear tests |
| 016 Orchestrator service | 009,011–015 | latest Request read → intent → extraction → Proposal/next question composition | direct patch/public endpoint/UI, rules engine duplication | application service; approval-before-mutation and Q&A branch tests |
| 018 Chat panel | 017 | non-destructive session/message UI | form replacement, direct mutation | `ui.py` additive panel; open/send/error/form-retention tests |
| 019 Proposal UI | 009,018 | Proposal diff + explicit approve/reject UI | frontend patch, optimistic form state | `ui.py` additive card; duplicate/stale/reject/pre-approval invariant tests |
| 020 MVP sync | 017–019 | approved result re-read → existing form/Fieldset refresh | duplicate patch, implicit overwrite of unsaved form | UI/API integration tests; two approvals, stale, manual-form-edit tests |

H5-ORCH-017 is intentionally not redesigned here; it remains the backend vertical slice after 016. H5-ORCH-018~020 must preserve the existing form as an independently usable API/UI surface.

# 최소 검증

| 검증 | 결과 |
|---|---|
| 정적 책임 매핑 | 완료: `extract_form_patch_with_llm -> proposal_from_operations/sanitize_external_operations -> apply_patch_operations`, 그리고 `/api/chat/send`의 patch/clarification/current-input/general-QA/RAG 분기를 확인했다. |
| geometry mapping | 완료: `geometry.products` sanitizer metadata가 canonical base/comparison Adapter로 연결되고 apply 뒤 `sanitize_state`/validation을 재사용함을 확인했다. |
| UTF-8 인코딩 | 아래 명령으로 변경 문서를 검사한다. |
| diff 형식 | 아래 명령으로 whitespace 오류를 검사한다. |
| mock regression | 사용자 요청 명령을 실행해 LLM/RAG 호출 없이 mock 경로를 확인한다. |

# 실패하거나 실행하지 못한 검증

- 실제 LLM/RAG/외부 DB 호출은 범위 금지이므로 실행하지 않는다.
- version/CAS/ledger, server latest-read, persistent Proposal의 동시성·replay 검증은 아직 구현 대상이 아니며 H5-ORCH-007~009에서 수행한다.

# 알려진 문제와 제한사항

- 현 Proposal은 client-supplied이며 서버 ledger가 없고, fingerprint stale check는 request version/CAS가 아니다. 따라서 forged/replayed Proposal 및 TOCTOU를 안전하게 해결한 상태가 아니다.
- client-held full state는 API 응답/다음 요청에서만 사실상 이어진다. 다음 단계는 공식 Request 저장·조회 권위를 만들기 전 이를 서버 State처럼 가정하면 안 된다.
- normalizer가 context/type 전환에서 inactive conditions 또는 invalid Matrix mapping을 제거할 수 있다. dry-run은 해당 영향을 보여야 하지만 값 retention policy를 005에서 결정하지 않는다.
- active Word는 browser-rendered DOM을 신뢰하는 기존 제약이 있다. canonical State refresh/readiness/DOM staleness guard는 후속 action-level 설계 대상이다.

# 발견된 위험

| 위험 | 영향 | 최소 완화 및 담당 단계 |
|---|---|---|
| API 호환성 파괴 | 기존 form/UI consumer 중단 | 기존 endpoint/shape를 유지하고 017~020에서 additive 경로만 추가한다. |
| 직접 form mutation 또는 optimistic UI | 승인 전 사용자 입력/공식 state 불일치 | 018~020은 pending Proposal 표시만 하고 approved result re-read 후 반영한다. |
| LLM 권한 확대 | 추론값·비허용 path·계산값이 Request에 유입 | LLM output은 sanitizer 앞 비신뢰 DTO이며 기존 engines의 권위를 침범하지 않는다. |
| RAG answer-to-patch | 근거 답변이 무승인 Request 변경으로 전환 | Q&A/RAG는 read-only로 고정한다; 명시 값 입력과 Proposal lifecycle 없이는 patch가 되지 않는다. |
| legacy geometry state 저장 | Case Matrix/renderer가 무시하는 비정규 상태 | Adapter가 canonical cards만 만든 뒤 normalizer를 통과시킨다. |
| stale/replay/ledger 부재 | 재전송·동시 변경·위조 Proposal 적용 | 007~009의 latest-read/version/CAS/ledger 전까지 완료 위험으로 선언하지 않는다. |

# 다음 단계에서 반드시 참고할 내용

- H5-ORCH-006은 legacy LLM DTO를 늘리기보다 canonical field binding과 existing normalizer authority를 registry로 노출해야 한다.
- H5-ORCH-007~009는 client-supplied state/Proposal을 권위로 쓰지 말고 server latest-read, request version/CAS, proposal ledger, terminal status와 exactly-once apply를 설계·검증해야 한다.
- H5-ORCH-014~016은 이 문서의 LLM-only structured output 및 read-only Q&A/RAG 계약을 wrapper/service로 보존해야 하며, 새 rule extractor/router를 만들면 안 된다.
- H5-ORCH-018~020은 API 호환성과 existing form state를 보존하고, 승인 전 form state 불변 및 승인 후 canonical refresh를 focused test로 고정해야 한다.

# 다음 단계 수정이 예상되는 파일

이 단계에서는 예상 위치만 기록하며 변경하지 않는다.

- `request_ai_agent_h5_v0/chat_patch.py`, `llm_client.py`, `app.py`: 014~017에서 adapter/service/API 경계를 additive하게 연결할 후보
- `request_ai_agent_h5_v0/schema.py`, `state.py`, `condition_fieldsets.py`: 006 registry와 canonical binding의 참조 후보 (기존 rules 재작성 금지)
- 새 bounded service/model/store module: 007~013의 version, Proposal, Conversation, workflow, planner 후보
- `request_ai_agent_h5_v0/ui.py`: 018~020의 additive panel/card/sync 후보
- `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py` 및 새 focused `tests/test_orchestrator_*.py`: mock-only contract regression 위치

# 후속 개선 후보

- conditional inactive-value retention/audit envelope의 명시 정책
- Word action 직전 canonical readiness와 DOM staleness guard
- H5-ORCH-029에서 출처 기반 RAG 안내와 workflow 복귀를 추가하되 answer-to-patch 금지 유지

# Roadmap 변경 필요 여부

없음. Worker는 Roadmap 상태, 기준 카드, 다음 단계 프롬프트를 변경하지 않는다. H5-ORCH-005는 Reviewer 검토 대기 상태로 남긴다.

# Git 상태와 Commit 여부

- 시작 시 기존 untracked automation/run 문서와 `__pycache__`가 있어 보존했다.
- 이번 작업의 의도된 변경은 이 인수인계 문서 1건이다.
- 커밋 여부: 검증 결과 확인 후에도 Worker가 Roadmap 상태를 확정하지 않으며, 커밋은 수행하지 않는다.

# Worker 보고서

최소 변경 계약을 문서로 확정했다. 기준선은 `69f9374`의 LLM-only structured output과 geometry Adapter이며, 흐름은 `LLM intent -> sanitizer -> geometry Adapter -> Proposal/dry-run -> approved apply`다. Proposal/dry-run 및 모든 Q&A/RAG 실패는 read-only, `state_changed=false`로 유지한다. `geometry.products`는 LLM-facing legacy DTO만으로 남고 canonical base/comparison product cards로 Adapter 변환된다. client-held state, stale/replay, Proposal ledger와 latest-read/version/CAS는 H5-ORCH-007~009의 미해결 선행 과제다. Reviewer가 실제 diff와 mock 회귀 결과를 검토하기 전까지 완료 상태를 확정하지 않는다.
