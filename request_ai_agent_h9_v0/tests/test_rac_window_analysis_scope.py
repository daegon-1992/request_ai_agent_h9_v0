from __future__ import annotations

from copy import deepcopy
from io import BytesIO
from zipfile import ZipFile

import pytest

from request_ai_agent_h9_v0.agent_context import _project_request_state
from request_ai_agent_h9_v0.preview_document import build_request_preview
from request_ai_agent_h9_v0.product_taxonomy import load_product_taxonomy
from request_ai_agent_h9_v0.request_context_confirmation import confirm_request_context_state
from request_ai_agent_h9_v0.state import create_initial_state, make_field, sanitize_state
from request_ai_agent_h9_v0.ui import HTML_TEMPLATE
from request_ai_agent_h9_v0.validator import state_with_validation
from request_ai_agent_h9_v0.word_export import build_word_docx


def _taxonomy_path(*, window: bool) -> dict:
    return next(
        path
        for path in load_product_taxonomy()["paths"]
        if path["division"] == "RAC"
        and ((path["product_lineup"] == "Window") is window)
    )


def _confirm_window(scope: str) -> dict:
    path = _taxonomy_path(window=True)
    state, _fieldset = confirm_request_context_state(
        create_initial_state(),
        {
            "taxonomy_id": path["taxonomy_id"],
            "analysis_type": "풍량",
            "analysis_scope": scope,
        },
    )
    return state


def test_rac_window_scope_is_canonical_and_is_not_operation_mode():
    state = _confirm_window("both")

    assert state["request_context"]["analysis_scope"] == "both"
    assert state["request_context"]["operation_mode"] == ""
    assert {
        card["analysis_scope"] for card in state["conditions"]["condition_sets"]
    } == {"indoor", "outdoor"}

    with pytest.raises(ValueError, match="missing_context:analysis_scope"):
        path = _taxonomy_path(window=True)
        confirm_request_context_state(
            create_initial_state(),
            {"taxonomy_id": path["taxonomy_id"], "analysis_type": "풍량"},
        )


def test_non_window_product_ignores_analysis_scope_and_keeps_existing_shape():
    path = _taxonomy_path(window=False)
    state, _fieldset = confirm_request_context_state(
        create_initial_state(),
        {
            "taxonomy_id": path["taxonomy_id"],
            "analysis_type": "풍량",
            "analysis_scope": "both",
        },
    )

    assert state["request_context"]["analysis_scope"] == ""
    assert all("analysis_scope" not in card for card in state["conditions"]["condition_sets"])
    assert "dropdown_options_by_scope" not in state["case_matrix"]


def test_scope_change_does_not_merge_other_side_conditions_or_cases():
    state = _confirm_window("both")
    state["geometry"]["base_product"]["drawing_no"] = make_field("WINDOW-001")
    state = sanitize_state(state)
    outdoor_ids = {
        card["id"] for card in state["conditions"]["condition_sets"]
        if card["analysis_scope"] == "outdoor"
    }

    state["request_context"]["analysis_scope"] = "indoor"
    indoor_only = sanitize_state(state)

    assert {card["analysis_scope"] for card in indoor_only["conditions"]["condition_sets"]} == {"indoor"}
    assert outdoor_ids.isdisjoint({card["id"] for card in indoor_only["conditions"]["condition_sets"]})
    assert {row["analysis_scope"] for row in indoor_only["case_matrix"]["rows"]} == {"indoor"}


def test_both_scopes_keep_condition_options_cases_and_duplicate_validation_independent():
    state = _confirm_window("both")
    state["geometry"]["base_product"]["drawing_no"] = make_field("WINDOW-001")
    for card in state["conditions"]["condition_sets"]:
        if card["type"] == "operating":
            card["fans"][0]["values"]["fan_rpm"] = "900"
        else:
            for key, field in card["fields"].items():
                if key != "name":
                    field["value"] = "1"
    state = sanitize_state(state)

    cards = state["conditions"]["condition_sets"]
    indoor_ids = {card["id"] for card in cards if card["analysis_scope"] == "indoor"}
    outdoor_ids = {card["id"] for card in cards if card["analysis_scope"] == "outdoor"}
    options = state["case_matrix"]["dropdown_options_by_scope"]

    assert indoor_ids.isdisjoint(outdoor_ids)
    assert {item["value"] for item in options["indoor"]["fan"]}.issubset(indoor_ids)
    assert {item["value"] for item in options["outdoor"]["fan"]}.issubset(outdoor_ids)
    assert [(row["analysis_scope"], row["visible_cells"]["case_no"]) for row in state["case_matrix"]["rows"]] == [
        ("indoor", "1"),
        ("outdoor", "1"),
    ]

    indoor = next(row for row in state["case_matrix"]["rows"] if row["analysis_scope"] == "indoor")
    duplicate = deepcopy(indoor)
    duplicate.update({"case_id": "indoor_extra", "auto_geometry_id": ""})
    state["case_matrix"]["rows"].append(duplicate)
    validated = state_with_validation(state)
    duplicates = [
        issue
        for issue in validated["review"]["validator"]["blocking"]
        if issue["code"] == "case_matrix.duplicate"
    ]

    assert [(issue["analysis_scope"], issue["case_no"], issue["duplicate_of_case_no"]) for issue in duplicates] == [
        ("indoor", 2, 1)
    ]
    assert validated["review"]["validator"]["coverage"]["by_scope"] == {
        "indoor": {"complete": True, "unused_items": []},
        "outdoor": {"complete": True, "unused_items": []},
    }


def test_preview_and_agent_projection_preserve_scope_boundaries():
    state = _confirm_window("both")
    state["geometry"]["base_product"]["drawing_no"] = make_field("WINDOW-001")
    state = sanitize_state(state)

    preview = build_request_preview(state)
    condition_section = next(section for section in preview["sections"] if section["key"] == "conditions")
    projection = _project_request_state(state)

    assert next(item for item in preview["sections"][1]["items"] if item["label"] == "해석 범위")["value"] == "실내·실외 모두"
    assert [group["label"] for group in condition_section["groups"]] == ["실내측", "실외측"]
    assert set(preview["case_matrix"]["by_scope"]) == {"indoor", "outdoor"}
    assert projection["request_context"]["analysis_scope"] == "both"
    assert {row["analysis_scope"] for row in projection["case_matrix"]["rows"]} == {"indoor", "outdoor"}


def test_window_scope_ui_uses_direct_choices_and_only_both_uses_tabs():
    scope_control = HTML_TEMPLATE.split('id="analysisScopeField"', 1)[1].split('</div>\n                    </div>', 1)[0]

    assert 'data-analysis-scope="indoor"' in scope_control
    assert 'data-analysis-scope="outdoor"' in scope_control
    assert 'data-analysis-scope="both"' in scope_control
    assert "실내·실외 모두" in scope_control
    assert "<select" not in scope_control
    assert "동시운전" not in scope_control
    assert 'contextText(context.division) === "RAC"' in HTML_TEMPLATE
    assert 'contextText(context.product_lineup) === "Window"' in HTML_TEMPLATE
    assert 'contextText(context.platform) === "Window"' in HTML_TEMPLATE
    assert 'if (!hasBothAnalysisScopes()) return "";' in HTML_TEMPLATE
    assert 'id="conditionScopeTabs"' in HTML_TEMPLATE
    assert 'id="caseScopeTabs"' in HTML_TEMPLATE
    assert 'const selectedScope = ["indoor","outdoor","both"].includes(contextText(context.analysis_scope)) ? context.analysis_scope : "";' in HTML_TEMPLATE
    assert '`${baseRequestTitle} · ${selectedScopeLabel}`' in HTML_TEMPLATE
    assert '`${scopeLabel(activeScope)} 해석 조건`' in HTML_TEMPLATE
    assert '`${scopeLabel(activeScope)} Case 구성`' in HTML_TEMPLATE
    assert '.workspace-shell .workspace-form .direct-choice button[aria-pressed="true"]' in HTML_TEMPLATE
    assert '.workspace-shell .workspace-form .analysis-scope-tabs button[aria-selected="true"]' in HTML_TEMPLATE
    assert 'requestFields.push(kv("해석 범위", scopeLabel(context.analysis_scope)))' in HTML_TEMPLATE
    assert 'data-preview-group-title>${scopeLabel(scope)}</h5>${conditionsBodyForScope(scope)}' in HTML_TEMPLATE
    assert 'data-preview-group-title>${scopeLabel(scope)}</h5>${matrixTableForScope(scope)}' in HTML_TEMPLATE


def test_word_export_keeps_indoor_and_outdoor_case_tables_separate():
    preview = {
        "request_title": "RAC Window 범위 구분",
        "request_no": "REQ-WINDOW-001",
        "sections": [
            {
                "title": "요청 내용",
                "blocks": [
                    {"type": "field", "label": "해석 범위", "value": "실내·실외 모두"},
                ],
            },
            {
                "title": "해석 조건",
                "blocks": [
                    {"type": "group", "title": "실내측"},
                    {"type": "table", "key": "operating_conditions_indoor", "headers": ["", "팬 개수", "팬 회전 설정"], "rows": [["운전 1", "1", "900 RPM"]]},
                    {"type": "group", "title": "실외측"},
                    {"type": "table", "key": "operating_conditions_outdoor", "headers": ["", "팬 개수", "팬 회전 설정"], "rows": [["운전 1", "2", "1100 RPM"]]},
                ],
            },
            {
                "title": "Case Matrix",
                "blocks": [
                    {"type": "group", "title": "실내측"},
                    {"type": "table", "key": "case_matrix_indoor", "headers": ["Case", "해석 제품", "운전 조건"], "rows": [["1", "WINDOW-001", "900 RPM"]]},
                    {"type": "group", "title": "실외측"},
                    {"type": "table", "key": "case_matrix_outdoor", "headers": ["Case", "해석 제품", "운전 조건"], "rows": [["1", "WINDOW-001", "1100 RPM"]]},
                ],
            },
        ],
    }

    with ZipFile(BytesIO(build_word_docx(preview))) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")

    assert "실내·실외 모두" in xml
    assert xml.count("실내측") == 2
    assert xml.count("실외측") == 2
    assert "900 RPM" in xml
    assert "1100 RPM" in xml


def _add_comparison_geometry(state: dict, *, geometry_id: str = "comparison_scope_001", drawing_no: str = "WINDOW-002") -> dict:
    state = deepcopy(state)
    state["geometry"]["comparison_products"].append(
        {
            "geometry_id": geometry_id,
            "role": "comparison",
            "drawing_no": make_field(drawing_no),
            "display_name": "",
            "difference_from_base": "",
        }
    )
    return sanitize_state(state)


def test_both_scope_requires_every_geometry_in_indoor_and_outdoor_case_matrices():
    state = _confirm_window("both")
    state["geometry"]["base_product"]["drawing_no"] = make_field("WINDOW-001")
    state = _add_comparison_geometry(state)

    comparison_id = state["geometry"]["comparison_products"][0]["geometry_id"]
    state["case_matrix"]["rows"] = [
        row
        for row in state["case_matrix"]["rows"]
        if not (row["analysis_scope"] == "outdoor" and row["geometry_id"] == comparison_id)
    ]

    validated = state_with_validation(state)
    issues = [
        issue
        for issue in validated["review"]["validator"]["blocking"]
        if issue["code"] == "case_matrix.scope_geometry_missing"
    ]

    assert [(issue["analysis_scope"], issue["geometry_id"], issue["field_label"]) for issue in issues] == [
        ("outdoor", comparison_id, "WINDOW-002")
    ]
    assert validated["review"]["submission"]["can_submit"] is False


def test_both_scope_allows_different_case_counts_when_every_geometry_exists_on_both_sides():
    state = _confirm_window("both")
    state["geometry"]["base_product"]["drawing_no"] = make_field("WINDOW-001")
    state = _add_comparison_geometry(state)

    indoor = next(row for row in state["case_matrix"]["rows"] if row["analysis_scope"] == "indoor")
    extra = deepcopy(indoor)
    extra.update({"case_id": "indoor_extra_count", "auto_geometry_id": ""})
    extra["condition_values"] = dict(extra["condition_values"])
    first_key = next(iter(extra["condition_values"]), "")
    options = state["case_matrix"]["dropdown_options_by_scope"]["indoor"].get(first_key, [])
    if len(options) > 1:
        extra["condition_values"][first_key] = options[1]["value"]
    else:
        extra["geometry_id"] = state["geometry"]["comparison_products"][0]["geometry_id"]
    state["case_matrix"]["rows"].append(extra)

    validated = state_with_validation(state)
    issues = [
        issue
        for issue in validated["review"]["validator"]["blocking"]
        if issue["code"] == "case_matrix.scope_geometry_missing"
    ]

    assert issues == []
    indoor_count = sum(row["analysis_scope"] == "indoor" for row in validated["case_matrix"]["rows"])
    outdoor_count = sum(row["analysis_scope"] == "outdoor" for row in validated["case_matrix"]["rows"])
    assert indoor_count != outdoor_count


def test_single_scope_does_not_apply_both_geometry_scope_coverage_rule():
    state = _confirm_window("indoor")
    state["geometry"]["base_product"]["drawing_no"] = make_field("WINDOW-001")
    state = _add_comparison_geometry(state)

    validated = state_with_validation(state)
    assert not any(
        issue["code"] == "case_matrix.scope_geometry_missing"
        for issue in validated["review"]["validator"]["blocking"]
    )


def test_screen_four_gate_applies_to_bottom_and_workflow_navigation_for_every_scope():
    gate_start = HTML_TEMPLATE.index("async function confirmConditionsBeforeCaseMatrix()")
    gate_end = HTML_TEMPLATE.index("function revealMissingFanControl", gate_start)
    gate = HTML_TEMPLATE[gate_start:gate_end]

    assert 'await refreshPreview();' in gate
    assert 'const issues = conditionValidationIssues();' in gate
    assert 'if (!hasBothAnalysisScopes())' not in gate
    assert HTML_TEMPLATE.count('if (targetScreen === "SCREEN-05")') == 3
