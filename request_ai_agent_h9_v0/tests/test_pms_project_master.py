from __future__ import annotations

import request_ai_agent_h9_v0.pms_project_master as pms_project_master


def test_internal_id_is_the_unique_pms_project_code_and_supports_lookup():
    projects = pms_project_master.load_pms_project_master()

    assert len({project["pms_project_code"] for project in projects}) == len(projects)
    for project in projects:
        assert project["internal_id"] == project["pms_project_code"]
        assert pms_project_master.find_pms_project(project["pms_project_code"]) == project


def test_source_row_position_does_not_change_the_pms_project_code_id(monkeypatch, tmp_path):
    header = {
        "A": "Project", "B": "PMS Project Code", "C": "Region", "D": "Grade",
        "E": "Event", "F": "Rep Model", "G": "Create Date",
    }
    source_rows = [
        [header, {"A": "First", "B": "PJT-001"}, {"A": "Target", "B": "PJT-002"}],
        [header, {"A": "Inserted", "B": "PJT-000"}, {"A": "First", "B": "PJT-001"}, {"A": "Target", "B": "PJT-002"}],
    ]

    for rows in source_rows:
        monkeypatch.setattr(pms_project_master, "_worksheet_rows", lambda _path, rows=rows: iter(rows))
        projects = pms_project_master._load_source("SAC", tmp_path / "source.xlsx")
        target = next(project for project in projects if project["project"] == "Target")
        assert target["internal_id"] == "PJT-002"


def test_search_uses_create_date_descending_then_deterministic_secondary_sort(monkeypatch):
    monkeypatch.setattr(
        pms_project_master,
        "load_pms_project_master",
        lambda: (
            {"division": "SAC", "project": "Zulu", "pms_project_code": "PJT-3", "internal_id": "PJT-3", "create_date": "2026-09-15", "rep_model": ""},
            {"division": "SAC", "project": "Beta", "pms_project_code": "PJT-2", "internal_id": "PJT-2", "create_date": "2026-09-20", "rep_model": ""},
            {"division": "SAC", "project": "Alpha", "pms_project_code": "PJT-1", "internal_id": "PJT-1", "create_date": "2026-09-20", "rep_model": ""},
        ),
    )

    assert [project["internal_id"] for project in pms_project_master.search_pms_projects("SAC")] == [
        "PJT-1", "PJT-2", "PJT-3",
    ]
