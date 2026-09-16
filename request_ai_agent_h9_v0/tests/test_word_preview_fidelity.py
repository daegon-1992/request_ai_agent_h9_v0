from io import BytesIO

import pytest
from docx import Document
from docx.oxml.ns import qn

from request_ai_agent_h9_v0.ui import HTML_TEMPLATE
from request_ai_agent_h9_v0.word_export import build_word_docx


def _preview_payload():
    return {
        "request_title": "HA / RAC / Sample / 유동해석",
        "request_no": "REQ-001",
        "sections": [
            {
                "title": "요청 내용",
                "blocks": [
                    {"type": "field", "label": "의뢰 유형", "value": "신규"},
                    {"type": "field", "label": "프로젝트명(PMS)", "value": "PMS-01"},
                    {"type": "field", "label": "해석을 요청하게 된 배경", "value": "배경 설명"},
                    {"type": "field", "label": "해석으로 확인하고 싶은 내용", "value": "확인 내용"},
                ],
            },
            {
                "title": "해석 조건",
                "blocks": [
                    {"type": "group", "title": "운전 조건"},
                    {
                        "type": "table",
                        "key": "operating_conditions",
                        "headers": ["", "팬 개수", "팬 회전 설정"],
                        "rows": [["운전 1", "2", "모든 팬 동일 · 900 RPM"]],
                    },
                    {"type": "group", "title": "열교환기 사양"},
                    {
                        "type": "table",
                        "key": "heat_exchanger_conditions",
                        "headers": ["", "HEX Type", "관 직경(Pi) / 채널 폭(Width)", "Fin type", "열 수", "FPI / FPDM"],
                        "rows": [["사양 1", "Fin-tube", "7 mm", "Louver", "2", "18"]],
                    },
                ],
            },
        ],
    }


def test_preview_serializer_preserves_condition_headings_and_table_identity():
    serializer = HTML_TEMPLATE.split("function previewDomForWord()", 1)[1].split(
        "async function exportWordFromPreview", 1
    )[0]

    for title in ("운전 조건", "열교환기 사양", "공간 환경 조건", "취출 공기 조건"):
        assert f"<h5 data-preview-group-title>{title}</h5>" in HTML_TEMPLATE
    assert "[data-preview-group-title]" in serializer
    assert '.filter(node => !node.matches(\'[data-preview-label]\') || !node.closest(\'table\'))' in serializer
    assert 'return {type:"group", title:clean(node.textContent)}' in serializer
    assert 'key:clean(node.dataset.previewTable)' in serializer


def test_word_matches_preview_hierarchy_without_synthetic_section_numbers():
    document = Document(BytesIO(build_word_docx(_preview_payload())))
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text]

    assert paragraphs == [
        "해석 의뢰서",
        "요청 내용",
        "해석 조건",
        "운전 조건",
        "열교환기 사양",
    ]
    assert all(not text.startswith(("01  ", "02  ")) for text in paragraphs)


def test_word_uses_preview_colors_borderless_fields_and_fixed_table_ratios():
    document = Document(BytesIO(build_word_docx(_preview_payload())))

    identity_table, field_table, operating_table, specification_table = document.tables
    for table in (identity_table, field_table):
        borders = table._tbl.tblPr.find(qn("w:tblBorders"))
        assert borders is not None
        assert {border.get(qn("w:val")) for border in borders} == {"nil"}

    header_shading = operating_table.rows[0].cells[0]._tc.tcPr.find(qn("w:shd"))
    assert header_shading is not None
    assert header_shading.get(qn("w:fill")) == "F7F8FA"

    operating_widths = [cell.width.cm for cell in operating_table.rows[0].cells]
    specification_widths = [cell.width.cm for cell in specification_table.rows[0].cells]
    assert operating_widths == pytest.approx([3.4, 3.06, 10.54], abs=0.02)
    assert specification_widths == pytest.approx([2.38, 3.74, 3.74, 3.74, 1.7, 1.7], abs=0.02)

    narrative_row = field_table.rows[-1]
    assert len(narrative_row.cells) == 4
    assert narrative_row.cells[0].text == "해석을 요청하게 된 배경\n배경 설명"
    assert narrative_row.cells[2].text == "해석으로 확인하고 싶은 내용\n확인 내용"
