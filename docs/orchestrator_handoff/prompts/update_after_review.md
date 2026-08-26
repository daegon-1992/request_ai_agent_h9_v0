# Reviewer 이후 Roadmap·다음 실행 프롬프트 갱신

각 단계의 Reviewer가 끝난 뒤 아래 블록에서 `<ID>`를 실제 단계 번호로 바꿔 실행한다.

```text
H5-ORCH-<ID>의 Reviewer 결과를 기준으로 Roadmap과 이후 실행 프롬프트를 갱신하라.

AGENTS.md, 최신 Roadmap, 해당 단계 인수인계 문서, Reviewer 결과, 실제 git diff와 테스트 결과,
common_stage_contract.md 및 baseline_prompts.md를 읽어라.

Reviewer의 safe_to_continue가 false이면 해당 단계만 중단 또는 부분 완료 상태로 정확히 기록하고,
필요한 사용자 결정 또는 최소 보완 작업을 보고하라. 다음 단계 프롬프트는 생성하지 마라.

safe_to_continue가 true이면 다음을 수행하라.
1. Roadmap의 해당 단계 상태와 변경 이력을 갱신한다.
2. 실제 결과에 영향을 받는 미완료 단계만 식별한다.
3. docs/orchestrator_handoff/prompts/current_stage.md를 다음 실행할 단계의 완성형 Worker 프롬프트로 갱신한다.
4. docs/orchestrator_handoff/prompts/review_current_stage.md를 그 단계의 독립 Reviewer 프롬프트로 갱신한다.
5. 필요하고 안전한 보완만 보조 ID로 추가하며 근거를 Roadmap에 남긴다.

완료된 단계의 ID·사실·인수인계 결과는 변경하지 마라. DB migration, API 호환성 파괴,
데이터 손실 위험, 추가 권한, 요구사항 충돌은 자동 결정하지 말고 중단 사유로 보고하라.
마지막에 다음 Worker에서 그대로 사용할 current_stage.md 경로와 선행 조건·검증 명령을 제시하라.
```
