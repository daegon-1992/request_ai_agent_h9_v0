from __future__ import annotations

import subprocess

import request_ai_agent_h9_v0.state as state_module

from request_ai_agent_h9_v0.agent_write_contract import build_agent_write_contract
from request_ai_agent_h9_v0.app import create_app
from request_ai_agent_h9_v0.pms_project_master import load_pms_project_master, search_pms_projects
from request_ai_agent_h9_v0.state import apply_pms_project_selection, create_initial_state, field_value, sanitize_state
from request_ai_agent_h9_v0.ui import HTML_TEMPLATE
from request_ai_agent_h9_v0.validator import validate_state


DEVELOPMENT_PROJECT = "\uac1c\ubc1c \ud504\ub85c\uc81d\ud2b8"
QUALITY_IMPROVEMENT = "\ud488\uc9c8 \uac1c\uc120"


def _development_state():
    state = create_initial_state()
    state["request_context"]["division"] = "SAC"
    state["analysis_overview"]["request_type"] = DEVELOPMENT_PROJECT
    return state


def test_project_name_is_a_dedicated_pms_search_control_while_model_keeps_custom_undecided_control():
    assert 'id="pmsProjectField"' in HTML_TEMPLATE
    assert 'data-pms-combobox' in HTML_TEMPLATE
    assert 'data-pms-menu role="listbox"' in HTML_TEMPLATE
    assert '프로젝트명 또는 모델명으로 검색' in HTML_TEMPLATE
    assert '.pms-combobox .undecided-combobox-toggle:hover{background:transparent;color:#525252}' in HTML_TEMPLATE
    assert HTML_TEMPLATE.count('data-undecided-combobox') >= 1
    assert 'id="modelSuffixInput" data-path="analysis_overview.model_suffix" data-undecided-input' in HTML_TEMPLATE
    assert 'id="projectNameInput" data-path="analysis_overview.project_name" data-undecided-input' not in HTML_TEMPLATE


def test_pms_search_results_and_keyboard_interaction_are_scoped_to_screen_two_control():
    assert 'data-pms-active="false" aria-selected="false"' in HTML_TEMPLATE
    assert 'item.grade || "-"' in HTML_TEMPLATE
    assert 'item.event || "-"' in HTML_TEMPLATE
    assert 'function setPmsActiveResult(index)' in HTML_TEMPLATE
    assert 'event.key === "ArrowDown" || event.key === "ArrowUp"' in HTML_TEMPLATE
    assert 'event.key === "Enter" && pmsActiveIndex >= 0' in HTML_TEMPLATE
    assert 'event.key === "Escape"' in HTML_TEMPLATE


def test_pms_master_search_is_division_scoped_and_matches_project_or_rep_model():
    initial = search_pms_projects("SAC")
    assert initial and all(item["division"] == "SAC" for item in initial)
    selected = initial[0]
    assert any(item["internal_id"] == selected["internal_id"] for item in search_pms_projects("SAC", selected["project"][:6]))
    assert any(item["internal_id"] == selected["internal_id"] for item in search_pms_projects("SAC", selected["rep_model"][:6]))


def test_pms_search_returns_all_division_projects_in_create_date_order():
    master = load_pms_project_master()

    for division in ("SAC", "RAC", "Air Care", "Chiller"):
        results = search_pms_projects(division)
        expected_count = sum(row["division"] == division for row in master)

        assert len(results) == expected_count
        assert [row["create_date"] for row in results] == sorted(
            (row["create_date"] for row in results), reverse=True
        )


def test_pms_selection_sets_reference_fields_and_resets_editable_defaults():
    selected = search_pms_projects("SAC")[0]
    state = _development_state()
    state["analysis_overview"].update({"development_grade": "manual", "npi_stage": "manual", "model_suffix": "manual"})
    state = apply_pms_project_selection(state, selected["internal_id"])
    overview = state["analysis_overview"]
    assert field_value(overview["selected_pms_project_id"]) == selected["internal_id"]
    assert field_value(overview["project_name"]) == selected["project"]
    assert field_value(overview["pms_project_code"]) == selected["pms_project_code"]
    assert field_value(overview["region"]) == selected["region"]
    assert field_value(overview["development_grade"]) == selected["grade"]
    assert field_value(overview["npi_stage"]) == selected["event"]
    assert field_value(overview["model_suffix"]) == selected["rep_model"]


def test_pms_selection_replaces_every_derived_value_when_the_next_project_has_blanks(monkeypatch):
    projects = {
        "SAC:A": {
            "internal_id": "SAC:A", "division": "SAC", "project": "Project A",
            "pms_project_code": "PMS-A", "region": "KR", "grade": "B", "event": "DV", "rep_model": "MODEL-A",
        },
        "SAC:B": {
            "internal_id": "SAC:B", "division": "SAC", "project": "Project B",
            "pms_project_code": "PMS-B", "region": "US", "grade": "", "event": "PV", "rep_model": "",
        },
    }
    monkeypatch.setattr(state_module, "find_pms_project", lambda internal_id: projects.get(str(internal_id)))

    state = apply_pms_project_selection(_development_state(), "SAC:A")
    state = apply_pms_project_selection(state, "SAC:B")
    overview = state["analysis_overview"]

    assert field_value(overview["project_name"]) == "Project B"
    assert field_value(overview["development_grade"]) == ""
    assert field_value(overview["npi_stage"]) == "PV"
    assert field_value(overview["model_suffix"]) == ""


def test_pms_api_selects_only_the_current_screen_one_division():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()
    project = client.get("/api/pms-projects?division=Air%20Care").get_json()["projects"][0]
    state = create_initial_state()
    state["request_context"]["division"] = "Air Care"
    state["analysis_overview"]["request_type"] = DEVELOPMENT_PROJECT

    response = client.post("/api/pms-projects/select", json={"state": state, "internal_id": project["internal_id"]})

    assert response.status_code == 200
    overview = response.get_json()["state"]["analysis_overview"]
    assert field_value(overview["selected_pms_project_id"]) == project["internal_id"]
    assert field_value(overview["project_name"]) == project["project"]
    assert field_value(overview["region"]) == project["region"]


def test_development_project_requires_a_real_pms_selection_and_agent_cannot_write_project_name():
    state = _development_state()
    codes = {issue["code"] for issue in validate_state(state)["blocking"]}
    assert "analysis_overview.selected_pms_project_id.required_missing" in codes
    paths = {target["path"] for target in build_agent_write_contract(state)["operations"]["set"]["targets"]}
    assert "analysis_overview.project_name" not in paths


def test_non_development_request_clears_pms_values_but_has_no_pms_validation():
    selected = search_pms_projects("SAC")[0]
    state = apply_pms_project_selection(_development_state(), selected["internal_id"])
    state["analysis_overview"]["request_type"] = QUALITY_IMPROVEMENT
    state = sanitize_state(state)
    overview = state["analysis_overview"]
    for key in ("selected_pms_project_id", "project_name", "pms_project_code", "region", "development_grade", "npi_stage", "model_suffix"):
        assert field_value(overview[key]) == ""
    assert "analysis_overview.selected_pms_project_id.required_missing" not in {
        issue["code"] for issue in validate_state(state)["blocking"]
    }


def test_screen_one_division_change_invalidates_the_existing_pms_selection():
    selected = search_pms_projects("SAC")[0]
    state = apply_pms_project_selection(_development_state(), selected["internal_id"])
    state["request_context"]["division"] = "RAC"

    state = sanitize_state(state)

    overview = state["analysis_overview"]
    assert field_value(overview["selected_pms_project_id"]) == ""
    assert field_value(overview["project_name"]) == ""
    assert field_value(overview["pms_project_code"]) == ""
    assert field_value(overview["region"]) == ""


def test_request_type_select_change_immediately_syncs_pms_control_state():
    pms_start = HTML_TEMPLATE.index("    function isDevelopmentProject()")
    pms_end = HTML_TEMPLATE.index("    function setPmsMenuOpen(open)", pms_start)
    dropdown_start = HTML_TEMPLATE.index("    function applyRequestTypeChange(value)")
    dropdown_end = HTML_TEMPLATE.index("    function handleConditionSelectChange(select)", dropdown_start)
    handlers = HTML_TEMPLATE[pms_start:pms_end] + HTML_TEMPLATE[dropdown_start:dropdown_end]
    script = f'''
const requestTypeInput = {{value:"", hidden:true, focused:false, focus() {{ this.focused = true; }}}};
const customControl = {{hidden:true}};
const projectInput = {{value:"", disabled:true}};
const gradeInput = {{disabled:true}};
const npiInput = {{disabled:true}};
const gradeSelect = {{value:"", disabled:true}};
const npiSelect = {{value:"", disabled:true}};
const modelInput = {{value:"", disabled:false}};
const pmsToggle = {{disabled:true}};
const helper = {{hidden:true, textContent:""}};
const pmsField = {{dataset:{{}}, setAttribute() {{}}}};
const pmsCombobox = {{dataset:{{}}}};
const select = {{value:"개발 프로젝트", hidden:false, dataset:{{dropdownPath:"analysis_overview.request_type"}}, focus() {{}}}};
const document = {{
  querySelector(selector) {{
    if (selector === 'select[data-dropdown-path="analysis_overview.request_type"]') return select;
    if (selector === 'input[data-path="analysis_overview.request_type"]') return requestTypeInput;
    if (selector === '[data-dropdown-custom-path="analysis_overview.request_type"]') return customControl;
    if (selector === '[data-pms-toggle]') return pmsToggle;
    if (selector === '[data-pms-combobox]') return pmsCombobox;
    if (selector === 'select[data-dropdown-path="analysis_overview.development_grade"]') return gradeSelect;
    if (selector === 'select[data-dropdown-path="analysis_overview.npi_stage"]') return npiSelect;
    if (selector === 'input[data-path="analysis_overview.development_grade"]') return gradeInput;
    if (selector === 'input[data-path="analysis_overview.npi_stage"]') return npiInput;
    if (selector === '[data-path="analysis_overview.development_grade"]') return gradeInput;
    if (selector === '[data-path="analysis_overview.npi_stage"]') return npiInput;
    if (selector === '[data-path="analysis_overview.model_suffix"]') return modelInput;
    return null;
  }},
}};
const CSS = {{escape:value => value}};
const $ = id => ({{pmsProjectField:pmsField, projectNameInput:projectInput, pmsProjectHelper:helper}})[id] || null;
const asObj = value => value && typeof value === "object" ? value : {{}};
const fieldDisplayValue = value => value && typeof value === "object" ? String(value.value || "") : String(value || "");
const contextText = value => String(value ?? "").trim();
const pathInput = (section, key) => document.querySelector(`[data-path="${{section}}.${{key}}"]`);
const touchedFields = new Set();
let requestState = {{analysis_overview:{{request_type:"품질 개선", selected_pms_project_id:"SAC:2", project_name:"OLD"}}}};
let navigationRenders = 0;
let previewRefreshes = 0;
function setPmsMenuOpen(_open) {{}}
function syncDropdownForPath(path, value) {{
  const select = document.querySelector(`select[data-dropdown-path="${{path}}"]`);
  if (select) select.value = value;
}}
function syncUndecidedCombobox(_path, _value) {{}}
function renderScreenNavigation() {{ navigationRenders += 1; }}
function schedulePreviewRefresh() {{ previewRefreshes += 1; }}
{handlers}

handleDropdownChange(select);
if (projectInput.disabled || gradeInput.disabled || npiInput.disabled || gradeSelect.disabled || npiSelect.disabled || pmsToggle.disabled) throw new Error("development project did not enable PMS controls");
if (requestState.analysis_overview.request_type !== "개발 프로젝트") throw new Error("request type state was not updated from the select");
if (requestState.analysis_overview.project_name !== "") throw new Error("PMS selection was not cleared");

select.value = "품질 개선";
handleDropdownChange(select);
if (!projectInput.disabled || !gradeInput.disabled || !npiInput.disabled || !gradeSelect.disabled || !npiSelect.disabled) throw new Error("quality improvement did not disable all PMS controls");

select.value = "필드 이슈";
handleDropdownChange(select);
if (!projectInput.disabled) throw new Error("non-development request did not disable PMS control");

select.value = "__custom__";
handleDropdownChange(select);
if (!select.hidden || customControl.hidden || !requestTypeInput.focused || !projectInput.disabled) throw new Error("custom request-type mode did not retain disabled PMS control");

applyRequestTypeChange("사용자 기타 입력");
if (!projectInput.disabled) throw new Error("custom request type enabled PMS control");
restoreDropdownControl({{dataset:{{dropdownRestorePath:"analysis_overview.request_type"}}}});
if (select.hidden || select.value !== "" || requestTypeInput.value !== "" || !customControl.hidden) throw new Error("request type did not restore to the dropdown");
if (requestState.analysis_overview.request_type !== "" || !projectInput.disabled || !gradeSelect.disabled || !npiSelect.disabled) throw new Error("dropdown restore did not use the request-type transition");
if (navigationRenders < 5 || previewRefreshes < 5) throw new Error("request type UI lifecycle did not run");
'''

    completed = subprocess.run(
        ["node", "-e", script], capture_output=True, text=True, encoding="utf-8", check=False
    )

    assert completed.returncode == 0, completed.stderr
