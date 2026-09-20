from __future__ import annotations

import json
import subprocess
from pathlib import Path

from copy import deepcopy

from request_ai_agent_h9_v0.condition_fieldsets import default_condition_sets
from request_ai_agent_h9_v0.state import _sanitize_manual_case_matrix_scope, create_initial_state, sanitize_state
from request_ai_agent_h9_v0.validator import validate_state


UI_PATH = Path(__file__).resolve().parents[1] / "ui.py"
HTML_TEMPLATE = UI_PATH.read_text(encoding="utf-8")


def _script_between(start: str, end: str) -> str:
    start_at = HTML_TEMPLATE.index(start)
    return HTML_TEMPLATE[start_at:HTML_TEMPLATE.index(end, start_at)]


def _run_node(script: str) -> dict:
    result = subprocess.run(
        ["node", "-e", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_both_scope_requires_outdoor_matrix_display_before_screen_six_and_keeps_single_scopes_unchanged():
    switch_scope = _script_between("function switchAnalysisScopeTab(kind, scope)", "function requiresOutdoorCaseMatrixView")
    review_helpers = _script_between("function requiresOutdoorCaseMatrixView()", "function renderPreviewCaseMatrixStatus")
    renderer = _script_between("function renderCasePreview()", "function focusCaseValidationIssue")
    confirmation = _script_between("async function confirmCaseConfiguration()", "function renderDerivedPanels()")

    rendered = _run_node(
        f"""
(async () => {{
  const action = {{disabled:false}};
  const nodes = {{caseScopeTabs:{{innerHTML:""}}, caseCommon:{{innerHTML:""}}, caseMatrix:{{innerHTML:""}}, caseCoverageStatus:{{scrollIntoView:() => {{}}}}}};
  const $ = id => id === "caseConfirmNextBtn" ? action : nodes[id];
  const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
  let both = true;
  const hasBothAnalysisScopes = () => both;
  const requestedAnalysisScopes = () => both ? ["indoor", "outdoor"] : [activeCaseScope];
  const scopeTabsHtml = (_kind, scope) => `tab-${{scope}}`;
  const caseImpactNoticeHtml = () => "";
  const caseSourceReferenceHtml = () => "";
  const caseTableHtml = () => `matrix-${{activeCaseScope}}`;
  const caseConfigurationInfoHtml = () => "";
  const renderCaseDuplicateWarning = () => {{}};
  const renderCaseCoverageStatus = () => {{}};
  const document = {{activeElement:null}};
  let activeScreen = "SCREEN-05";
  let activeCaseScope = "indoor";
  let outdoorCaseMatrixViewed = false;
  let preserved = 0;
  const preserveCaseSelections = () => {{ preserved += 1; }};
  {review_helpers}
  {renderer}
  {switch_scope}
  activeCaseScope = "outdoor";
  document.activeElement = {{matches:selector => selector === "select[data-case-field]"}};
  renderCasePreview();
  const skippedRender = outdoorCaseMatrixViewed;
  document.activeElement = null;
  switchAnalysisScopeTab("case", "outdoor");
  const directTab = {{scope:activeCaseScope, viewed:outdoorCaseMatrixViewed, matrix:nodes.caseMatrix.innerHTML, preserved}};

  activeCaseScope = "indoor";
  outdoorCaseMatrixViewed = false;
  let nextScreen = "";
  let switches = 0;
  const refreshPreview = async () => true;
  const resetCaseImpactBaseline = () => {{}};
  const caseConfigurationIssues = () => requestState.review.validator.blocking;
  const focusCaseValidationIssue = () => {{}};
  const navigateScreen = screen => {{ nextScreen = screen; }};
  let requestState = {{review:{{validator:{{blocking:[], coverage:{{complete:true}}}}}}}};
  const originalSwitch = switchAnalysisScopeTab;
  switchAnalysisScopeTab = (kind, scope) => {{ switches += 1; originalSwitch(kind, scope); }};
  {confirmation}
  await confirmCaseConfiguration();
  const firstNext = {{screen:nextScreen, scope:activeCaseScope, viewed:outdoorCaseMatrixViewed, switches}};
  await confirmCaseConfiguration();
  const secondNext = nextScreen;

  both = false;
  outdoorCaseMatrixViewed = false;
  activeCaseScope = "indoor";
  nextScreen = "";
  await confirmCaseConfiguration();
  const indoorOnly = nextScreen;
  activeCaseScope = "outdoor";
  nextScreen = "";
  await confirmCaseConfiguration();
  const outdoorOnly = nextScreen;
  process.stdout.write(JSON.stringify({{skippedRender, directTab, firstNext, secondNext, indoorOnly, outdoorOnly}}));
}})().catch(error => {{ console.error(error); process.exit(1); }});
"""
    )

    assert rendered == {
        "skippedRender": False,
        "directTab": {"scope": "outdoor", "viewed": True, "matrix": "matrix-outdoor", "preserved": 1},
        "firstNext": {"screen": "", "scope": "outdoor", "viewed": True, "switches": 1},
        "secondNext": "SCREEN-06",
        "indoorOnly": "SCREEN-06",
        "outdoorOnly": "SCREEN-06",
    }


def test_case_impact_invalidation_clears_only_the_outdoor_matrix_view_history():
    classifier = _script_between("function classifyCaseImpact(state)", "function caseImpactNoticeHtml")

    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
let outdoorCaseMatrixViewed = true;
let activeCaseScope = "indoor";
let caseImpactSideState = {{status:"", reasons:[]}};
let caseImpactBaseline = {{sources:{{geometry:new Map([["geometry_1", "WINDOW-001"]]), conditions:new Map()}}, rows:[{{geometry_id:"geometry_1", condition_values:{{}}}}]}};
let changed = true;
const caseImpactSources = () => ({{geometry:new Map([["geometry_1", changed ? "WINDOW-002" : "WINDOW-001"]]), conditions:new Map()}});
const hasConditionReference = () => false;
const hasBothAnalysisScopes = () => false;
{classifier}
const impactDetected = classifyCaseImpact({{}});
const invalidated = outdoorCaseMatrixViewed;
outdoorCaseMatrixViewed = true;
changed = false;
const unrelatedChange = classifyCaseImpact({{}});
process.stdout.write(JSON.stringify({{impactDetected, invalidated, unrelatedChange, retained:outdoorCaseMatrixViewed}}));
"""
    )

    assert rendered == {
        "impactDetected": True,
        "invalidated": False,
        "unrelatedChange": False,
        "retained": True,
    }


def test_review_is_completed_only_after_all_affected_scopes_render_and_the_user_leaves_screen_five():
    review_helpers = _script_between("function requiresOutdoorCaseMatrixView()", "function renderPreviewCaseMatrixStatus")
    renderer = _script_between("function renderCasePreview()", "function focusCaseValidationIssue")
    navigation = _script_between("function navigateScreen(screenId, options={})", "function updateGate()")

    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
let activeScreen = "SCREEN-05";
let activeCaseScope = "indoor";
let caseImpactSideState = {{status:CASE_REVIEW_REQUIRED, impactedCaseIds:["indoor_case", "outdoor_case"], renderedScopes:[]}};
let requestState = {{case_matrix:{{rows:[
  {{case_id:"indoor_case", analysis_scope:"indoor"}},
  {{case_id:"outdoor_case", analysis_scope:"outdoor"}}
]}}}};
let resets = 0;
const resetCaseImpactBaseline = () => {{ resets += 1; caseImpactSideState = {{status:"", reasons:[]}}; }};
const hasBothAnalysisScopes = () => true;
const currentCaseScope = () => activeCaseScope;
let outdoorCaseMatrixViewed = false;
const requestedAnalysisScopes = () => ["indoor", "outdoor"];
const scopeTabsHtml = () => "";
const caseImpactNoticeHtml = () => "";
const caseSourceReferenceHtml = () => "";
const caseTableHtml = () => `matrix-${{activeCaseScope}}`;
const caseConfigurationInfoHtml = () => "";
const renderCaseDuplicateWarning = () => {{}};
const renderCaseCoverageStatus = () => {{}};
const caseImpactReviewRequiredForScope = scope => caseImpactSideState.status === CASE_REVIEW_REQUIRED
  && requestState.case_matrix.rows.some(row => row.analysis_scope === scope && caseImpactSideState.impactedCaseIds.includes(row.case_id));
const nodes = {{caseScopeTabs:{{innerHTML:""}}, caseCommon:{{innerHTML:""}}, caseMatrix:{{innerHTML:""}}}};
const $ = id => nodes[id];
const document = {{activeElement:null}};
{review_helpers}
{renderer}
renderCasePreview();
const indoorRendered = [...caseImpactSideState.renderedScopes];
completeCaseImpactReviewOnLeave("SCREEN-04");
const partialLeave = {{resets, status:caseImpactSideState.status}};
activeCaseScope = "outdoor";
renderCasePreview();
completeCaseImpactReviewOnLeave("SCREEN-06");
const completedLeave = {{resets, status:caseImpactSideState.status}};
process.stdout.write(JSON.stringify({{indoorRendered, partialLeave, completedLeave}}));
"""
    )

    assert rendered == {
        "indoorRendered": ["indoor"],
        "partialLeave": {"resets": 0, "status": "CASE_REVIEW_REQUIRED"},
        "completedLeave": {"resets": 1, "status": ""},
    }
    assert "completeCaseImpactReviewOnLeave(screen.id);" in navigation


def test_a_new_review_change_clears_the_previous_render_confirmation():
    classifier = _script_between("function conditionImpactScope(sources, key)", "function caseImpactNoticeHtml")

    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
const hasBothAnalysisScopes = () => false;
let activeCaseScope = "indoor";
let outdoorCaseMatrixViewed = true;
let caseImpactSideState = {{status:"", reasons:[]}};
let currentValue = "1100";
let caseImpactBaseline = {{
  sources:{{
    geometry:new Map(),
    conditions:new Map([["operating_1:fan_1_rpm", "1000"]]),
    conditionScopes:new Map([["operating_1", "indoor"]])
  }},
  rows:[{{case_id:"case_001", analysis_scope:"indoor", condition_values:{{fan:"operating_1"}}}}]
}};
const caseImpactSources = () => ({{
  geometry:new Map(),
  conditions:new Map([["operating_1:fan_1_rpm", currentValue]]),
  conditionScopes:new Map([["operating_1", "indoor"]])
}});
{classifier}
classifyCaseImpact({{}});
const firstKey = caseImpactSideState.reviewKey;
caseImpactSideState = {{...caseImpactSideState, renderedScopes:["indoor"]}};
currentValue = "1200";
classifyCaseImpact({{}});
process.stdout.write(JSON.stringify({{firstKey, secondKey:caseImpactSideState.reviewKey, renderedScopes:caseImpactSideState.renderedScopes}}));
"""
    )

    assert rendered["firstKey"] != rendered["secondKey"]
    assert rendered["renderedScopes"] == []


def test_same_review_reclassification_keeps_rac_both_navigation_and_confirmation_state():
    classifier = _script_between("function conditionImpactScope(sources, key)", "function caseImpactNoticeHtml")

    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
const hasBothAnalysisScopes = () => true;
let activeCaseScope = "outdoor";
let outdoorCaseMatrixViewed = true;
let caseImpactSideState = {{status:"", reasons:[]}};
let indoorRpm = "1000";
let caseImpactBaseline = {{
  sources:{{
    geometry:new Map(),
    conditions:new Map([["indoor_card:fan_1_rpm", "900"], ["outdoor_card:fan_1_rpm", "900"]]),
    conditionScopes:new Map([["indoor_card", "indoor"], ["outdoor_card", "outdoor"]])
  }},
  rows:[
    {{case_id:"indoor_case", analysis_scope:"indoor", condition_values:{{fan:"indoor_card"}}}},
    {{case_id:"outdoor_case", analysis_scope:"outdoor", condition_values:{{fan:"outdoor_card"}}}}
  ]
}};
const caseImpactSources = () => ({{
  geometry:new Map(),
  conditions:new Map([["indoor_card:fan_1_rpm", indoorRpm], ["outdoor_card:fan_1_rpm", "900"]]),
  conditionScopes:new Map([["indoor_card", "indoor"], ["outdoor_card", "outdoor"]])
}});
{classifier}
classifyCaseImpact({{case_matrix:{{rows:caseImpactBaseline.rows}}}});
const first = {{scope:activeCaseScope, outdoorCaseMatrixViewed, reviewKey:caseImpactSideState.reviewKey}};
activeCaseScope = "outdoor";
outdoorCaseMatrixViewed = true;
caseImpactSideState = {{...caseImpactSideState, renderedScopes:["indoor", "outdoor"]}};
classifyCaseImpact({{case_matrix:{{rows:caseImpactBaseline.rows}}}});
const same = {{scope:activeCaseScope, outdoorCaseMatrixViewed, renderedScopes:caseImpactSideState.renderedScopes, reviewKey:caseImpactSideState.reviewKey}};
indoorRpm = "1100";
classifyCaseImpact({{case_matrix:{{rows:caseImpactBaseline.rows}}}});
const changed = {{scope:activeCaseScope, outdoorCaseMatrixViewed, renderedScopes:caseImpactSideState.renderedScopes, reviewKey:caseImpactSideState.reviewKey}};
process.stdout.write(JSON.stringify({{first, same, changed}}));
"""
    )

    assert rendered["first"]["scope"] == "indoor"
    assert rendered["first"]["outdoorCaseMatrixViewed"] is False
    assert rendered["same"] == {
        "scope": "outdoor",
        "outdoorCaseMatrixViewed": True,
        "renderedScopes": ["indoor", "outdoor"],
        "reviewKey": rendered["first"]["reviewKey"],
    }
    assert rendered["changed"]["scope"] == "indoor"
    assert rendered["changed"]["outdoorCaseMatrixViewed"] is False
    assert rendered["changed"]["renderedScopes"] == []
    assert rendered["changed"]["reviewKey"] != rendered["first"]["reviewKey"]


def test_first_visible_case_matrix_render_establishes_the_review_baseline_once():
    reset = _script_between("function resetCaseImpactBaseline(options={})", "function clearCaseConfigurationWarning")
    classifier = _script_between("function conditionImpactScope(sources, key)", "function caseImpactNoticeHtml")
    renderer = _script_between("function renderCasePreview()", "function focusCaseValidationIssue")
    completion = _script_between("function caseImpactReviewScopes()", "function renderPreviewCaseMatrixStatus")

    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
let activeScreen = "SCREEN-01";
let activeCaseScope = "indoor";
let outdoorCaseMatrixViewed = false;
let caseImpactBaseline = null;
let caseImpactSideState = {{status:"", reasons:[]}};
let rpm = "900";
let requestState = {{case_matrix:{{rows:[{{case_id:"case_001", analysis_scope:"indoor", condition_values:{{fan:"operating_1"}}}}]}}}};
const caseImpactSources = () => ({{
  geometry:new Map(),
  conditions:new Map([["operating_1:fan_1_rpm", rpm]]),
  conditionScopes:new Map([["operating_1", "indoor"]])
}});
const clearCaseConfigurationWarning = () => {{}};
const hasBothAnalysisScopes = () => false;
const requestedAnalysisScopes = () => ["indoor"];
const scopeTabsHtml = () => "";
const caseImpactNoticeHtml = () => "";
const caseSourceReferenceHtml = () => "";
const caseTableHtml = () => "matrix";
const caseConfigurationInfoHtml = () => "";
const renderCaseDuplicateWarning = () => {{}};
const renderCaseCoverageStatus = () => {{}};
const recordOutdoorCaseMatrixView = () => {{}};
const caseImpactReviewRequiredForScope = scope => caseImpactSideState.status === CASE_REVIEW_REQUIRED
  && requestState.case_matrix.rows.some(row => row.analysis_scope === scope && caseImpactSideState.impactedCaseIds.includes(row.case_id));
const document = {{activeElement:null}};
const $ = id => ({{caseScopeTabs:{{innerHTML:""}}, caseCommon:{{innerHTML:""}}, caseMatrix:{{innerHTML:""}}}})[id];
{reset}
{classifier}
{renderer}
const caseImpactReviewRequiredForCase = row => caseImpactSideState.status === CASE_REVIEW_REQUIRED
  && caseImpactSideState.impactedCaseIds.includes(row.case_id);
{completion}

renderCasePreview();
const beforeScreenFive = caseImpactBaseline === null;
activeScreen = "SCREEN-05";
renderCasePreview();
const firstBaselineRpm = caseImpactBaseline.sources.conditions.get("operating_1:fan_1_rpm");
const noInitialReview = classifyCaseImpact(requestState);
activeScreen = "SCREEN-04";
rpm = "1000";
const firstReview = classifyCaseImpact(requestState);
activeScreen = "SCREEN-05";
renderCasePreview();
const baselineWasNotOverwritten = caseImpactBaseline.sources.conditions.get("operating_1:fan_1_rpm");
completeCaseImpactReviewOnLeave("SCREEN-04");
const completed = {{status:caseImpactSideState.status, baseline:caseImpactBaseline.sources.conditions.get("operating_1:fan_1_rpm")}};
rpm = "1100";
const secondReview = classifyCaseImpact(requestState);
process.stdout.write(JSON.stringify({{beforeScreenFive, firstBaselineRpm, noInitialReview, firstReview, baselineWasNotOverwritten, completed, secondReview}}));
"""
    )

    assert rendered == {
        "beforeScreenFive": True,
        "firstBaselineRpm": "900",
        "noInitialReview": False,
        "firstReview": True,
        "baselineWasNotOverwritten": "900",
        "completed": {"status": "", "baseline": "1000"},
        "secondReview": True,
    }


def test_screen_four_preview_then_navigation_to_screen_five_establishes_and_preserves_review_baseline():
    reset = _script_between("function resetCaseImpactBaseline(options={})", "function clearCaseConfigurationWarning")
    classifier = _script_between("function conditionImpactScope(sources, key)", "function caseImpactNoticeHtml")
    renderer = _script_between("function renderCasePreview()", "function focusCaseValidationIssue")
    review_completion = _script_between("function caseImpactReviewScopes()", "function renderPreviewCaseMatrixStatus")
    navigation = _script_between("function navigateScreen(screenId, options={})", "function updateGate()")
    condition_navigation = _script_between("async function confirmConditionsBeforeCaseMatrix()", "function revealMissingFanControl")

    rendered = _run_node(
        f"""
(async () => {{
  const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
  const asArray = value => Array.isArray(value) ? value : [];
  const contextText = value => String(value ?? "").trim();
  const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
  const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
  const screenOrder = ["SCREEN-01", "SCREEN-02", "SCREEN-03", "SCREEN-04", "SCREEN-05", "SCREEN-06"].map(id => ({{id, tab:"write", requiresContext:false}}));
  let activeScreen = "SCREEN-04";
  let activeTopTab = "write";
  let activeCaseScope = "indoor";
  let outdoorCaseMatrixViewed = false;
  let caseImpactBaseline = null;
  let caseImpactSideState = {{status:"", reasons:[]}};
  let rpm = "900";
  let previewScreen = "";
  let shownScreen = "";
  let requestState = {{case_matrix:{{rows:[{{case_id:"case_001", analysis_scope:"", condition_values:{{fan:"operating_1"}}}}]}}}};
  const caseImpactSources = () => ({{
    geometry:new Map(),
    conditions:new Map([["operating_1:fan_1_rpm", rpm]]),
    conditionScopes:new Map([["operating_1", ""]])
  }});
  const clearCaseConfigurationWarning = () => {{}};
  const isContextLocked = () => true;
  const firstIncompleteScreenBefore = () => null;
  const missingRequiredControl = () => null;
  const blockingScreenError = () => null;
  const focusRequiredControl = () => {{}};
  const renderScreenNavigation = () => {{ shownScreen = activeScreen; }};
  const focusScreenHeading = () => {{}};
  const hasBothAnalysisScopes = () => false;
  const requestedAnalysisScopes = () => [""];
  const scopeTabsHtml = () => "";
  const caseImpactNoticeHtml = () => "";
  const caseSourceReferenceHtml = () => "";
  const caseTableHtml = () => caseImpactReviewRequiredForCase(requestState.case_matrix.rows[0]) ? "⚠ 확인 필요" : "정상";
  const caseConfigurationInfoHtml = () => "";
  const renderCaseDuplicateWarning = () => {{}};
  const renderCaseCoverageStatus = () => {{}};
  const recordOutdoorCaseMatrixView = () => {{}};
  const document = {{activeElement:null}};
  const nodes = {{caseScopeTabs:{{innerHTML:""}}, caseCommon:{{innerHTML:""}}, caseMatrix:{{innerHTML:""}}}};
  const $ = id => nodes[id];
  const caseImpactReviewRequiredForScope = scope => caseImpactSideState.status === CASE_REVIEW_REQUIRED
    && requestState.case_matrix.rows.some(row => (!scope || row.analysis_scope === scope) && caseImpactSideState.impactedCaseIds.includes(row.case_id));
  const caseImpactReviewRequiredForCase = row => caseImpactSideState.status === CASE_REVIEW_REQUIRED
    && caseImpactSideState.impactedCaseIds.includes(row.case_id);
  const conditionValidationIssues = () => [];
  const focusConditionValidationIssue = () => {{}};
  {reset}
  {classifier}
  {renderer}
  {review_completion}
  const renderDerivedPanels = () => {{ previewScreen = activeScreen; renderCasePreview(); }};
  const refreshPreview = async () => {{ renderDerivedPanels(); }};
  {navigation}
  {condition_navigation}

  await confirmConditionsBeforeCaseMatrix();
  const firstVisit = {{previewScreen, shownScreen, baseline:caseImpactBaseline.sources.conditions.get("operating_1:fan_1_rpm"), status:caseImpactSideState.status}};
  navigateScreen("SCREEN-04");
  rpm = "1000";
  const firstReview = classifyCaseImpact(requestState);
  await refreshPreview();
  navigateScreen("SCREEN-05");
  const reviewedVisit = {{baseline:caseImpactBaseline.sources.conditions.get("operating_1:fan_1_rpm"), matrix:nodes.caseMatrix.innerHTML, renderedScopes:caseImpactSideState.renderedScopes}};
  navigateScreen("SCREEN-04");
  const completed = {{status:caseImpactSideState.status, baseline:caseImpactBaseline.sources.conditions.get("operating_1:fan_1_rpm")}};
  rpm = "1100";
  const secondReview = classifyCaseImpact(requestState);
  process.stdout.write(JSON.stringify({{firstVisit, firstReview, reviewedVisit, completed, secondReview}}));
}})().catch(error => {{ console.error(error); process.exit(1); }});
"""
    )

    assert rendered == {
        "firstVisit": {"previewScreen": "SCREEN-04", "shownScreen": "SCREEN-05", "baseline": "900", "status": ""},
        "firstReview": True,
        "reviewedVisit": {"baseline": "900", "matrix": "⚠ 확인 필요", "renderedScopes": [""]},
        "completed": {"status": "", "baseline": "1000"},
        "secondReview": True,
    }


def test_existing_case_validation_runs_before_the_outdoor_view_guard():
    confirmation = _script_between("async function confirmCaseConfiguration()", "function renderDerivedPanels()")

    assert confirmation.index("if (blockingIssues.length || coverageBlocked)") < confirmation.index(
        "if (requiresOutdoorCaseMatrixView() && !outdoorCaseMatrixViewed)"
    )


def test_case_validation_and_coverage_move_to_the_scope_that_contains_the_error():
    switch_scope = _script_between("function switchAnalysisScopeTab(kind, scope)", "function requiresOutdoorCaseMatrixView")
    focus_helpers = _script_between("function focusCaseValidationIssue(issue)", "async function confirmCaseConfiguration()")
    confirmation = _script_between("async function confirmCaseConfiguration()", "function renderDerivedPanels()")

    rendered = _run_node(
        f"""
(async () => {{
  const action = {{disabled:false}};
  const scrolls = [];
  const classes = [];
  const field = {{classList:{{add:value => classes.push(value)}}, focus:() => scrolls.push("field-focus"), scrollIntoView:() => scrolls.push("field-scroll")}};
  const row = {{scrollIntoView:() => scrolls.push("row-scroll")}};
  const coverage = {{scrollIntoView:() => scrolls.push("coverage-scroll")}};
  const duplicate = {{scrollIntoView:() => scrolls.push("configuration-scroll")}};
  const nodes = {{caseConfirmNextBtn:action, caseCoverageStatus:coverage, caseDuplicateWarning:duplicate, "section-case":{{scrollIntoView:() => scrolls.push("section-scroll")}}}};
  const $ = id => nodes[id];
  const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
  const asArray = value => Array.isArray(value) ? value : [];
  const contextText = value => String(value ?? "").trim();
  const CSS = {{escape:value => value}};
  const document = {{querySelector:selector => selector.startsWith("select[") ? field : selector.startsWith("tr[") ? row : null}};
  let activeCaseScope = "indoor";
  const hasBothAnalysisScopes = () => true;
  const preserveCaseSelections = () => {{}};
  const renderCasePreview = () => {{}};
  {switch_scope}
  {focus_helpers}
  const refreshPreview = async () => true;
  const resetCaseImpactBaseline = () => {{}};
  const navigateScreen = () => {{ throw new Error("must remain on SCREEN-05"); }};
  let requestState = {{
    case_matrix:{{rows:[{{case_id:"indoor_1"}}, {{case_id:"outdoor_1"}}]}},
    review:{{validator:{{
      blocking:[{{analysis_scope:"outdoor", path:"case_matrix.rows[1].condition_values.fan", field_key:"fan"}}],
      coverage:{{complete:true, by_scope:{{indoor:{{complete:true}}, outdoor:{{complete:true}}}}}}
    }}}}
  }};
  const caseValidatorState = () => requestState.review.validator;
  const caseConfigurationIssues = () => requestState.review.validator.blocking;
  {confirmation}
  await confirmCaseConfiguration();
  const fieldIssue = {{scope:activeCaseScope, classes:[...classes], scrolls:[...scrolls]}};
  activeCaseScope = "outdoor";
  scrolls.length = 0;
  requestState.review.validator = {{
    blocking:[{{analysis_scope:"indoor", path:"case_matrix.rows[0].condition_values.fan", field_key:"fan"}}],
    coverage:{{complete:true, by_scope:{{indoor:{{complete:true}}, outdoor:{{complete:true}}}}}}
  }};
  await confirmCaseConfiguration();
  const reverseFieldIssue = {{scope:activeCaseScope, scrolls:[...scrolls]}};
  activeCaseScope = "indoor";
  scrolls.length = 0;
  requestState.review.validator = {{blocking:[], coverage:{{complete:false, by_scope:{{indoor:{{complete:true}}, outdoor:{{complete:false}}}}}}}};
  await confirmCaseConfiguration();
  const coverageIssue = {{scope:activeCaseScope, scrolls:[...scrolls]}};
  activeCaseScope = "outdoor";
  scrolls.length = 0;
  requestState.review.validator = {{blocking:[], coverage:{{complete:false, by_scope:{{indoor:{{complete:false}}, outdoor:{{complete:true}}}}}}}};
  await confirmCaseConfiguration();
  const reverseCoverageIssue = {{scope:activeCaseScope, scrolls:[...scrolls]}};
  activeCaseScope = "outdoor";
  scrolls.length = 0;
  focusCaseValidationIssue({{analysis_scope:"indoor", path:"case_matrix.rows[0]"}});
  const rowIssue = {{scope:activeCaseScope, scrolls:[...scrolls]}};
  process.stdout.write(JSON.stringify({{fieldIssue, reverseFieldIssue, coverageIssue, reverseCoverageIssue, rowIssue}}));
}})().catch(error => {{ console.error(error); process.exit(1); }});
"""
    )

    assert rendered == {
        "fieldIssue": {
            "scope": "outdoor",
            "classes": ["required-field-highlight"],
            "scrolls": ["field-scroll", "field-focus"],
        },
        "reverseFieldIssue": {"scope": "indoor", "scrolls": ["field-scroll", "field-focus"]},
        "coverageIssue": {"scope": "outdoor", "scrolls": ["coverage-scroll"]},
        "reverseCoverageIssue": {"scope": "indoor", "scrolls": ["coverage-scroll"]},
        "rowIssue": {"scope": "indoor", "scrolls": ["row-scroll"]},
    }


def test_case_impact_prefers_the_changed_condition_scope_and_defaults_common_changes_to_indoor():
    classifier = _script_between("function conditionImpactScope(sources, key)", "function caseImpactNoticeHtml")

    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
const hasBothAnalysisScopes = () => true;
let activeCaseScope = "outdoor";
let outdoorCaseMatrixViewed = true;
let caseImpactSideState = {{status:"", reasons:[]}};
const baselineSources = () => ({{
  geometry:new Map([["geometry_1", "WINDOW-001"]]),
  conditions:new Map([["indoor_card:fan_rpm", "1000"], ["outdoor_card:fan_rpm", "1000"]]),
  conditionScopes:new Map([["indoor_card", "indoor"], ["outdoor_card", "outdoor"]])
}});
const scopedRows = [
  {{case_id:"indoor_case", geometry_id:"geometry_1", condition_values:{{fan:"indoor_card"}}}},
  {{case_id:"outdoor_case", geometry_id:"geometry_1", condition_values:{{fan:"outdoor_card"}}}}
];
let caseImpactBaseline = {{sources:baselineSources(), rows:scopedRows}};
let changed = "indoor";
const caseImpactSources = () => ({{
  geometry:new Map([["geometry_1", changed === "common" ? "WINDOW-002" : "WINDOW-001"]]),
  conditions:new Map([
    ["indoor_card:fan_rpm", changed === "indoor" ? "1100" : "1000"],
    ["outdoor_card:fan_rpm", changed === "outdoor" ? "1100" : "1000"]
  ]),
  conditionScopes:new Map([["indoor_card", "indoor"], ["outdoor_card", "outdoor"]])
}});
const hasConditionReference = () => false;
{classifier}
classifyCaseImpact({{}});
const indoor = activeCaseScope;
caseImpactBaseline = {{sources:baselineSources(), rows:scopedRows}};
activeCaseScope = "indoor";
changed = "outdoor";
classifyCaseImpact({{}});
const outdoor = activeCaseScope;
caseImpactBaseline = {{sources:baselineSources(), rows:scopedRows}};
activeCaseScope = "outdoor";
changed = "common";
classifyCaseImpact({{}});
process.stdout.write(JSON.stringify({{indoor, outdoor, common:activeCaseScope, viewed:outdoorCaseMatrixViewed}}));
"""
    )

    assert rendered == {"indoor": "indoor", "outdoor": "outdoor", "common": "indoor", "viewed": False}


def test_review_marks_only_the_cases_that_reference_the_changed_source():
    classifier = _script_between("function conditionImpactScope(sources, key)", "function caseImpactNoticeHtml")

    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
const hasBothAnalysisScopes = () => false;
let activeCaseScope = "indoor";
let outdoorCaseMatrixViewed = true;
let caseImpactSideState = {{status:"", reasons:[]}};
let caseImpactBaseline = {{
  sources:{{
    geometry:new Map([["geometry_1", "WINDOW-001"]]),
    conditions:new Map([["indoor_card:fan_rpm", "1000"], ["outdoor_card:fan_rpm", "1000"]]),
    conditionScopes:new Map([["indoor_card", "indoor"], ["outdoor_card", "outdoor"]])
  }},
  rows:[
    {{case_id:"indoor_case", geometry_id:"geometry_1", condition_values:{{fan:"indoor_card"}}}},
    {{case_id:"outdoor_case", geometry_id:"geometry_1", condition_values:{{fan:"outdoor_card"}}}}
  ]
}};
const caseImpactSources = () => ({{
  geometry:new Map([["geometry_1", "WINDOW-001"]]),
  conditions:new Map([["indoor_card:fan_rpm", "1100"], ["outdoor_card:fan_rpm", "1000"]]),
  conditionScopes:new Map([["indoor_card", "indoor"], ["outdoor_card", "outdoor"]])
}});
{classifier}
classifyCaseImpact({{}});
process.stdout.write(JSON.stringify(caseImpactSideState));
"""
    )

    assert rendered["status"] == "CASE_REVIEW_REQUIRED"
    assert rendered["impactedCaseIds"] == ["indoor_case"]
    assert rendered["invalidSelections"] == []


def test_new_or_unreferenced_sources_do_not_create_a_review():
    classifier = _script_between("function conditionImpactScope(sources, key)", "function caseImpactNoticeHtml")

    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
const hasBothAnalysisScopes = () => false;
let activeCaseScope = "indoor";
let outdoorCaseMatrixViewed = true;
let caseImpactSideState = {{status:"", reasons:[]}};
let caseImpactBaseline = {{
  sources:{{
    geometry:new Map([["geometry_1", "WINDOW-001"]]),
    conditions:new Map([["operating_1:fan_1_rpm", "900"]]),
    conditionScopes:new Map([["operating_1", ""]])
  }},
  rows:[{{case_id:"case_001", geometry_id:"geometry_2", condition_values:{{fan:"operating_2"}}}}]
}};
const caseImpactSources = () => ({{
  geometry:new Map([["geometry_1", "WINDOW-002"], ["geometry_2", "WINDOW-003"]]),
  conditions:new Map([["operating_1:fan_1_rpm", "1000"], ["operating_2:fan_1_rpm", "1100"]]),
  conditionScopes:new Map([["operating_1", ""], ["operating_2", ""]])
}});
{classifier}
classifyCaseImpact({{case_matrix:{{rows:caseImpactBaseline.rows}}}});
process.stdout.write(JSON.stringify(caseImpactSideState));
"""
    )

    assert rendered == {"status": "", "reasons": []}


def test_case_impact_uses_the_current_case_selection_and_a_preserved_rebuild_selection():
    classifier = _script_between("function conditionImpactScope(sources, key)", "function caseImpactNoticeHtml")

    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
const hasBothAnalysisScopes = () => false;
let activeCaseScope = "indoor";
let outdoorCaseMatrixViewed = true;
let caseImpactSideState = {{status:"", reasons:[]}};
let present = true;
const sources = () => ({{
  geometry:new Map(),
  conditions:present ? new Map([["operating_2:fan_1_rpm", "1100"]]) : new Map(),
  conditionScopes:new Map([["operating_2", ""]])
}});
let caseImpactBaseline = {{
  sources:{{
    geometry:new Map(),
    conditions:new Map([["operating_2:fan_1_rpm", "1000"]]),
    conditionScopes:new Map([["operating_2", ""]])
  }},
  rows:[{{case_id:"case_001", condition_values:{{fan:"operating_1"}}}}]
}};
const caseImpactSources = () => sources();
{classifier}
classifyCaseImpact({{case_matrix:{{rows:[{{case_id:"case_001", condition_values:{{fan:"operating_2"}}, visible_cells:{{fan:"운전 2"}}}}]}}}});
const review = caseImpactSideState;
present = false;
classifyCaseImpact({{case_matrix:{{rows:[{{case_id:"case_001", condition_values:{{}}, invalid_selection_values:{{fan:{{value:"operating_2", label:"운전 2"}}}}}}]}}}});
const rebuild = caseImpactSideState;
process.stdout.write(JSON.stringify({{review, rebuild}}));
"""
    )

    assert rendered["review"]["status"] == "CASE_REVIEW_REQUIRED"
    assert rendered["review"]["impactedCaseIds"] == ["case_001"]
    assert rendered["rebuild"]["status"] == "CASE_REBUILD_REQUIRED"
    assert rendered["rebuild"]["impactedCaseIds"] == ["case_001"]
    assert rendered["rebuild"]["invalidSelections"] == [
        {"caseId": "case_001", "key": "fan", "value": "operating_2", "label": "운전 2"}
    ]


def test_rebuild_keeps_deleted_auto_geometry_as_a_required_blank_selection():
    matrix = _sanitize_manual_case_matrix_scope(
        {
            "rows": [
                {
                    "case_id": "case_001",
                    "geometry_id": "geometry_deleted",
                    "auto_geometry_id": "geometry_deleted",
                    "condition_values": {},
                }
            ],
            "geometry_snapshot_ids": ["geometry_deleted"],
        },
        products=[{"geometry_id": "geometry_current", "drawing_no": "WINDOW-001"}],
        condition_sets=[],
        request_context={"analysis_type": "풍량"},
    )

    assert matrix["rows"] == [
        {
            "case_id": "case_001",
            "geometry_id": "",
            "auto_geometry_id": "",
            "condition_values": {},
            "invalid_selection_values": {"geometry_id": {"value": "geometry_deleted"}},
            "visible_cells": {"case_no": "1", "geometry_id": "", "fan": "", "heat_exchanger": ""},
        }
    ]


def test_rebuild_placeholder_retains_the_previous_value_and_existing_required_validation_blocks_next_step():
    select_renderer = _script_between("function caseSelectFieldHtml(rowId, key, selected, options, sources)", "function caseReadonlyFieldHtml")
    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const esc = value => String(value ?? "");
const caseImpactPreviousSelection = () => "운전 2";
const caseSelectionPresentation = (_key, value, label) => ({{label:label || value, summary:""}});
{select_renderer}
process.stdout.write(JSON.stringify({{html:caseSelectFieldHtml("case_002", "fan", "", [{{value:"operating_1", label:"운전 1"}}], {{}})}}));
"""
    )

    assert '<option value="" disabled hidden selected>[선택 필요]</option>' in rendered["html"]
    assert "기존 값: 운전 2" in rendered["html"]
    assert 'option value="operating_1" selected' not in rendered["html"]

    state = create_initial_state()
    state["request_context"].update({"analysis_type": "풍량", "context_locked": True})
    state["geometry"]["base_product"]["drawing_no"] = "WINDOW-001"
    cards = default_condition_sets(state["request_context"])
    for card in cards:
        if card["type"] == "operating":
            card["fans"][0]["values"]["fan_rpm"] = "900"
        elif card["type"] == "heat_exchanger":
            for key, field in card["fields"].items():
                if key != "name":
                    field["value"] = "1"
    state["conditions"]["condition_sets"] = cards
    configured = sanitize_state(state)
    extra_operating = deepcopy(next(card for card in configured["conditions"]["condition_sets"] if card["type"] == "operating"))
    extra_operating.update({"id": "operating_2", "is_default": False})
    extra_operating["fans"][0]["values"]["fan_rpm"] = "1100"
    configured["conditions"]["condition_sets"].append(extra_operating)
    configured = sanitize_state(configured)
    configured["case_matrix"]["rows"][0]["condition_values"]["fan"] = "operating_2"
    configured["case_matrix"]["rows"][0]["visible_cells"]["fan"] = "운전 2"
    configured["conditions"]["condition_sets"] = [
        card for card in configured["conditions"]["condition_sets"] if card["id"] != "operating_2"
    ]
    rebuilt = sanitize_state(configured)

    assert "fan" not in rebuilt["case_matrix"]["rows"][0]["condition_values"]
    assert rebuilt["case_matrix"]["rows"][0]["invalid_selection_values"]["fan"] == {
        "value": "operating_2",
        "label": "운전 2",
    }
    assert any(issue["code"] == "case_matrix.fan.missing" for issue in validate_state(rebuilt)["blocking"])

    rebuilt["case_matrix"]["rows"][0]["condition_values"]["fan"] = "operating_1"
    repaired = sanitize_state(rebuilt)
    assert repaired["case_matrix"]["rows"][0]["condition_values"]["fan"] == "operating_1"
    assert "fan" not in repaired["case_matrix"]["rows"][0].get("invalid_selection_values", {})
    assert not any(issue["code"] == "case_matrix.fan.missing" for issue in validate_state(repaired)["blocking"])


def test_rebuilds_when_a_referenced_operating_source_loses_its_required_rpm():
    state = create_initial_state()
    state["request_context"].update({"analysis_type": "일반 유동 해석", "context_locked": True})
    state["geometry"]["base_product"]["drawing_no"] = "WINDOW-001"
    cards = default_condition_sets(state["request_context"])
    for card in cards:
        if card["type"] == "operating":
            card["fans"][0]["values"]["fan_rpm"] = "900"
        elif card["type"] == "heat_exchanger":
            for key, field in card["fields"].items():
                if key != "name":
                    field["value"] = "1"
    state["conditions"]["condition_sets"] = cards
    configured = sanitize_state(state)
    assert configured["case_matrix"]["dropdown_options"]["fan"] == [
        {"value": "operating_1", "label": "운전 1"}
    ]

    operating = next(card for card in configured["conditions"]["condition_sets"] if card["id"] == "operating_1")
    operating["fans"][0]["values"]["fan_rpm"] = ""
    rebuilt = sanitize_state(configured)

    assert rebuilt["case_matrix"]["dropdown_options"]["fan"] == []
    assert rebuilt["case_matrix"]["rows"][0]["condition_values"].get("fan") is None
    assert rebuilt["case_matrix"]["rows"][0]["invalid_selection_values"]["fan"] == {
        "value": "operating_1",
        "label": "운전 1",
    }
    assert any(issue["code"] == "case_matrix.fan.missing" for issue in validate_state(rebuilt)["blocking"])


def test_rebuild_previous_value_uses_only_the_saved_user_facing_label():
    previous_selection = _script_between("function caseImpactPreviousSelection(rowId, key, selected)", "function caseConfigurationInfoHtml")
    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const CASE_REBUILD_REQUIRED = "CASE_REBUILD_REQUIRED";
let caseImpactSideState = {{status:"", invalidSelections:[]}};
let requestState = {{case_matrix:{{rows:[
  {{case_id:"labelled", invalid_selection_values:{{fan:{{value:"operating_2", label:"운전 2"}}}}}},
  {{case_id:"legacy", invalid_selection_values:{{fan:{{value:"operating_2"}}}}}}
]}}}};
{previous_selection}
caseImpactSideState = {{
  status:CASE_REBUILD_REQUIRED,
  invalidSelections:[{{caseId:"labelled", key:"fan", value:"operating_2", label:""}}]
}};
process.stdout.write(JSON.stringify({{
  labelled:caseImpactPreviousSelection("labelled", "fan", ""),
  legacy:caseImpactPreviousSelection("legacy", "fan", ""),
  selected:caseImpactPreviousSelection("labelled", "fan", "operating_1"),
  emptyClientLabelFallsBack:caseImpactPreviousSelection("labelled", "fan", "")
}}));
"""
    )

    assert rendered == {"labelled": "운전 2", "legacy": "", "selected": "", "emptyClientLabelFallsBack": "운전 2"}


def test_case_row_collection_preserves_the_selected_option_label_before_a_rebuild():
    collector = _script_between("function collectCaseRows()", "function preserveCaseSelections")
    rendered = _run_node(
        f"""
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const CSS = {{escape:value => value}};
const selected = {{dataset:{{caseField:"fan"}}, value:"operating_2", selectedOptions:[{{textContent:"운전 2"}}]}};
const document = {{
  querySelector:() => null,
  querySelectorAll:() => [selected],
}};
let requestState = {{case_matrix:{{rows:[{{
  case_id:"case_002",
  geometry_id:"geometry_1",
  condition_values:{{fan:"operating_1"}},
  visible_cells:{{fan:"운전 1"}}
}}]}}}};
{collector}
process.stdout.write(JSON.stringify(collectCaseRows()[0]));
"""
    )

    assert rendered["condition_values"]["fan"] == "operating_2"
    assert rendered["visible_cells"]["fan"] == "운전 2"


def test_review_uses_existing_warning_status_without_blocking_or_repeating_when_an_error_exists():
    validation = _script_between("function caseTableValidationPresentation()", "function renderCaseValidationStatus()")
    renderer = _script_between("function caseValidatorState(state=requestState)", "function renderCaseCoverageStatus()")
    confirmation = _script_between("async function confirmCaseConfiguration()", "function renderDerivedPanels()")
    rendered = _run_node(
        f"""
const target = {{innerHTML:"", className:""}};
const $ = id => id === "caseDuplicateWarning" ? target : null;
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
const esc = value => String(value ?? "");
const CASE_REVIEW_REQUIRED = "CASE_REVIEW_REQUIRED";
let activeCaseScope = "indoor";
let caseValidationPending = false;
let caseImpactSideState = {{status:CASE_REVIEW_REQUIRED, impactedCaseIds:["affected"]}};
let requestState = {{
  request_context:{{}},
  case_matrix:{{visible_columns:[], rows:[{{case_id:"affected"}}, {{case_id:"unchanged"}}]}},
  review:{{validator:{{blocking:[], coverage:{{complete:true}}}}}}
}};
{validation}
{renderer}
const reviewStatus = caseTableValidationPresentation();
renderCaseDuplicateWarning();
const reviewMessage = target.innerHTML;
requestState.review.validator.blocking = [{{code:"case_matrix.duplicate", case_no:2, duplicate_of_case_no:1}}];
const errorStatus = caseTableValidationPresentation();
renderCaseDuplicateWarning();
const errorMessage = target.innerHTML;
process.stdout.write(JSON.stringify({{reviewStatus, reviewMessage, errorStatus, errorMessage}}));
"""
    )

    assert rendered["reviewStatus"] == {"text": "⚠ 확인 필요", "tone": "warning"}
    assert "입력값 변경으로 영향을 받은 Case가 있습니다." in rendered["reviewMessage"]
    assert rendered["errorStatus"]["tone"] == "error"
    assert "확인 필요" not in rendered["errorMessage"]
    assert "const reviewPending" in confirmation
    assert "!reviewPending" in confirmation


def test_case_next_keeps_review_state_until_the_screen_five_leave_handler_completes_it():
    confirmation = _script_between("async function confirmCaseConfiguration()", "function renderDerivedPanels()")
    rendered = _run_node(
        f"""
(async () => {{
  const action = {{disabled:false}};
  const $ = id => id === "caseConfirmNextBtn" ? action : null;
  const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
  const contextText = value => String(value ?? "").trim();
  let caseImpactSideState = {{status:"CASE_REVIEW_REQUIRED", impactedCaseIds:["case_001"]}};
  let resets = 0;
  let nextScreen = "";
  const refreshPreview = async () => true;
  const unresolvedCaseImpactSelections = () => [];
  const resetCaseImpactBaseline = () => {{ resets += 1; caseImpactSideState = {{status:""}}; }};
  const renderCasePreview = () => {{}};
  const caseConfigurationIssues = () => [];
  const requiresOutdoorCaseMatrixView = () => false;
  const navigateScreen = screen => {{ nextScreen = screen; }};
  let requestState = {{review:{{validator:{{coverage:{{complete:true}}}}}}}};
  {confirmation}
  await confirmCaseConfiguration();
  process.stdout.write(JSON.stringify({{resets, status:caseImpactSideState.status, nextScreen}}));
}})().catch(error => {{ console.error(error); process.exit(1); }});
"""
    )

    assert rendered == {"resets": 0, "status": "CASE_REVIEW_REQUIRED", "nextScreen": "SCREEN-06"}
