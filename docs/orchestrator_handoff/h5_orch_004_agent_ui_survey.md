# 단계 정보

- 단계 ID: H5-ORCH-004
- 단계명: Agent·Q&A·RAG·추출·UI 조사
- 수행 기준 프로젝트 루트: `request_ai_agent_h5_v0`
- 수행 기준 코드 버전 또는 Commit: `dfd6655` (조사 시작 시 `HEAD`)
- Roadmap 버전: 0.5
- 작업 상태: 완료 후보 — Reviewer 검토 대기

# 이번 단계 목표

기존 h5_v0의 규칙/LLM 입력 추출, Chat Proposal, 입력 도움말·일반 Q&A·RAG Q&A 및 내장 UI의 실제 입출력 경계를 읽기 전용으로 확인했다. 후속 H5-ORCH-005, 014~016, 018~020이 기존 기능을 대체하지 않고, 승인 전 Request State를 바꾸지 않도록 재사용 지점과 위험을 기록한다.

# 사전 입력 문서

- `AGENTS.md`
- `docs/orchestrator_handoff/orchestrator_roadmap.md`
- `docs/orchestrator_handoff/prompts/common_stage_contract.md`
- `docs/orchestrator_handoff/prompts/baseline_prompts.md`
- `docs/orchestrator_handoff/prompts/manual_stage_execution.md`
- `docs/orchestrator_handoff/h5_orch_001_repo_map.md`
- `docs/orchestrator_handoff/h5_orch_002_state_proposal_survey.md`
- `docs/orchestrator_handoff/h5_orch_003_rules_engines_survey.md`

공통 제약을 그대로 따른다: 기존 form/API 유지, 최신 Request 재조회·version 확인, 모든 Agent 변경의 Proposal+사용자 승인, LLM의 조건·필수·계산·검증 결정 금지, 기존 Fieldset·Validator·Case Matrix·Preview·Word·RAG 재사용이다.

# 실제 수행 내용

## 입력·출력과 권한 경계

| 영역 | 실제 입력 → 출력 | state_changed/read_only 근거 | 활성화·실패 경계와 재사용 지점 |
|---|---|---|---|
| 규칙 추출 | `chat_patch.extract_patch_proposal(message, state)` → 보수적 `operations`, `warnings`, `questions`, `status` | 생성 Proposal은 `state_changed=False`, `read_only=True` (`chat_patch.py:635-682`). | `set`은 `_SET_ALLOWED_PATHS`, list는 `geometry.products/parts`, condition은 알려진 `CONDITION_FIELD_SPECS` key만 수용한다 (`:494-566`). 새 추출기는 이 sanitizer/DTO를 통과해야 한다. |
| LLM form 추출 | message + `summarize_current_state(base_state)` + `get_public_schema()` → JSON object의 `operations/summary/questions/warnings` | system prompt도 직접 state 변경 금지·명시값만 추출을 지시하며, 결과는 `proposal_from_operations()`으로 재-sanitize한다 (`llm_client.py:251-326`, `app.py:1041-1080`). | `REQUEST_AGENT_LLM_FORM_EXTRACTION_ENABLED=false` 또는 `llm_status().ready=false`면 미사용. 호출 예외는 operation 없는 warning Proposal로 바뀌며 적용하지 않는다. |
| LLM client | Azure messages → content/raw/deployment/api_version | `azure_chat_completion()`은 호출 helper일 뿐 State API를 알지 못한다 (`llm_client.py:100-164`). | `REQUEST_AGENT_LLM_ENABLED`, endpoint, deployment, API key가 모두 준비되어야 ready (`:64-98`). 400의 `max_completion_tokens`만 `max_tokens`로 한 번 재시도; HTTP/URL 오류는 `RuntimeError`. 실제 호출은 하지 않았다. |
| Chat Proposal/dry-run | `/api/chat/propose` 또는 `/api/chat/send` patch branch: message + browser `state` → assistant, Proposal, dry-run State/Matrix/validation/submission | propose/send 응답은 명시적으로 `state_changed=False`이며 `_store_pending_proposal()`은 server storage 없이 browser Proposal에 fingerprint만 stamp한다 (`app.py:499-503, 1659-1682, 1770-1815`). dry-run은 `apply_patch_operations()`의 복사본이다. | `chat_patch.proposal_response()`을 규칙 baseline으로 쓰고 LLM 결과를 merge한 뒤에도 sanitizer를 거친 operation만 남는다. |
| 승인/거절 | `/api/chat/apply`: client Proposal + 최신 browser state → normalized State; `/api/chat/reject` → rejected Proposal | apply만 `apply_patch_operations(base_state, operations)` 뒤 `state_changed=True`; reject는 false (`app.py:1684-1768`). | stale/replay/ledger의 설계 상세는 H5-ORCH-002를 재사용한다. 이 조사에서 확인한 최소 사실은 apply가 client-supplied Proposal과 client-supplied base state를 받으므로 후속 server-authoritative contract가 필요하다는 점이다. |
| 입력 도움말·현재 입력 Q&A | `_local_chat_answer()` 또는 `run_rag_qa()` → 안내 텍스트/structured state summary | `field_help`, stage/service/form guidance, current-input 모두 `state_changed=False`; current-input QA는 `read_only=True` (`app.py:973-1000`, `rag_qa.py:325-392`). | `현재 입력` 유형은 문서 검색을 하지 않고 sanitized structured State만 요약한다. |
| 일반 Q&A | non-patch, non-local, non-RAG message + state summary → LLM 답변 또는 제한 안내 | `/api/chat/send` general branch의 `chat_result.state_changed=False`, top-level false (`app.py:1023-1039, 1817-1836`). | LLM 미준비 시 일반 Q&A 분류와 안내만 유지; LLM 예외도 fallback 텍스트와 `{used:false,error}`이다. |
| RAG Q&A | question + sanitized state summary → query, sources, confidence, limitations, answer | `run_rag_qa()`의 모든 반환은 `read_only=True`, `state_changed=False` (`rag_qa.py:325-430`); hit record도 `read_only=True` (`rag_search.py:823-837`). | RAG On은 `metadata.rag_enabled`; Off면 문서성 질문은 `_rag_disabled_qa()`이고 외부 검색을 하지 않는다 (`app.py:93-112, 175-190, 1723-1767`). 검색은 local text 또는 Chroma SQLite read와 선택적 embedding query가 전제이며 (`rag_search.py:142-236, 868-956`) 외부 RAG/vector store/DB는 호출하지 않았다. |
| RAG LLM 보조 | 검색된 `qa`의 context/sources → rerank 또는 출처 안의 한국어 답변 | rerank/answer는 QA DTO만 바꾸며 Request State를 쓰지 않는다 (`rag_qa.py:397-430`, `llm_client.py:185-216, 328-413`). | ready가 아니거나 rerank/answer 예외면 원래 keyword/vector 검색 답변을 보존하고 `{used:false,error}`을 반환한다. |
| UI chat/Proposal | `collectState()` + message → `/api/chat/send`; response assistant/Proposal/QA → chat DOM | Proposal 응답의 `dry_run`은 UI가 채택하지 않는다. `sendChatMessage()`는 응답 `state`가 있을 때만 `syncEditorFromState()`를 부르고, pending Proposal은 카드에만 보관한다 (`ui.py:1822-1905, 1992-2028`). | `applyChatProposal()`의 Yes만 `/api/chat/apply` 호출 후 `adoptStateFromResponse()`와 editor sync를 수행한다 (`:1881-1905`). |

`FEATURE_LOCKS`에서 현재 analysis-type recommendation과 condition recommendation은 false이고 route도 즉시 403 disabled payload를 반환한다 (`app.py:62-72, 1355-1410`). UI에 남은 추천 호출부도 조기 return으로 비활성 안내만 낸다 (`ui.py:1948-1981`). 이는 새 Orchestrator가 기존 잠금 기능을 몰래 활성화하거나 재구현하면 안 되는 근거다.

## structured output/operation 안전성

LLM structured output은 Azure API의 provider-native JSON mode가 아니라 “JSON object만”이라는 prompt와 `_json_object_from_text()`의 `json.loads`/중괄호 fallback 조합이다 (`llm_client.py:166-183, 251-326`). 따라서 malformed JSON은 빈 payload가 되고 `proposal_from_operations()`은 `needs_clarification` 또는 `noop`로 남는다. 외부/LLM operation은 허용 op, path, known condition key, non-empty value, confidence, merge strategy를 다시 제한한다. `merge_patch_proposals()`도 LLM operation이 존재하면 그 목록을 선택한 뒤 중복 제거한다 (`chat_patch.py:568-619`).

후속 DTO는 raw LLM JSON을 Request patch로 신뢰하면 안 된다. `ExtractionCandidate`와 `Proposal`을 분리하고, candidate가 반드시 기존 `sanitize_external_operations()`의 allowlist를 지난 canonical operation 집합임을 계약으로 둬야 한다. LLM에는 값 후보·질문·근거 설명 권한만 부여하고 field activation, required, calculation, validation, case/condition binding 결정권을 주지 않는다.

## 대표 메시지 정적 end-to-end 추적

대표 입력은 **“제품 모델은 A100, B200으로 입력해줘.”**로 선택했다. 명시적 제품값과 편집 의도가 함께 있어 Proposal 정상 경계를 가장 작게 보여 준다.

1. `ui.py:1992-2028`의 `sendChatMessage()`가 사용자 메시지를 chat history에 표시하고 `collectState()` snapshot과 `{mode:"auto"}`를 `/api/chat/send`로 POST한다. 이 호출 전/후 Proposal operation을 DOM form field에 쓰지 않는다.
2. `app.py:1770-1815`가 규칙 `extract_patch_proposal()`을 먼저 실행한다. `chat_patch.py:254-332`의 geometry extractor가 명시 모델을 `list_values`, `path="geometry.products"`, `values=["A100","B200"]` 후보로 만들고 `:635-682`가 pending Proposal을 만든다. `edit_intent`와 pending이므로 auto mode는 `input_proposal`로 분기한다.
3. `_proposal_response_with_llm()`은 규칙 Proposal과, 준비된 경우에만 LLM 후보를 merge한다 (`app.py:1082-1107`). LLM Off/미준비 또는 extraction flag Off라면 규칙 Proposal과 규칙 dry-run만 반환한다. LLM 호출 실패라면 warning을 가진 operation 없는 LLM Proposal이 생성되어 merge 후 기존 규칙 후보가 유지된다.
4. `proposal_response()`/`apply_patch_operations()`은 `deepcopy(base_state)`에만 후보를 적용하고 `sanitize_state()`/validator를 거쳐 dry-run State·Case Matrix·validation을 만든다 (`chat_patch.py:745-781`). `/api/chat/send` 응답은 `proposal`, `dry_run`, `state_changed:false`를 반환한다. 따라서 후보값은 response DTO에는 있지만 Request State mutation이 아니다.
5. UI는 `renderProposalMessage()`가 operations와 Yes/No 버튼을 가진 카드로 표시하고 `pendingChatProposals` map에만 보관한다 (`ui.py:1822-1867, 2015-2021`). `dry_run.state`는 채택하지 않는다. Yes 후에만 `applyChatProposal()`이 `/api/chat/apply`로 Proposal과 새 `collectState()`를 보내고 server response의 `state`를 `adoptStateFromResponse()`/`syncEditorFromState()`로 반영한다. No는 `/api/chat/reject`만 호출한다.

별도 Q&A/RAG 경계도 확인했다. 예를 들어 “현재 입력 상태를 요약해줘”는 patch가 아니라 `_local_chat_answer()`의 `current_state`로 먼저 분기해 sanitized State summary만 반환한다. “SOP 근거를 알려줘”는 `metadata.rag_enabled=true`일 때 document RAG로 가고, false일 때 `_rag_disabled_qa()`의 read-only 안내로 끝난다. RAG가 실제 실행되어도 `run_rag_qa()`는 source snippets/limitations만 반환한다. RAG LLM answer 또는 rerank가 실패해도 keyword/vector search의 read-only 답을 보존한다.

## UI/request-context 관련 최소 흐름

UI에는 Proposal과 별개의 정상 form editing client draft가 있다. `updateRequestContextDraft()`와 quick-prep selection은 `requestState.request_context`를 브라우저 메모리에서 즉시 바꾸며 (`ui.py:1025-1065`), Confirm/fieldset 호출 때만 server normalized State를 채택한다 (`:1090-1120`, `app.py:1148-1240`). 이는 Proposal 낙관 적용과 혼동하면 안 된다. chat user/assistant messages도 `metadata.chat_history` client draft에 추가된다 (`ui.py:1706-1740`).

반면 chat Proposal operations/dry-run은 이 direct form mutation 경로를 사용하지 않는다. 다만 현재 API가 browser supplied full `state`를 base로 받는 legacy 구조라서, 새 UI/service가 `requestState` client draft를 공식 최신 Request로 오인하거나 approval 전에 `dry_run.state`를 주입하면 state overwrite 위험이 생긴다. H5-ORCH-005/007/009/016은 apply 시 server의 최신 Request 재조회와 version/stale checks를 authority로 명시해야 한다. H5-ORCH-002의 ledger/replay 상세는 여기서 반복하지 않는다.

# 변경 파일

| 파일 | 변경 |
|---|---|
| `docs/orchestrator_handoff/h5_orch_004_agent_ui_survey.md` | 본 읽기 전용 조사 인수인계 문서 추가 |

# 추가 또는 변경된 데이터 구조

없음. 앱 State, Proposal, API DTO, DB schema, RAG index, prompt, UI를 변경하지 않았다.

조사에서 확인한 기존 재사용 DTO 경계는 다음과 같다.

- `PatchOperation`: `set | list_values | condition_values`, allowlisted path/key, label/confidence/source/merge strategy.
- `PatchProposal`: `proposal_id`, status/intent, message, canonical operations, summary/warnings/questions, `state_changed=False`, `read_only=True`, optional base schema version/fingerprint context.
- Chat response: assistant, mode/result, optional Proposal, dry-run (read-only prediction), optional QA/LLM diagnostics, top-level `state_changed`.
- RAG QA: question type/query/source records/confidence/limitations/answer plus `read_only=True`, `state_changed=False`.

# 추가 또는 변경된 API

없음. 조사한 기존 API는 `/api/chat/instant`, `/api/chat/propose`, `/api/chat/apply`, `/api/chat/reject`, `/api/chat/send`, `/api/rag/qa`, `/api/llm/status`, `/api/rag/status`, `/api/request-context/confirm`, `/api/request-context/fieldset`이다.

# 중요한 설계 결정

- Adapter는 기존 규칙 extractor와 LLM extractor의 output을 동일한 sanitized candidate/Proposal input으로 바꾸되, 승인 적용 authority를 갖지 않는다.
- Intent Router는 patch intent를 field help/current-input/general QA/RAG보다 먼저 또는 별도 명시 mode로 안전하게 분리하되, 기존 `_local_chat_answer()`와 `_should_use_document_rag()`의 read-only 분기를 대체하지 않는다.
- Orchestrator service는 conversation DTO와 Request snapshot을 분리하고, Proposal 생성 시 `state_changed=False`를 보장하며, 승인 시에만 최신 Request/version을 다시 읽어 lifecycle service에 위임해야 한다.
- UI 018은 chat panel만 추가/교체하고 legacy form draft와 chat history를 Request mutation authority로 승격하지 않는다. UI 019는 Proposal card의 diff/Yes/No만 표현하고 dry-run을 form에 미리 쓰지 않는다. UI 020은 approval 후 server State만 editor에 반영한다.

# 기존 기능 재사용 지점

| 후속 단계 | 반드시 재사용할 파일·계약 | focused test 위치/추가 관점 |
|---|---|---|
| H5-ORCH-005 | `chat_patch.py:sanitize_external_operations`, `proposal_from_operations`, `preview_patch`; `app.py:_proposal_response_with_llm`, `FEATURE_LOCKS`; H5-ORCH-002/003의 official state/fieldset contracts | `tests/test_task12_minimal_regression.py`; 신규 adapter test는 raw LLM operation 거절, dry-run 불변, legacy geometry/condition sanitizer 재사용을 좁게 검증 |
| H5-ORCH-014 | `llm_client.py:extract_form_patch_with_llm`, `chat_patch.py:494-619`, `rag_qa.summarize_current_state()` | mock LLM JSON의 allowlist/invalid JSON/LLM disabled/failure만 검증; 실제 Azure 호출 금지 |
| H5-ORCH-015 | `app.py:_looks_like_edit_intent`, `_local_chat_answer`, `_should_use_document_rag`, `rag_qa.classify_question` | field question→field_help, current-input→read-only summary, document question→RAG/Off fallback, explicit patch→Proposal |
| H5-ORCH-016 | `/api/chat/send` response shape, `_state_from_request`, Proposal/dry-run boundary, H5-ORCH-002 apply/version authority | Proposal 생성 전후 State 동일, approval 때 최신 snapshot/version 검증, Q&A/RAG branch state unchanged |
| H5-ORCH-018~020 | `ui.py:sendChatMessage`, `renderProposalMessage`, `applyChatProposal`, `rejectChatProposal`, `adoptStateFromResponse` | browser-unit/integration 수준에서 pending card가 dry-run을 editor에 쓰지 않고 Yes의 state response만 채택함을 검증 |

# 수행하지 않은 작업

- H5-ORCH-002의 server ledger, stale/replay/중복 적용, repository/version lifecycle 상세를 재조사하거나 변경하지 않았다.
- H5-ORCH-003의 Fieldset, Validator, Case Matrix, Preview/Word renderer 세부 경로를 재조사하거나 복제하지 않았다. 이 문서에서는 Proposal dry-run이 기존 `sanitize_state()`/validator를 통과한다는 경계와 legacy geometry/condition binding 위험만 참조한다.
- Prompt, 규칙 추출, LLM/API/UI/RAG 설정, tests, DB schema, Roadmap/기준 카드/다음 단계 prompt를 수정하지 않았다.
- 실제 Request, DB/vector store, Azure LLM, RAG search/embedding 또는 browser를 호출하지 않았다.

# 최소 검증

| 확인 | 결과 |
|---|---|
| 대표 메시지 정적 호출 추적 | 완료. `ui.py:1992-2028` → `app.py:1770-1870` → `chat_patch.py:635-781` → `ui.py:1822-1905`의 Proposal/dry-run/Yes 적용 경계를 위에 기록했다. |
| LLM/RAG 비활성·실패 정적 경로 | 완료. LLM disabled/not-ready/exception과 RAG Off/current-input/RAG LLM failure 경계를 코드로 확인했다. 실제 네트워크 호출은 하지 않았다. |
| 기존 focused regression | `G:\Tech\00_Agent\01_Agent_Code\.venv\Scripts\python.exe -m pytest request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`를 repository parent에서 먼저 실행하면 현재 실제 test 위치가 한 단계 더 안쪽이라 `0 collected / file or directory not found`였다. project root에서 같은 명령을 실행한 재시도는 `16 passed in 0.96s`였다. 여기에는 LLM explicit-disable 및 field question→field_help 회귀가 포함된다. |
| 문서 인코딩 | project root에서 `G:\Tech\00_Agent\01_Agent_Code\.venv\Scripts\python.exe tools/check_encoding.py --changed`: `Encoding check passed`. |
| diff 형식 | project root에서 `git diff --check`: 성공(출력 없음). |

# 실패하거나 수행하지 못한 검증

실제 LLM/RAG/외부 DB 및 browser E2E는 범위상 실행하지 않았다. 이들은 read-only/비활성/failure code path의 정적 확인과 focused regression으로 대체했다.

# 알려진 문제와 제한 사항

- LLM의 JSON parsing은 strict provider schema enforcement가 아니므로 sanitizer는 계속 최종 방어선이어야 한다.
- legacy chat apply는 client-supplied Proposal 및 full State를 받는다. fingerprint stale guard가 있어도 후속 official architecture는 client state를 source of truth로 사용하면 안 된다.
- `conditions.fields.*.values`와 legacy geometry/condition binding은 H5-ORCH-003이 확인한 dynamic Fieldset/normalizer authority를 거쳐야 한다. 자연어 candidate를 그 binding에 직접 쓰거나 별도 geometry/condition model을 만들면 Case Matrix/Validator와 불일치한다.
- UI의 request-context/chat-history client draft는 Proposal operations와 별개다. 새 conversation/session 설계는 이 메모리 값을 승인 전 Request State로 저장하거나 version으로 취급하지 않아야 한다.
- RAG가 실검색되는 경우 local files/Chroma SQLite 접근 및 선택적 embedding runtime이 필요하다. RAG answer는 source snippet 기반 설명이지 auto-patch 근거가 아니다.

# 발견된 위험

| 위험 | 근거와 영향 | 후속 대응 |
|---|---|---|
| 승인 전 optimistic State 적용 | Proposal response에 dry-run State가 있어 UI가 잘못 adopt하면 승인 전 Request가 바뀐다. 현재 UI는 이를 채택하지 않는다. | 005/016/019/020에서 `state_changed=false` response는 State replacement 금지로 계약화. |
| client-supplied Proposal/state | apply가 browser Proposal과 `collectState()` snapshot을 받는다. forged/stale payload 및 latest server state overwrite 위험이 있다. | 005/007~009/016에서 server latest-read/version/CAS 및 persisted Proposal authority를 확정. |
| LLM 권한 확장 | raw LLM JSON이 geometry/conditions/validation을 임의로 결정하면 003의 dynamic Fieldset/Case Matrix 계약을 깨뜨린다. | 014에서 allowlist sanitizer 뒤 candidate-only 권한, Fieldset/Validator/normalizer 재사용. |
| direct form mutation 혼동 | UI request-context/client chat history는 로컬 `requestState`를 직접 바꾼다. 이를 Agent approval 결과로 해석하면 안 된다. | 018~020에서 UI local draft, conversation state, server Request State를 명시적으로 분리. |
| legacy geometry/condition binding | `condition_values` key만으로 active card instance/Matrix visibility를 보장하지 않는다. | 005/014/016에서 003의 canonical sanitizer/fieldset adapter만 호출하고 legacy path 복제 금지. |
| RAG 답변의 patch 전환 | RAG는 read-only source evidence인데 자동 조건 반영으로 연결하면 근거·승인 경계를 위반한다. | 015/016/029에서 RAG는 guidance만, 변경은 별도 sanitized Proposal. |

# 다음 단계에서 반드시 참고할 내용

H5-ORCH-005는 002의 State/Proposal lifecycle 결론, 003의 Fieldset/Validator/Case Matrix authority, 본 문서의 candidate/intent/UI boundary를 하나의 최소 architecture로 결합해야 한다. 특히 Proposal generation과 dry-run은 어떠한 경우에도 Request write가 아니며, 기존 form context-confirm path와 Agent approval path는 구분되어야 한다.

H5-ORCH-014~016은 `chat_patch.py` allowlist와 `rag_qa.py` read-only DTO를 adapter 입력으로 재사용해야 한다. H5-ORCH-018~020은 pending Proposal을 화면 카드/state outside form으로 보관하고, approve response의 server State만 form에 반영해야 한다.

# 다음 단계 수정이 예상되는 파일

- H5-ORCH-005: `docs/orchestrator_handoff/h5_orch_005_target_architecture.md`만.
- H5-ORCH-014~016: H5-ORCH-005의 결정 후 새로운 adapter/router/service 모듈과 focused tests. 기존 `chat_patch.py`, `rag_qa.py`, `llm_client.py`는 우선 재사용 대상이다.
- H5-ORCH-018~020: H5-ORCH-017 API contract 후 chat UI component/`ui.py`의 최소 연결과 focused UI/integration tests. 기존 form·Preview/Word renderer는 재구현 대상이 아니다.

# 후속 개선 후보

- provider-native structured schema 또는 strict JSON validation을 검토하되, 기존 sanitizer를 제거하지 않는다.
- server-persisted Proposal ID/version/fingerprint와 conversation state를 분리해 client-supplied full Proposal/state 의존을 제거한다.
- RAG source citation DTO를 conversation response에 유지하되 RAG evidence에서 Request operation으로 직접 변환하지 않는다.

# Roadmap 변경 필요 여부

없음. Worker는 Roadmap 상태, 기준 카드, 현재/다음 단계 prompt를 변경하지 않았다. 완료 표시는 Reviewer 판단 전까지 검토 대기다.

# Git 상태와 Commit 여부

- 이 단계에서 추가한 파일: `docs/orchestrator_handoff/h5_orch_004_agent_ui_survey.md`.
- 시작 시 이미 존재한 사용자 변경: Roadmap/current/review prompt 수정, 001~003 문서 및 automation/runs/cache 관련 untracked 항목. 보존했고 수정하지 않았다.
- Commit 여부: 하지 않음. Reviewer 검토 후 상태 확정이 필요하다.

# Worker 보고

조사 문서 한 건만 추가했다. 규칙·LLM 추출은 모두 sanitized pending Proposal과 read-only dry-run을 만들며, `/api/chat/apply`의 Yes 경로만 State를 바꾼다. UI도 현재 pending Proposal/dry-run을 form에 쓰지 않고 Yes 후 server State만 채택한다. Q&A/RAG는 current-input 요약, 일반 Q&A, 문서 RAG 및 RAG Off/LLM failure 모두 read-only 응답으로 분리된다. Reviewer는 client-supplied Proposal/state 및 legacy geometry/condition binding 위험이 후속 architecture와 tests에 반영됐는지 확인해야 한다.
# H5-ORCH-004 구현 정합화 부록 (2026-07-31, 우선 적용)

이 부록은 `69f9374 feat: adapt LLM geometry proposals safely` 기준의 현재 구현을
조사 기준선으로 고정한다. 아래의 이전 조사 본문에서 규칙 기반
`extract_patch_proposal`, `merge_patch_proposals`, `_local_chat_answer` 또는
`_should_use_document_rag`가 활성 경로라고 설명한 부분은 역사적 기록이며,
이 부록과 충돌할 경우 이 부록이 우선한다. H5-ORCH-004 상태는 **Reviewer 검토 대기**다.

## 현재 계약

| 경계 | 입력 | 출력 | Request State 경계 |
|---|---|---|---|
| LLM 분류/추출 | 메시지, sanitized state summary, public schema | `intent` (`patch`, `general_qa`, `rag_qa`, `current_input`, `needs_clarification`)와 JSON `operations` | LLM은 후보 DTO만 반환하며 state를 쓰지 않는다. |
| operation sanitizer | LLM operation | allowlisted `set`, `list_values`, `condition_values`만 포함한 Proposal operation | 허용되지 않은 path/key/op는 Proposal과 apply 양쪽에서 제외한다. |
| geometry Adapter | LLM `list_values: geometry.products` | canonical `geometry.base_product` 및 `geometry.comparison_products` 카드 | legacy `geometry.products` 필드는 state에 저장하지 않는다. 정상화 후 기존 Case Matrix/Validator가 canonical card를 사용한다. |
| Proposal/dry-run | 후보 operation과 browser state snapshot | pending Proposal, cloned/normalized dry-run, `state_changed=false` | UI는 dry-run을 form state로 채택하지 않는다. |
| 승인 apply | pending Proposal, 최신 base state | normalized canonical state, `state_changed=true` | 승인 endpoint만 operation을 적용한다. H5-ORCH-002의 client-held state/stale/replay 위험은 후속 server-authoritative version 계약에서 해소한다. |
| current input | LLM `current_input` intent + state | structured state summary QA | RAG 호출이나 mutation 없이 `read_only=true`, `state_changed=false`다. |
| general QA | LLM `general_qa` intent | LLM 답변 또는 unavailable 안내 | 항상 read-only다. 추출 실패는 general QA로 우회하지 않고 clarification으로 끝난다. |
| RAG QA | LLM `rag_qa` intent 또는 명시적 rag mode | source/limitation QA DTO | `metadata.rag_enabled=false`이면 검색하지 않고 disabled DTO를 반환한다. 검색 예외도 error DTO로 변환하며 mutation은 없다. |

## 대표 경로: “제품 모델은 A100, B200으로 입력해줘.”

1. `ui.py`의 `sendChatMessage()`가 `collectState()` snapshot과 메시지를 `/api/chat/send`에 보낸다.
2. `app.py:_proposal_response_with_llm()`이 LLM structured output을 받고,
   `chat_patch.proposal_from_operations()`/`sanitize_external_operations()`으로 제한한다.
3. LLM 후보 `geometry.products=["A100", "B200"]`에는
   `geometry_products_to_complete_product_cards` Adapter metadata가 붙는다.
4. dry-run의 `apply_patch_operations()`은 복사본에서 Adapter를 실행해
   `base_product.drawing_no=A100`, `comparison_products[0].drawing_no=B200`을 만든 뒤
   기존 `sanitize_state()`와 validator를 거친다. Case Matrix의 geometry option도
   `A100`, `B200`을 사용한다.
5. `/api/chat/send`은 Proposal/dry-run만 반환하고 `state_changed=false`다. 원래 Request는
   유지된다. UI는 pending Proposal 카드만 표시한다.
6. 사용자가 Yes를 눌러 `/api/chat/apply`를 호출할 때만 동일 Adapter 결과가 canonical
   Request state로 적용된다. No/reject와 모든 Q&A 응답은 state를 바꾸지 않는다.

## feature lock 및 실패 경로

- LLM extraction disable/not-ready/예외: operation 없는 `needs_clarification` Proposal,
  `state_changed=false`. 규칙 기반 값/intent 추출로 fallback하지 않는다.
- invalid LLM operation: sanitizer가 제거하고 patch intent를 clarification으로 격하시킨다.
- `current_input`: canonical state 요약만 반환하며 RAG를 호출하지 않는다.
- RAG disabled: 외부 검색을 호출하지 않는 `rag_disabled` QA DTO를 반환한다.
- RAG exception: `rag_error`, `read_only=true`, `state_changed=false` QA DTO로 변환한다.
- 기존 analysis-type/condition recommendation feature lock은 변경하지 않는다.

## 002·003과 만나는 위험 및 재사용 경계

- client-supplied Proposal/full state와 stale/replay/ledger 상세는 H5-ORCH-002의 범위다.
  이 단계는 Proposal이 승인 전 불변이라는 현재 경계만 재확인한다.
- Fieldset 활성화, canonical normalization, Validator, Case Matrix, Preview/Word renderer는
  H5-ORCH-003의 authority를 그대로 사용한다. LLM/Adapter는 이를 재구현하거나 우회하지 않는다.
- UI의 일반 form draft/request-context 변경과 Agent Proposal apply를 혼동하면 안 된다.
  chat dry-run은 optimistic form mutation 근거가 아니다.

## 후속 단계 인수인계

| 단계 | 반드시 재사용할 계약 | focused test 경계 |
|---|---|---|
| 005 | `chat_patch.sanitize_external_operations`, `proposal_from_operations`, Adapter, `apply_patch_operations`; 002/003 state authority | Adapter dry-run/apply, canonical Matrix/Validator, 승인 전 원본 state 불변 |
| 014 | `llm_client.extract_form_patch_with_llm`의 intent+operation DTO 및 sanitizer | mock LLM 정상/disabled/error/invalid operation. 실제 Azure 호출 금지 |
| 015 | `LLM_CHAT_INTENTS`, `/api/chat/send`의 resolved mode | patch/general/rag/current_input/clarification 각각 무변경 또는 Proposal 경계 |
| 016 | Proposal/dry-run/read-only response DTO, 기존 apply lifecycle | 최신 state/version 재조회는 002 계약으로 강화하고 direct patch 금지 |
| 018~020 | `ui.py` pending Proposal card/Yes-No/adopt-state 경계 | dry-run 미채택, Yes 응답만 form sync, stale/validation error UI |

## 검증 기준

- mock만 사용하여 실제 LLM/RAG/vector DB/Request를 호출하지 않는다.
- `request_ai_agent_h5_v0/tests/test_task12_minimal_regression.py`는 Adapter의 canonical
  geometry/Case Matrix, LLM unavailable/error/invalid operation, current-input, chat/direct
  RAG disabled/error, 승인 전 불변을 검증한다.
- 현재 기준: `python -m pytest` 23 passed, `tools/check_encoding.py --all` passed,
  `git diff --check` passed.
