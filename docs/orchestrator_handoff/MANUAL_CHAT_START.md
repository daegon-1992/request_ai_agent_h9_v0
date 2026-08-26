# 수동 단계 실행 시작 프롬프트

아래 블록 전체를 새 Codex 채팅의 첫 요청으로 붙여넣는다. 자동 Runner를 실행하지 않고 한 단계씩 진행할 때 사용한다.

```text
이 저장소에서 h5_v0 오케스트레이터를 수동 단계 방식으로 진행한다.

먼저 AGENTS.md와 다음 문서를 순서대로 읽어라.
1. docs/orchestrator_handoff/README.md
2. docs/orchestrator_handoff/orchestrator_master_plan.md
3. docs/orchestrator_handoff/orchestrator_roadmap.md
4. docs/orchestrator_handoff/prompts/common_stage_contract.md
5. docs/orchestrator_handoff/prompts/baseline_prompts.md
6. docs/orchestrator_handoff/prompts/manual_stage_execution.md
7. docs/orchestrator_handoff/prompts/current_stage.md

자동 Runner, 자동 연속 실행, 다음 단계 자동 실행은 수행하지 마라.
현재 단계 프롬프트의 Worker 역할만 수행하고, 완료 후 지정된 인수인계 문서와 Worker 보고서를 남겨라.
Roadmap 상태와 다음 단계 프롬프트는 변경하거나 확정하지 말고 Reviewer 검토 대기로 남겨라.
```
