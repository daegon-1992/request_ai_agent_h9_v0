from __future__ import annotations

from copy import deepcopy

from request_ai_agent_h9_v0.condition_fieldsets import default_condition_sets, make_condition_card
from request_ai_agent_h9_v0.state import create_initial_state, sanitize_state


def _set_field(card, field_key, value):
    card["fields"][field_key]["value"] = value


def _configured_state(analysis_type: str = "이슬맺힘"):
    state = create_initial_state()
    state["request_context"].update(
        {
            "analysis_type": analysis_type,
            "context_locked": True,
        }
    )
    state["geometry"]["base_product"]["drawing_no"] = "DRAW-A"

    cards = default_condition_sets(state["request_context"])
    operating = next(card for card in cards if card["type"] == "operating")
    operating["fans"][0]["values"]["fan_rpm"] = "700"

    space_1 = next(card for card in cards if card["type"] == "space_environment")
    supply_1 = next(card for card in cards if card["type"] == "supply_air")
    _set_field(space_1, "room_temp", "25")
    _set_field(supply_1, "heat_exchanger_temp", "12")
    if "room_rh" in space_1["fields"]:
        _set_field(space_1, "room_rh", "50")
    if "heat_exchanger_rh" in supply_1["fields"]:
        _set_field(supply_1, "heat_exchanger_rh", "95")

    space_2 = make_condition_card("space_environment", 2)
    supply_2 = make_condition_card("supply_air", 2)
    _set_field(space_2, "room_temp", "30")
    _set_field(supply_2, "heat_exchanger_temp", "15")
    if analysis_type == "이슬맺힘":
        _set_field(space_2, "room_rh", "70")
        _set_field(supply_2, "heat_exchanger_rh", "90")

    state["conditions"]["condition_sets"] = [*cards, space_2, supply_2]
    return state


def test_dew_case_matrix_uses_condition_instances_for_space_and_supply_air():
    state = sanitize_state(_configured_state())
    matrix = state["case_matrix"]

    condition_columns = [
        (column["key"], column["label"])
        for column in matrix["visible_columns"]
        if column["kind"] == "condition"
    ]
    assert condition_columns == [
        ("fan", "운전 조건"),
        ("heat_exchanger", "열교환기 사양"),
        ("space_environment", "공간 환경 조건"),
        ("supply_air", "취출 공기 조건"),
    ]
    assert "room_temp" not in matrix["dropdown_options"]
    assert "room_rh" not in matrix["dropdown_options"]
    assert "heat_exchanger_temp" not in matrix["dropdown_options"]
    assert "heat_exchanger_rh" not in matrix["dropdown_options"]
    assert matrix["dropdown_options"]["space_environment"] == [
        {"value": "space_environment_1", "label": "25 °C / 50 %"},
        {"value": "space_environment_2", "label": "30 °C / 70 %"},
    ]
    assert matrix["dropdown_options"]["supply_air"] == [
        {"value": "supply_air_1", "label": "12 °C / 95 %"},
        {"value": "supply_air_2", "label": "15 °C / 90 %"},
    ]
    assert matrix["rows"][0]["condition_values"]["space_environment"] == "space_environment_1"
    assert matrix["rows"][0]["condition_values"]["supply_air"] == "supply_air_1"


def test_legacy_temperature_and_humidity_selections_migrate_only_as_an_exact_pair():
    state = _configured_state()
    state["case_matrix"] = {
        "rows": [
            {
                "case_id": "case_001",
                "geometry_id": "base_001",
                "auto_geometry_id": "base_001",
                "condition_values": {
                    "fan": "operating_1",
                    "heat_exchanger": "heat_exchanger_1",
                    "room_temp": "30",
                    "room_rh": "70",
                    "heat_exchanger_temp": "15",
                    "heat_exchanger_rh": "90",
                },
            }
        ],
        "geometry_snapshot_ids": ["base_001"],
    }

    matrix = sanitize_state(state)["case_matrix"]
    values = matrix["rows"][0]["condition_values"]

    assert values["space_environment"] == "space_environment_2"
    assert values["supply_air"] == "supply_air_2"
    assert "room_temp" not in values and "room_rh" not in values
    assert "heat_exchanger_temp" not in values and "heat_exchanger_rh" not in values


def test_ambiguous_legacy_pair_is_not_silently_defaulted_to_a_condition_card():
    state = _configured_state()
    duplicate = make_condition_card("space_environment", 3)
    _set_field(duplicate, "room_temp", "30")
    _set_field(duplicate, "room_rh", "70")
    state["conditions"]["condition_sets"].append(duplicate)
    state["case_matrix"] = {
        "rows": [
            {
                "case_id": "case_001",
                "geometry_id": "base_001",
                "auto_geometry_id": "base_001",
                "condition_values": {
                    "fan": "operating_1",
                    "heat_exchanger": "heat_exchanger_1",
                    "room_temp": "30",
                    "room_rh": "70",
                    "heat_exchanger_temp": "15",
                    "heat_exchanger_rh": "90",
                },
            }
        ],
        "geometry_snapshot_ids": ["base_001"],
    }

    values = sanitize_state(state)["case_matrix"]["rows"][0]["condition_values"]

    assert "space_environment" not in values
    assert values["supply_air"] == "supply_air_2"


def test_group_selection_survives_value_edit_and_updates_its_visible_label():
    state = _configured_state()
    state["case_matrix"] = {
        "rows": [
            {
                "case_id": "case_001",
                "geometry_id": "base_001",
                "auto_geometry_id": "base_001",
                "condition_values": {
                    "fan": "operating_1",
                    "heat_exchanger": "heat_exchanger_1",
                    "space_environment": "space_environment_2",
                    "supply_air": "supply_air_2",
                },
            }
        ],
        "geometry_snapshot_ids": ["base_001"],
    }
    normalized = sanitize_state(state)
    edited = deepcopy(normalized)
    space_2 = next(
        card
        for card in edited["conditions"]["condition_sets"]
        if card["id"] == "space_environment_2"
    )
    space_2["fields"]["room_rh"]["value"] = "65"

    matrix = sanitize_state(edited)["case_matrix"]

    assert matrix["rows"][0]["condition_values"]["space_environment"] == "space_environment_2"
    assert matrix["rows"][0]["visible_cells"]["space_environment"] == "30 °C / 65 %"


def test_temperature_only_analysis_still_uses_one_group_column_per_condition_card():
    state = sanitize_state(_configured_state("기류 패턴"))
    matrix = state["case_matrix"]

    assert matrix["dropdown_options"]["space_environment"] == [
        {"value": "space_environment_1", "label": "25 °C"},
        {"value": "space_environment_2", "label": "30 °C"},
    ]
    assert matrix["dropdown_options"]["supply_air"] == [
        {"value": "supply_air_1", "label": "12 °C"},
        {"value": "supply_air_2", "label": "15 °C"},
    ]
