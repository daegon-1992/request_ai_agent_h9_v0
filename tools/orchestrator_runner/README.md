# H5-ORCH PowerShell Runner

`Invoke-H5Orchestrator.ps1` is the single-process Windows PowerShell runner for the H5-ORCH Worker → Reviewer → Planner loop.

It reads the user-requested profile policy from `model_profiles.json`, creates an exclusive lock, writes the state atomically, emits a separate `codex exec --json` event log for every role, and records the final message and execution metadata under `docs/orchestrator_handoff/runs/`.

The Runner never selects a default model: every invocation specifies `--model` and `model_reasoning_effort`. Profiles are limited to Terra/Luna at `low`, `medium`, or `high`; Luna is disabled until the CLI can establish its availability.

Run the required non-mutating mock validation first:

```powershell
& .\tools\orchestrator_runner\Invoke-H5Orchestrator.ps1 -Mock
```

After it reports `READY`, start (or continue from a safe checkpoint) with:

```powershell
& .\tools\orchestrator_runner\Invoke-H5Orchestrator.ps1 -Run
```

Inspect durable state with:

```powershell
& .\tools\orchestrator_runner\Invoke-H5Orchestrator.ps1 -Status
```

When the Runner enters `BLOCKED`, correct only the recorded blocking condition, then use `-Resume`. The Runner intentionally does not reset files, push, deploy, or delete pre-existing `__pycache__` content.
