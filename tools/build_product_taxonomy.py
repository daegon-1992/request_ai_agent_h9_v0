"""Build the runtime product taxonomy from the approved classification workbook."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"m": MAIN_NS, "r": REL_NS}
EXPECTED_HEADERS = ("DIVISION", "LEVEL1", "LEVEL2", "LEVEL3")
EXCLUDED_DIVISIONS = {"ESS"}
EXCLUDED_SAC_LEVEL1 = {"etc", "networkcontrol", "platform"}
DIVISION_CODES = {
    "SAC": "SAC",
    "RAC": "RAC",
    "Air Care": "AIR_CARE",
    "Chiller": "CHILLER",
}
CELL_CORRECTIONS = {
    "Siganture(PP)": "Signature(PP)",
    "Siganture(S7)": "Signature(S7)",
    "Accessary": "Accessory",
}
DERIVED_PLATFORM_DIVISIONS = {"Air Care", "RAC"}
LITERAL_NA_CHASSIS_PLATFORMS = {"Duct(Multi V)", "Duct(Single CAC)"}


def _cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    value = cell.find("m:v", NS)
    if cell.attrib.get("t") == "s" and value is not None:
        return shared_strings[int(value.text or "0")]
    inline = cell.find("m:is", NS)
    if cell.attrib.get("t") == "inlineStr" and inline is not None:
        return "".join(node.text or "" for node in inline.iter(f"{{{MAIN_NS}}}t"))
    return value.text if value is not None and value.text is not None else ""


def read_xlsx_rows(path: Path) -> list[tuple[str, str, str, str]]:
    """Read the first worksheet with only the Python standard library."""

    with zipfile.ZipFile(path) as archive:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared_strings = [
                "".join(node.text or "" for node in item.iter(f"{{{MAIN_NS}}}t"))
                for item in root.findall("m:si", NS)
            ]

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = {
            item.attrib["Id"]: item.attrib["Target"]
            for item in ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        }
        sheet = workbook.find("m:sheets", NS)
        if sheet is None or not list(sheet):
            raise ValueError("taxonomy_workbook_has_no_sheet")
        first_sheet = list(sheet)[0]
        relationship_id = first_sheet.attrib[f"{{{REL_NS}}}id"]
        target = relationships[relationship_id].replace("\\", "/").lstrip("/")
        if not target.startswith("xl/"):
            target = f"xl/{target}"
        root = ET.fromstring(archive.read(target))

        rows: list[tuple[str, str, str, str]] = []
        for row in root.findall(".//m:sheetData/m:row", NS):
            values: dict[str, str] = {}
            for cell in row.findall("m:c", NS):
                match = re.match(r"[A-Z]+", cell.attrib.get("r", "A"))
                if match:
                    values[match.group()] = _cell_value(cell, shared_strings)
            rows.append(tuple(values.get(column, "") for column in ("A", "B", "C", "D")))
        return rows


def _clean_cell(value: str) -> str:
    clean = str(value or "").replace("\x00", "").strip()
    return CELL_CORRECTIONS.get(clean, clean)


def _is_temporary(row: Iterable[str]) -> bool:
    values = tuple(row)
    return any("ETC" in value.upper() for value in values) or any(value.casefold() == "test" for value in values)


def clean_rows(rows: list[tuple[str, str, str, str]]) -> list[tuple[str, str, str, str]]:
    if not rows:
        raise ValueError("taxonomy_workbook_is_empty")
    headers = tuple(_clean_cell(value).upper().replace(" ", "") for value in rows[0])
    if headers != EXPECTED_HEADERS:
        raise ValueError(f"unexpected_taxonomy_headers:{headers!r}")

    cleaned: list[tuple[str, str, str, str]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for raw_row in rows[1:]:
        row = tuple(_clean_cell(value) for value in raw_row)
        if not any(row):
            continue
        if not all(row):
            raise ValueError(f"incomplete_taxonomy_path:{row!r}")
        division, level1, _level2, _level3 = row
        if division in EXCLUDED_DIVISIONS:
            continue
        if division == "SAC" and level1.casefold() in EXCLUDED_SAC_LEVEL1:
            continue
        if _is_temporary(row):
            continue
        if row in seen:
            continue
        seen.add(row)
        cleaned.append(row)
    return cleaned


def _identity_value(value: str | None) -> str:
    return "<NULL>" if value is None else value


def taxonomy_id(row: tuple[str, str, str, str | None]) -> str:
    digest = hashlib.sha1("\x1f".join(_identity_value(value) for value in row).encode("utf-8")).hexdigest()[:12].upper()
    return f"PTX-{digest}"


def variant_id(row: tuple[str, str, str, str]) -> str:
    digest = hashlib.sha1("\x1f".join(row).encode("utf-8")).hexdigest()[:12].upper()
    return f"PVX-{digest}"


def build_payload(rows: list[tuple[str, str, str, str]], *, source: str, version: str) -> dict[str, object]:
    grouped: dict[tuple[str, str, str, str | None], dict[str, Any]] = {}
    non_null_chassis_groups = {
        (division, level1, level2)
        for division, level1, level2, level3 in rows
        if division not in DERIVED_PLATFORM_DIVISIONS and level3 not in {"NA", "Accessory"}
    }

    for division, level1, level2, level3 in rows:
        source_row = (division, level1, level2, level3)
        if division in DERIVED_PLATFORM_DIVISIONS:
            key = (division, level1, level1, level2)
            item = grouped.setdefault(key, {"variants": []})
            if level3 != "NA":
                item["variants"].append({"variant_id": variant_id(source_row), "label": level3})
            continue

        if level3 == "Accessory":
            continue
        if level3 == "NA" and level2 not in LITERAL_NA_CHASSIS_PLATFORMS:
            if (division, level1, level2) in non_null_chassis_groups:
                continue
            chassis: str | None = None
        else:
            chassis = level3
        grouped.setdefault((division, level1, level2, chassis), {"variants": []})

    paths: list[dict[str, Any]] = []
    ids: set[str] = set()
    variant_ids: set[str] = set()
    for row, extras in grouped.items():
        division, product_lineup, platform, chassis = row
        item_id = taxonomy_id(row)
        if item_id in ids:
            raise ValueError(f"taxonomy_id_collision:{item_id}")
        ids.add(item_id)
        variants = extras["variants"]
        for variant in variants:
            if variant["variant_id"] in variant_ids:
                raise ValueError(f"variant_id_collision:{variant['variant_id']}")
            variant_ids.add(variant["variant_id"])
        display_values = (division, product_lineup, platform, chassis if chassis is not None else "null")
        paths.append(
            {
                "taxonomy_id": item_id,
                "division_code": DIVISION_CODES[division],
                "division": division,
                "product_lineup": product_lineup,
                "platform": platform,
                "chassis": chassis,
                "display_path": " > ".join(display_values),
                "variants": variants,
                "aliases": ["Aircare", "에어케어"] if division == "Air Care" else [],
                "active": True,
            }
        )

    counts = Counter(item["division"] for item in paths)
    return {
        "taxonomy_version": version,
        "source": source,
        "row_count": len(paths),
        "variant_count": sum(len(item["variants"]) for item in paths),
        "division_counts": dict(sorted(counts.items())),
        "division_rules": {
            division: {
                "platform_selection_mode": (
                    "derived_from_product_lineup" if division in DERIVED_PLATFORM_DIVISIONS else "catalog"
                )
            }
            for division in DIVISION_CODES
        },
        "paths": paths,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()

    payload = build_payload(
        clean_rows(read_xlsx_rows(args.input)),
        source=args.input.name,
        version=args.version,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {key: payload[key] for key in ("taxonomy_version", "row_count", "variant_count", "division_counts")},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
