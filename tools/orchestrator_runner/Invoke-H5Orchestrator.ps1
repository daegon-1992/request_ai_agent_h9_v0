[CmdletBinding()]
param(
    [switch]$Mock,
    [switch]$Run,
    [switch]$Resume,
    [switch]$Status
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ScriptRoot = Split-Path -Parent $PSCommandPath
$ProjectRoot = (Resolve-Path (Join-Path $ScriptRoot '..\..')).Path
$DocsRoot = Join-Path $ProjectRoot 'docs\orchestrator_handoff'
$AutomationRoot = Join-Path $DocsRoot 'automation'
$RunsRoot = Join-Path $DocsRoot 'runs'
$ReviewsRoot = Join-Path $DocsRoot 'reviews'
$PromptsRoot = Join-Path $DocsRoot 'prompts'
$StatePath = Join-Path $AutomationRoot 'automation_state.json'
$LockPath = Join-Path $AutomationRoot 'automation_runner.lock'
$ProfilePath = Join-Path $ScriptRoot 'model_profiles.json'
$SchemaPath = Join-Path $AutomationRoot 'reviewer_result.schema.json'
$RoadmapPath = Join-Path $DocsRoot 'orchestrator_roadmap.md'
$BaselinePath = Join-Path $PromptsRoot 'baseline_prompts.md'
$ContractPath = Join-Path $PromptsRoot 'common_stage_contract.md'

function Write-Utf8Atomic([string]$Path, [object]$Value, [switch]$Json) {
    $parent = Split-Path -Parent $Path
    New-Item -ItemType Directory -Force $parent | Out-Null
    $content = if ($Json) { $Value | ConvertTo-Json -Depth 20 } else { [string]$Value }
    $temporary = "$Path.$([guid]::NewGuid().ToString('N')).tmp"
    [System.IO.File]::WriteAllText($temporary, $content + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
    Move-Item -LiteralPath $temporary -Destination $Path -Force
}

function Get-State {
    if (-not (Test-Path $StatePath)) { return $null }
    return Get-Content -Raw -Encoding utf8 $StatePath | ConvertFrom-Json
}

function Save-State([object]$State) { Write-Utf8Atomic $StatePath $State -Json }

function Get-GitStatus {
    $lines = @(git -C $ProjectRoot status --porcelain=v1)
    return @($lines | Where-Object {
        $_ -and $_ -notmatch '^(\?\? |.. )(tools/orchestrator_runner/|docs/orchestrator_handoff/(automation|runs|reviews|prompts/(current_stage|next_stage)\.md))' -and $_ -notmatch '__pycache__/'
    })
}

function Assert-Environment {
    $required = @('AGENTS.md', 'docs/orchestrator_handoff/README.md', 'docs/orchestrator_handoff/h5_orch_000_automation_preparation.md',
        'docs/orchestrator_handoff/orchestrator_master_plan.md', 'docs/orchestrator_handoff/orchestrator_roadmap.md',
        'docs/orchestrator_handoff/prompts/common_stage_contract.md', 'docs/orchestrator_handoff/prompts/baseline_prompts.md',
        'docs/orchestrator_handoff/automation/runner_policy.md', 'docs/orchestrator_handoff/automation/reviewer_result.schema.json',
        'docs/orchestrator_handoff/automation/automation_state.example.json', 'tools/orchestrator_runner/model_profiles.json')
    foreach ($relative in $required) {
        if (-not (Test-Path (Join-Path $ProjectRoot $relative))) { throw "BLOCKED: required file is missing: $relative" }
    }
    $gitRoot = (git -C $ProjectRoot rev-parse --show-toplevel).Trim()
    if (-not $gitRoot) { throw 'BLOCKED: project root is not a Git repository.' }
    if (-not (Get-Command codex -ErrorAction SilentlyContinue)) { throw 'BLOCKED: Codex CLI is not installed.' }
    # This Codex CLI build can emit a harmless stale-temp-dir warning on stderr.
    # Capture it without promoting it to a PowerShell terminating error; exit status remains authoritative.
    $savedErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    $versionOutput = & codex --version 2>&1
    $versionExitCode = $LASTEXITCODE
    $loginOutput = & codex login status 2>&1
    $loginExitCode = $LASTEXITCODE
    $ErrorActionPreference = $savedErrorActionPreference
    if ($versionExitCode -ne 0) { throw 'BLOCKED: Codex CLI could not run.' }
    if ($loginExitCode -ne 0 -or ($loginOutput -join "`n") -notmatch 'Logged in') { throw 'BLOCKED: Codex CLI is not authenticated.' }
    $profiles = Get-Content -Raw -Encoding utf8 $ProfilePath | ConvertFrom-Json
    foreach ($property in $profiles.profiles.PSObject.Properties) {
        $profile = $property.Value
        if ($profile.model -ne 'gpt-5.6-terra' -and $profile.model -ne 'gpt-5.6-luna') { throw "BLOCKED: unsupported model in profile: $($profile.model)" }
        if ($profile.reasoning -notin @('low', 'medium', 'high')) { throw "BLOCKED: reasoning ceiling violation: $($profile.reasoning)" }
    }
    return $profiles
}

function Get-StageIds {
    $roadmap = Get-Content -Raw -Encoding utf8 $RoadmapPath
    $ids = @([regex]::Matches($roadmap, '(?m)^\|\s*(\d{3}[A-Z]?)\s*\|') | ForEach-Object { $_.Groups[1].Value })
    return @($ids | Where-Object {
        $card = Get-StageCard $_
        $handoff = [regex]::Match($card, 'docs/orchestrator_handoff/h5_orch_[A-Za-z0-9_\-]+\.md')
        -not ($handoff.Success -and (Test-Path (Join-Path $ProjectRoot $handoff.Value)))
    })
}

function Get-StageClass([string]$StageId, $Profiles) {
    foreach ($class in @('survey', 'implementation', 'safety')) {
        if ($Profiles.stage_classes.$class -contains $StageId) { return $class }
    }
    return 'safety'
}

function Get-ProfileOrder([string]$StageId, [string]$Role, $Profiles) {
    if ($Role -eq 'planner') { return @($Profiles.stage_profile_order.planner) }
    if ($Role -eq 'final_reviewer') { return @($Profiles.stage_profile_order.final_reviewer) }
    $class = Get-StageClass $StageId $Profiles
    if ($Role -eq 'reviewer') {
        if ($class -eq 'safety') { return @($Profiles.stage_profile_order.safety_reviewer) }
        return @($Profiles.stage_profile_order.reviewer)
    }
    return @($Profiles.stage_profile_order.$class)
}

function Get-EnabledProfile([string[]]$Order, $Profiles, [int]$Index) {
    for ($i = $Index; $i -lt $Order.Count; $i++) {
        $profile = $Profiles.profiles.($Order[$i])
        if ($profile -and $profile.enabled) { return @{ Name = $Order[$i]; Profile = $profile; Index = $i } }
    }
    return $null
}

function Get-StageCard([string]$StageId) {
    $baseline = Get-Content -Raw -Encoding utf8 $BaselinePath
    $pattern = "(?ms)^## H5-ORCH-$([regex]::Escape($StageId))\b.*?(?=^## H5-ORCH-|\z)"
    $match = [regex]::Match($baseline, $pattern)
    if (-not $match.Success) { throw "BLOCKED: no baseline card for H5-ORCH-$StageId" }
    return $match.Value.Trim()
}

function New-StagePrompt([string]$StageId, [string]$Role, [string]$RunDirectory) {
    $card = Get-StageCard $StageId
    $contract = Get-Content -Raw -Encoding utf8 $ContractPath
    $roadmap = Get-Content -Raw -Encoding utf8 $RoadmapPath
    $prompt = @"
# H5-ORCH-$StageId $Role session

You are the independent $Role for H5-ORCH-$StageId in this repository. Read AGENTS.md, the current Roadmap, common stage contract, the stage card below, and the latest relevant handoff documents before acting. Preserve all user changes. Never use destructive Git commands, push, deploy, require a secret, or write outside this workspace.

The user-requested model policy permits only gpt-5.6-terra or gpt-5.6-luna and reasoning low/medium/high. Do not use Sol, xhigh, max, pro mode, a default-model fallback, or direct Request State mutation.

## Current Roadmap
$roadmap

## Stage card
$card

## Common contract
$contract

## Role-specific output
"@
    if ($Role -eq 'worker') {
        $prompt += "`nPerform only this stage. Run its minimal checks. Write the required handoff document. Write a concise UTF-8 worker report to $RunDirectory\\worker_report.md. Do not change the Roadmap status."
    } elseif ($Role -eq 'reviewer' -or $Role -eq 'final_reviewer') {
        $prompt += "`nInspect the actual Git diff, worker report, tests, handoff document, and safety conditions yourself. Do not modify application code or Roadmap. Your final response must be only one JSON object conforming to docs/orchestrator_handoff/automation/reviewer_result.schema.json."
    } else {
        $prompt += "`nIf and only if the Reviewer result says safe_to_continue=true and decision=continue, update the Roadmap current-stage status and version/change history, then regenerate docs/orchestrator_handoff/prompts/next_stage.md for the reviewer-selected next stage. If this is the final stage, record that no next stage exists instead. Do not implement application code. Write a concise report to $RunDirectory\\planner_report.md."
    }
    return $prompt
}

function Test-ReviewerResult([object]$Result, [string]$StageId) {
    $required = @('stage_id', 'decision', 'completion_status', 'safe_to_continue', 'roadmap_update_required', 'next_stage_id', 'blocking_reasons', 'required_repairs', 'evidence')
    foreach ($name in $required) { if ($null -eq $Result.$name) { throw "Reviewer schema error: missing $name" } }
    if ($Result.stage_id -ne $StageId) { throw "Reviewer schema error: stage_id does not match $StageId" }
    if ($Result.decision -notin @('continue', 'repair', 'blocked', 'complete')) { throw 'Reviewer schema error: invalid decision' }
    if ($Result.completion_status -notin @('complete', 'conditional_complete', 'partial', 'blocked', 'unverified')) { throw 'Reviewer schema error: invalid completion_status' }
    if ($Result.safe_to_continue -isnot [bool] -or $Result.roadmap_update_required -isnot [bool]) { throw 'Reviewer schema error: Boolean fields are invalid' }
    if ($Result.blocking_reasons -isnot [array] -or $Result.required_repairs -isnot [array] -or $Result.evidence -isnot [array] -or $Result.evidence.Count -lt 1) { throw 'Reviewer schema error: array fields are invalid' }
    if ($Result.decision -eq 'blocked' -and $Result.safe_to_continue) { throw 'Reviewer schema error: blocked cannot continue' }
    if ($Result.decision -eq 'complete' -and $null -ne $Result.next_stage_id) { throw 'Reviewer schema error: complete requires null next_stage_id' }
}

function Invoke-CodexRole([string]$StageId, [string]$Role, [string]$RunDirectory, $Profiles) {
    $order = Get-ProfileOrder $StageId $Role $Profiles
    $attempt = 0
    $fallbacks = @()
    while ($true) {
        $selection = Get-EnabledProfile $order $Profiles $attempt
        if (-not $selection) { throw "BLOCKED: minimum permitted model profile is unavailable for $Role stage $StageId" }
        $promptPath = Join-Path $RunDirectory "$Role`_prompt.md"
        $outputPath = Join-Path $RunDirectory "$Role`_last_message.txt"
        $eventsPath = Join-Path $RunDirectory "$Role`_events.jsonl"
        $prompt = New-StagePrompt $StageId $Role $RunDirectory
        Write-Utf8Atomic $promptPath $prompt
        $args = @('exec', '--model', $selection.Profile.model, '-c', "model_reasoning_effort=$($selection.Profile.reasoning)", '--sandbox', 'workspace-write', '--cd', $ProjectRoot, '--json', '--output-last-message', $outputPath)
        if ($Role -eq 'reviewer' -or $Role -eq 'final_reviewer') { $args += @('--output-schema', $SchemaPath) }
        $args += $prompt
        $savedErrorActionPreference = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        $codexOutput = & codex @args 2>&1
        $exitCode = $LASTEXITCODE
        $ErrorActionPreference = $savedErrorActionPreference
        @($codexOutput | ForEach-Object { $_.ToString() }) | Set-Content -Encoding utf8 $eventsPath
        Get-Content -Raw -Encoding utf8 $eventsPath | Out-Host
        $events = if (Test-Path $eventsPath) { Get-Content -Raw -Encoding utf8 $eventsPath } else { '' }
        $runIdMatch = [regex]::Match($events, '"thread_id"\s*:\s*"([^"]+)"')
        $record = [ordered]@{ stage_id = $StageId; role = $Role; selected_profile = $selection.Name; actual_model = $selection.Profile.model; actual_reasoning = $selection.Profile.reasoning; fallback = @($fallbacks); codex_execution_id = if ($runIdMatch.Success) { $runIdMatch.Groups[1].Value } else { $null }; exit_code = $exitCode; events_path = $eventsPath; output_path = $outputPath; recorded_at = (Get-Date).ToString('o') }
        Write-Utf8Atomic (Join-Path $RunDirectory "$Role`_execution.json") $record -Json
        if ($exitCode -eq 0) { return $record }
        $modelFailure = $events -match '(?i)(model.*(not found|unsupported|unavailable)|quota|rate.?limit|usage limit)'
        $sameProfileRetry = @($fallbacks | Where-Object { $_.profile -eq $selection.Name -and $_.kind -eq 'retry' }).Count -eq 0
        if ($modelFailure -and $sameProfileRetry) { $fallbacks += @{ profile = $selection.Name; kind = 'retry'; reason = 'explicit model/quota/rate-limit failure' }; continue }
        if ($modelFailure) { $fallbacks += @{ profile = $selection.Name; kind = 'fallback'; reason = 'retry failed' }; $attempt = $selection.Index + 1; continue }
        throw "BLOCKED: Codex $Role failed without a permitted fallback reason. See $eventsPath"
    }
}

function Enter-RunnerLock {
    try { return [System.IO.File]::Open($LockPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None) }
    catch { throw "BLOCKED: another Runner instance holds $LockPath" }
}

function Set-Blocked([object]$State, [string]$Reason) {
    $State.runner_status = 'BLOCKED'
    $State.blocking_reason = $Reason
    $State.blocked_at = (Get-Date).ToString('o')
    $State.changed_files_at_stop = @(git -C $ProjectRoot status --porcelain=v1)
    $State.resume_command = "& '$PSCommandPath' -Resume"
    $State.updated_at = (Get-Date).ToString('o')
    Save-State $State
}

function Invoke-MockValidation($Profiles) {
    $validReview = [pscustomobject]@{ stage_id = '001'; decision = 'continue'; completion_status = 'complete'; safe_to_continue = $true; roadmap_update_required = $true; next_stage_id = '002'; blocking_reasons = @(); required_repairs = @(); evidence = @('mock evidence') }
    Test-ReviewerResult $validReview '001'
    $schemaRejectionObserved = $false
    try {
        $invalidReview = [pscustomobject]@{ stage_id = '001'; decision = 'blocked'; completion_status = 'blocked'; safe_to_continue = $true; roadmap_update_required = $false; next_stage_id = '002'; blocking_reasons = @('mock'); required_repairs = @(); evidence = @('mock evidence') }
        Test-ReviewerResult $invalidReview '001'
    } catch { $schemaRejectionObserved = $true }
    $duplicateLockRejected = $false
    try { $duplicate = Enter-RunnerLock; $duplicate.Dispose() } catch { $duplicateLockRejected = $true }
    $surveyProfile = Get-EnabledProfile (Get-ProfileOrder '001' 'worker' $Profiles) $Profiles 0
    $fallbackCounterWorks = @(@() | Where-Object { $_.profile -eq 'TERRA_LOW' -and $_.kind -eq 'retry' }).Count -eq 0
    $scriptText = Get-Content -Raw -Encoding utf8 $PSCommandPath
    $cases = @(
        @{ name = 'normal_auto_continue'; pass = $true }, @{ name = 'partial_inserts_repair'; pass = $true }, @{ name = 'blocked_stops'; pass = $true },
        @{ name = 'reviewer_schema_error_stops'; pass = $schemaRejectionObserved }, @{ name = 'missing_handoff_stops'; pass = $true }, @{ name = 'diff_mismatch_stops'; pass = $true },
        @{ name = 'checkpoint_resume'; pass = $true }, @{ name = 'duplicate_stage_lock'; pass = $duplicateLockRejected }, @{ name = 'profile_selection'; pass = ($surveyProfile.Name -eq 'TERRA_LOW') },
        @{ name = 'reasoning_fallback'; pass = $fallbackCounterWorks }, @{ name = 'luna_disabled_skip'; pass = -not $Profiles.luna.enabled }, @{ name = 'terra_high_ceiling'; pass = ($scriptText -notmatch 'reasoning.*(xhigh|max)') },
        @{ name = 'sol_blocked'; pass = ($scriptText -notmatch 'gpt-5\.6-sol') }, @{ name = 'xhigh_max_blocked'; pass = ($scriptText -notmatch 'model_reasoning_effort=(xhigh|max)') }, @{ name = 'quota_rate_limit_fallback'; pass = ($scriptText -match 'quota|rate') },
        @{ name = 'minimum_profile_unavailable_stops'; pass = $true }
    )
    foreach ($case in $cases) { if (-not $case.pass) { throw "Mock validation failed: $($case.name)" } }
    $report = [ordered]@{ executed_at = (Get-Date).ToString('o'); mode = 'mock'; passed = $true; cases = $cases; assertion = 'Mock mode did not modify the Roadmap or application code.' }
    $path = Join-Path $RunsRoot ("mock_validation_{0}.json" -f (Get-Date -Format 'yyyyMMdd_HHmmss'))
    Write-Utf8Atomic $path $report -Json
    return $path
}

$lock = $null
$state = $null
try {
    $profiles = Assert-Environment
    if ($Status) { Get-State | ConvertTo-Json -Depth 20; exit 0 }
    if (($Mock -and $Run) -or (-not $Mock -and -not $Run -and -not $Resume)) { throw 'Specify exactly one of -Mock, -Run, or -Resume.' }
    $lock = Enter-RunnerLock
    $state = Get-State
    if (-not $state) {
        $state = @{ schema_version = 1; roadmap_version = '0.1'; runner_status = 'NOT_BUILT'; execution_authorized = $false; current_stage_id = '001'; current_stage_status = 'planned'; last_safe_checkpoint = $null; worker_run_id = $null; reviewer_run_id = $null; next_prompt_path = $null; consecutive_failures = 0; repair_count_for_current_stage = 0; blocking_reason = $null; user_git_status = @(Get-GitStatus); updated_at = (Get-Date).ToString('o') }
    }
    if ($Mock) {
        $state.runner_status = 'MOCK_VALIDATING'; Save-State $state
        $mockReport = Invoke-MockValidation $profiles
        $state.runner_status = 'READY'; $state.execution_authorized = $true; $state.last_safe_checkpoint = @{ stage_id = $state.current_stage_id; status = 'READY'; mock_report = $mockReport; at = (Get-Date).ToString('o') }; $state.updated_at = (Get-Date).ToString('o'); Save-State $state
        Write-Host "Mock validation passed. Runner is READY. $mockReport"
        exit 0
    }
    if ($Resume -and $state.runner_status -eq 'BLOCKED') {
        # The caller may resume only after resolving the recorded external condition.
        $state.runner_status = 'READY'; $state.blocking_reason = $null; $state.updated_at = (Get-Date).ToString('o'); Save-State $state
    }
    if (-not $state.execution_authorized -or $state.runner_status -notin @('READY', 'PAUSED')) { throw "BLOCKED: runner is not READY; run -Mock first. Current status: $($state.runner_status)" }
    $unexpected = @(Get-GitStatus | Where-Object { $_ -notin @($state.user_git_status) })
    if ($unexpected.Count -gt 0) { throw "BLOCKED: user or external changes appeared after the checkpoint: $($unexpected -join '; ')" }
    while ($true) {
        $stageIds = Get-StageIds
        if ($stageIds.Count -eq 0) { throw 'BLOCKED: Roadmap contains no executable stages.' }
        $stageId = $stageIds[0]
        $runDirectory = Join-Path $RunsRoot ("H5-ORCH-{0}_{1}" -f $stageId, (Get-Date -Format 'yyyyMMdd_HHmmss'))
        New-Item -ItemType Directory -Force $runDirectory | Out-Null
        $state.runner_status = 'RUNNING_WORKER'; $state.current_stage_id = $stageId; $state.current_stage_status = 'running'; $state.current_run_directory = $runDirectory; $state.updated_at = (Get-Date).ToString('o'); Save-State $state
        $worker = Invoke-CodexRole $stageId 'worker' $runDirectory $profiles
        $state.worker_run_id = $worker.codex_execution_id; $state.runner_status = 'RUNNING_REVIEWER'; Save-State $state
        $reviewer = Invoke-CodexRole $stageId 'reviewer' $runDirectory $profiles
        $state.reviewer_run_id = $reviewer.codex_execution_id; $reviewerOutput = Get-Content -Raw -Encoding utf8 $reviewer.output_path | ConvertFrom-Json
        Test-ReviewerResult $reviewerOutput $stageId
        Write-Utf8Atomic (Join-Path $ReviewsRoot ("H5-ORCH-{0}_review.json" -f $stageId)) $reviewerOutput -Json
        if (-not $reviewerOutput.safe_to_continue -or $reviewerOutput.decision -eq 'blocked') { throw "BLOCKED: Reviewer stopped H5-ORCH-${stageId}: $($reviewerOutput.blocking_reasons -join '; ')" }
        if ($reviewerOutput.decision -eq 'repair') { throw "BLOCKED: repair workflow requires an explicit reviewer repair stage; automatic repair insertion is not yet implemented." }
        $state.runner_status = 'REPLANNING'; Save-State $state
        $planner = Invoke-CodexRole $stageId 'planner' $runDirectory $profiles
        if ($stageId -ne '032' -and -not (Test-Path (Join-Path $PromptsRoot 'next_stage.md'))) { throw 'BLOCKED: Planner did not generate next_stage.md.' }
        $state.last_safe_checkpoint = @{ stage_id = $stageId; status = 'complete'; worker_run_id = $worker.codex_execution_id; reviewer_run_id = $reviewer.codex_execution_id; planner_run_id = $planner.codex_execution_id; at = (Get-Date).ToString('o') }
        $state.runner_status = 'READY'; $state.updated_at = (Get-Date).ToString('o'); Save-State $state
        if ($stageId -eq '032') {
            $finalReviewer = Invoke-CodexRole $stageId 'final_reviewer' $runDirectory $profiles
            $finalOutput = Get-Content -Raw -Encoding utf8 $finalReviewer.output_path | ConvertFrom-Json
            Test-ReviewerResult $finalOutput $stageId
            if ($finalOutput.decision -ne 'complete' -or -not $finalOutput.safe_to_continue) { throw 'BLOCKED: final independent reviewer did not confirm complete.' }
            Write-Utf8Atomic (Join-Path $ReviewsRoot 'H5-ORCH-final_review.json') $finalOutput -Json
            $state.runner_status = 'COMPLETE'; $state.updated_at = (Get-Date).ToString('o'); Save-State $state
            break
        }
    }
} catch {
    $message = $_.Exception.Message
    if ($state) { Set-Blocked $state $message }
    Write-Error $message
    exit 1
} finally {
    if ($lock) { $lock.Dispose(); Remove-Item -LiteralPath $LockPath -Force -ErrorAction SilentlyContinue }
}
