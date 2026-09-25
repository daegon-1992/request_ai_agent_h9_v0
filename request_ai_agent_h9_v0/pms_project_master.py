"""Read-only PMS Project Master imported from the Division source workbooks.

The supplied workbooks are XLSX files, but this project deliberately has no
spreadsheet runtime dependency.  The small reader below consumes only the
first worksheet and the columns used by SCREEN-02.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree
from zipfile import ZipFile


_MAIN_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_WORKBOOK_REL_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"

_SOURCES = {
    "Air Care": "20260915_PMS_Project_Running_Aircare.xlsx",
    "SAC": "20260915_PMS_Project_Running_CAC.xlsx",
    "Chiller": "20260915_PMS_Project_Running_Chiller.xlsx",
    "RAC": "20260915_PMS_Project_Running_RAC.xlsx",
}
_DIVISION_ALIASES = {"Aircare": "Air Care", "AIR_CARE": "Air Care"}
_REQUIRED_COLUMNS = {
    "Project": "project",
    "PMS Project Code": "pms_project_code",
    "Region": "region",
    "Grade": "grade",
    "Event": "event",
    "Rep Model": "rep_model",
    "Create Date": "create_date",
}


def _clean(value: Any) -> str:
    return str(value or "").replace("\x00", "").strip()


def normalize_pms_division(value: Any) -> str:
    division = _clean(value)
    return _DIVISION_ALIASES.get(division, division)


def _column_name(cell_reference: str) -> str:
    return "".join(char for char in cell_reference if char.isalpha())


def _shared_strings(archive: ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(node.text or "" for node in item.iter(f"{_MAIN_NS}t")) for item in root]


def _cell_text(cell: ElementTree.Element, shared: list[str]) -> str:
    value = cell.find(f"{_MAIN_NS}v")
    if value is None:
        inline = cell.find(f"{_MAIN_NS}is")
        return "" if inline is None else "".join(node.text or "" for node in inline.iter(f"{_MAIN_NS}t"))
    text = value.text or ""
    return shared[int(text)] if cell.get("t") == "s" and text else text


def _first_sheet_path(archive: ZipFile) -> str:
    workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
    sheet = workbook.find(f".//{_MAIN_NS}sheet")
    if sheet is None:
        raise ValueError("PMS workbook has no worksheet.")
    relation_id = sheet.get(f"{_REL_NS}id")
    relationships = ElementTree.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    target = next(
        (item.get("Target", "") for item in relationships if item.get("Id") == relation_id),
        "",
    )
    if not target:
        raise ValueError("PMS workbook worksheet relation is missing.")
    return "xl/" + target.lstrip("/")


def _worksheet_rows(path: Path) -> Iterable[dict[str, str]]:
    with ZipFile(path) as archive:
        shared = _shared_strings(archive)
        root = ElementTree.fromstring(archive.read(_first_sheet_path(archive)))
        for row in root.findall(f".//{_MAIN_NS}sheetData/{_MAIN_NS}row"):
            yield {
                _column_name(cell.get("r", "")): _cell_text(cell, shared)
                for cell in row.findall(f"{_MAIN_NS}c")
            }


def _date_key(value: str) -> int:
    digits = "".join(char for char in _clean(value) if char.isdigit())
    return int(digits[:8]) if len(digits) >= 8 else 0


def _load_source(division: str, path: Path) -> list[dict[str, str]]:
    rows = list(_worksheet_rows(path))
    if not rows:
        raise ValueError(f"PMS workbook is empty: {path.name}")
    header = rows[0]
    positions = {value: key for key, value in header.items()}
    missing = [name for name in _REQUIRED_COLUMNS if name not in positions]
    if missing:
        raise ValueError(f"PMS workbook has unsupported columns ({path.name}): {', '.join(missing)}")
    master: list[dict[str, str]] = []
    for row_number, row in enumerate(rows[1:], start=2):
        item = {field: _clean(row.get(positions[column])) for column, field in _REQUIRED_COLUMNS.items()}
        if not item["project"]:
            continue
        if not item["pms_project_code"]:
            raise ValueError(
                f"PMS Project Code is missing: division={division}, row={row_number}, project={item['project']}"
            )
        item.update({
            "internal_id": item["pms_project_code"],
            "division": division,
        })
        master.append(item)
    return master


@lru_cache(maxsize=1)
def load_pms_project_master() -> tuple[dict[str, str], ...]:
    docs = Path(__file__).resolve().parents[1] / "docs"
    master: list[dict[str, str]] = []
    for division, filename in _SOURCES.items():
        path = docs / filename
        if not path.is_file():
            raise FileNotFoundError(f"PMS source workbook is missing: {path}")
        master.extend(_load_source(division, path))
    projects_by_code: dict[str, dict[str, str]] = {}
    for item in master:
        code = item["pms_project_code"]
        previous = projects_by_code.get(code)
        if previous is not None:
            raise ValueError(
                "PMS Project Code is duplicated: "
                f"code={code}, first={previous['division']}/{previous['project']}, "
                f"duplicate={item['division']}/{item['project']}"
            )
        projects_by_code[code] = item
    return tuple(master)


def find_pms_project(internal_id: Any) -> dict[str, str] | None:
    wanted = _clean(internal_id)
    return next((dict(item) for item in load_pms_project_master() if item["internal_id"] == wanted), None)


def search_pms_projects(division: Any, query: Any = "") -> list[dict[str, str]]:
    """Return every matching project for one Division, newest Create Date first."""

    wanted_division = normalize_pms_division(division)
    needle = _clean(query).casefold()
    matches = [
        dict(item)
        for item in load_pms_project_master()
        if item["division"] == wanted_division
        and (not needle or needle in item["project"].casefold() or needle in item["rep_model"].casefold())
    ]
    matches.sort(
        key=lambda item: (
            -_date_key(item["create_date"]),
            item["project"].casefold(),
            item["pms_project_code"],
        )
    )
    return matches
