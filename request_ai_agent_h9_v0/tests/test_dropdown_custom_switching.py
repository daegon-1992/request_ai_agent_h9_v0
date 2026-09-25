from __future__ import annotations

from request_ai_agent_h9_v0 import create_app
from request_ai_agent_h9_v0.constants import DROPDOWN_OPTION_DEFS
from request_ai_agent_h9_v0.pms_project_master import load_pms_project_master
from request_ai_agent_h9_v0.product_hierarchy import build_product_hierarchy_payload
from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


SWITCHING_PATHS = (
    "basic_info.division",
    "basic_info.requester_role",
    "analysis_overview.development_grade",
    "analysis_overview.npi_stage",
)


def test_requested_dropdowns_include_undecided():
    assert "미정" in DROPDOWN_OPTION_DEFS["analysis_overview.development_grade"]
    assert "미정" in DROPDOWN_OPTION_DEFS["analysis_overview.npi_stage"]
    assert "fallback_product_group_options" not in build_product_hierarchy_payload()
    assert 'id="quickProductLineupSelect"' in HTML_TEMPLATE


def test_pms_grade_and_event_values_are_merged_into_the_sorted_dropdowns():
    master = load_pms_project_master()
    expected_grades = sorted({row["grade"] for row in master}) + ["선행", "미정", "직접 입력"]
    expected_events = sorted({row["event"] for row in master}) + ["미정", "직접 입력"]

    assert DROPDOWN_OPTION_DEFS["analysis_overview.development_grade"] == expected_grades
    assert DROPDOWN_OPTION_DEFS["analysis_overview.npi_stage"] == expected_events
    assert '"analysis_overview.development_grade": ["A","B","B_Mi"' in HTML_TEMPLATE
    assert '"analysis_overview.npi_stage": ["CP","DV","MP","MQ","PV","Pre MP","Pre-MP"' in HTML_TEMPLATE


def test_all_select_pickers_share_the_grade_list_maximum_and_internal_scroll():
    assert "--ui-select-picker-max-height:320px" in HTML_TEMPLATE
    assert ".select-picker-menu{position:fixed;z-index:200;max-height:var(--ui-select-picker-max-height);overflow-y:auto;overscroll-behavior:contain;" in HTML_TEMPLATE
    assert ".undecided-combobox-menu,.pms-combobox-menu{" in HTML_TEMPLATE
    assert "max-height:var(--ui-select-picker-max-height);overflow-y:auto;overscroll-behavior:contain;" in HTML_TEMPLATE
    assert 'document.addEventListener("pointerdown", handleSelectPickerPointerDown, true);' in HTML_TEMPLATE
    assert 'document.addEventListener("scroll", handleSelectPickerScroll, true);' in HTML_TEMPLATE


def test_served_api_responses_include_all_requested_undecided_options():
    client = create_app().test_client()
    bootstrap = client.get("/api/bootstrap")
    hierarchy = client.get("/api/product-hierarchy")

    assert bootstrap.status_code == 200
    assert hierarchy.status_code == 200
    ui_options = bootstrap.get_json()["schema"]["ui_options"]
    assert "미정" in ui_options["analysis_overview.development_grade"]
    assert "미정" in ui_options["analysis_overview.npi_stage"]
    assert hierarchy.get_json()["row_count"] == 251


def test_requested_custom_fields_replace_the_dropdown_with_an_input():
    for path in SWITCHING_PATHS:
        assert f'data-dropdown-path="{path}"' in HTML_TEMPLATE
        assert f'data-dropdown-custom-path="{path}" hidden' in HTML_TEMPLATE
        assert f'data-dropdown-restore-path="{path}"' in HTML_TEMPLATE

    assert "select.hidden = customMode;" in HTML_TEMPLATE
    assert "if (customControl) customControl.hidden = !customMode;" in HTML_TEMPLATE
    assert 'if (dropdownRestore) { restoreDropdownControl(dropdownRestore); return; }' in HTML_TEMPLATE


def test_direct_input_and_restore_clear_the_previous_dropdown_value():
    assert 'if (select.value === "__custom__") {\n        input.value = "";\n        select.hidden = true;' in HTML_TEMPLATE
    assert 'select.hidden = false;\n      select.value = "";\n      input.value = "";' in HTML_TEMPLATE
