import json
import subprocess
from pathlib import Path


UI_PATH = Path(__file__).resolve().parents[1] / "ui.py"


def test_t204_case_impact_hook_is_client_side_and_preserves_case_rows():
    ui = UI_PATH.read_text(encoding="utf-8")

    assert 'const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";' in ui
    assert 'const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";' in ui
    assert "function classifyCaseImpact(state)" in ui
    assert "function resetCaseImpactBaseline(options={})" in ui
    assert "data-case-impact-status" not in ui
    schedule_start = ui.index("function schedulePreviewRefresh()")
    schedule_end = ui.index("async function refreshPreview", schedule_start)
    schedule = ui[schedule_start:schedule_end]

    assert "classifyCaseImpact(" not in schedule
    assert "adoptStateFromResponse(data);\n        classifyCaseImpact(requestState);" in ui
    assert "previewRefreshTimer = window.setTimeout(() => {" in ui
    assert "refreshPreview(scheduledRevision);" in ui
    assert "Case 행은 자동으로 변경하지 않았습니다." not in ui
    assert "새 소스가 추가되었거나 비참조 소스가 변경되었습니다. Case 행을 검토해 주세요." not in ui
    assert 'function caseImpactPreviousSelection(rowId, key, selected)' in ui


def test_case_impact_commits_only_after_canonical_preview_normalization():
    ui = UI_PATH.read_text(encoding="utf-8")
    source_start = ui.index("function sourceFieldValue(value)")
    source_end = ui.index("function resetCaseImpactBaseline(options={})", source_start)
    source_functions = ui[source_start:source_end]
    impact_start = ui.index("function hasConditionReference(rows, value)")
    impact_end = ui.index("function caseImpactNoticeHtml()", impact_start)
    impact_functions = ui[impact_start:impact_end]
    preview_start = ui.index("function invalidatePendingPreviewRefresh()")
    preview_end = ui.index("const CASE_REVIEW_REQUIRED", preview_start)
    preview_functions = ui[preview_start:preview_end]

    script = f'''
(async () => {{
  const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
  const asArray = value => Array.isArray(value) ? value : [];
  const contextText = value => String(value ?? "").trim();
  const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
  const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
  let previewStateRevision = 0;
  let previewRefreshTimer = null;
  let activeCaseScope = "indoor";
  let outdoorCaseMatrixViewed = true;
  let caseValidationPending = false;
  let caseImpactSideState = {{status:"", reasons:[]}};
  const caseImpactBaseline = {{
    sources:{{geometry:new Map([["geometry_1", "WINDOW-001"]]), conditions:new Map(), conditionScopes:new Map()}},
    rows:[{{case_id:"case_001", geometry_id:"geometry_1", condition_values:{{}}}}],
  }};
  let requestState = {{
    geometry:{{base_product:{{geometry_id:"geometry_1", drawing_no:{{value:"WINDOW-001"}}}}, comparison_products:[]}},
    conditions:{{condition_sets:[]}},
    case_matrix:{{
      visible_columns:[],
      dropdown_options:{{geometry_id:[{{value:"geometry_1"}}]}},
      rows:[{{case_id:"case_001", geometry_id:"geometry_1", condition_values:{{}}}}],
    }},
  }};
  const window = {{
    clearTimeout:() => {{}},
    setTimeout:(callback) => {{ previewRefreshTimer = callback; return 1; }},
  }};
  const clearCaseConfigurationWarning = () => {{}};
  const renderScreenNavigation = () => {{}};
  const orchestratorPanelState = {{dirty:false}};
  const collectState = () => requestState;
  const hasBothAnalysisScopes = () => false;
  const postState = async () => ({{state:{{
    geometry:{{base_product:{{geometry_id:"geometry_1", drawing_no:{{value:"WINDOW-001"}}}}, comparison_products:[]}},
    conditions:{{condition_sets:[]}},
    case_matrix:{{
      visible_columns:[],
      dropdown_options:{{geometry_id:[]}},
      rows:[{{
        case_id:"case_001", geometry_id:"", condition_values:{{}},
        invalid_selection_values:{{geometry_id:{{value:"geometry_1", label:"Base"}}}},
      }}],
    }},
  }}}});
  const conditionCardIdentity = () => "";
  const adoptStateFromResponse = data => {{ requestState = data.state; }};
  const renderConditionFields = () => {{}};
  const renderDerivedPanels = () => {{}};
  const renderCaseValidationStatus = () => {{}};
  {source_functions}
  {impact_functions}
  {preview_functions}

  schedulePreviewRefresh();
  const draft = {{status:caseImpactSideState.status, viewed:outdoorCaseMatrixViewed}};
  await refreshPreview();
  process.stdout.write(JSON.stringify({{draft, canonical:{{
    status:caseImpactSideState.status,
    invalid:caseImpactSideState.invalidSelections,
    viewed:outdoorCaseMatrixViewed,
  }}}}));
}})().catch(error => {{ console.error(error); process.exit(1); }});
'''
    result = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {
        "draft": {"status": "", "viewed": True},
        "canonical": {
            "status": "CASE_REBUILD_REQUIRED",
            "invalid": [{"caseId": "case_001", "key": "geometry_id", "value": "geometry_1", "label": "Base"}],
            "viewed": False,
        },
    }


def test_t204_classifies_only_referenced_existing_source_changes():
    ui = UI_PATH.read_text(encoding="utf-8")

    assert 'reviewReasons.push(`geometry:${id}:added`)' not in ui
    assert 'reviewReasons.push(`condition:${key}:added`)' not in ui
    assert 'rebuildReasons.push(`geometry:${id}:required_value_invalid`)' in ui
    assert 'rebuildReasons.push(`condition:${key}:required_value_invalid`)' in ui
    assert 'status:CASE_REBUILD_REQUIRED' in ui
    assert 'status:CASE_REVIEW_REQUIRED' in ui


def test_case_configuration_confirmation_revalidates_before_entering_preview():
    ui = UI_PATH.read_text(encoding="utf-8")

    assert '이전: 요청 내용' in ui
    assert '다음: 해석 조건' in ui
    assert '이전: 해석 제품' in ui
    assert '다음: Case Matrix' in ui
    assert 'id="caseConfirmNextBtn"' in ui
    assert 'function confirmCaseConfiguration()' in ui
    assert 'await refreshPreview();' in ui
    assert 'resetCaseImpactBaseline();' in ui
    assert 'const blockingIssues = caseConfigurationIssues();' in ui
    assert 'focusCaseValidationIssue(blockingIssues[0]);' in ui
    assert 'navigateScreen("SCREEN-06");' in ui
    assert 'function caseConfigurationMessageHtml(issues, state=requestState, includeReviewAction=false)' in ui
    assert '오류 · Case 구성을 확인해 주세요.' in ui
    assert 'case_matrix.duplicate' in ui


def test_case_matrix_dropdown_changes_refresh_validator_feedback_without_rebuilding_active_select():
    ui = UI_PATH.read_text(encoding="utf-8")
    preserve_start = ui.index("function preserveCaseSelections(changedSelect=null)")
    preserve_end = ui.index("function collectState()", preserve_start)
    preserve = ui[preserve_start:preserve_end]

    assert '!event.target.matches("select[data-case-field]")' in ui
    assert 'if (event.target.matches("select[data-case-field]")) preserveCaseSelections(event.target);' in ui
    assert 'const activeCaseSelect = document.activeElement?.matches?.("select[data-case-field]");' in ui
    assert 'if (!activeCaseSelect) $("caseMatrix").innerHTML' in ui
    assert 'lastCaseDeleteNoticeVisible = false;' in preserve
    assert 'schedulePreviewRefresh();' in preserve
    assert 'else if (event.target.matches("select[data-case-field]")) refreshPreview();' not in ui
