from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_full_preview_uses_section_titles_without_repeated_table_captions():
    preview = HTML_TEMPLATE.split("function renderDocumentPreviewPanel", 1)[1].split(
        "function renderCandidateNotice", 1
    )[0]

    assert 'section("conditions", "해석 조건"' in preview
    assert '<thead><tr><th></th><th>팬 개수</th><th>팬 회전 설정</th></tr></thead>' in preview
    assert '<th>HEX Type</th><th>관 직경(Pi) / 채널 폭(Width)</th><th>Fin type</th><th>열 수</th><th>FPI / FPDM</th>' in preview
    assert 'class="preview-condition-pair"' in preview
    assert "<caption>해석 대상 제품</caption>" not in preview
    assert "<caption>조건 카드 목록</caption>" not in preview
    assert "<caption>Case Matrix</caption>" not in preview
    assert "조건 카드" not in preview


def test_full_preview_table_cells_do_not_repeat_header_labels():
    preview = HTML_TEMPLATE.split("function renderDocumentPreviewPanel", 1)[1].split(
        "function renderCandidateNotice", 1
    )[0]

    assert 'previewTableValue("팬 회전 설정", setting, display.missing)' in preview
    assert 'previewFieldLabel("팬 회전 설정", display.missing)' not in preview
    assert 'previewTableValue(labels[key] || key, value(fields[key]), isMissing(fields[key]))' in preview
    assert '${previewFieldLabel(labels[key] || key' not in preview


def test_full_preview_uses_product_widths_and_shared_case_matrix_contract():
    preview = HTML_TEMPLATE.split("function renderDocumentPreviewPanel", 1)[1].split(
        "function renderCandidateNotice", 1
    )[0]

    assert '<col class="preview-product-role"><col class="preview-product-drawing"><col class="preview-product-change">' in preview
    assert '.preview-product-role{width:14%}' in HTML_TEMPLATE
    assert '.preview-product-drawing{width:26%}' in HTML_TEMPLATE
    assert '.preview-product-change{width:60%}' in HTML_TEMPLATE
    assert 'class="preview-table case-matrix-grid" data-preview-table="case_matrix"' in preview
    assert 'caseColumnDisplayLabel(row)' in preview
    assert 'caseColumnClass(key)' in preview
    assert 'const matrixSources = caseSelectionSources(state);' in preview
    assert 'caseReadonlyFieldHtml(key, selected, cells[key], matrixSources)' in preview
    assert '<select' not in preview
    assert 'data-action="remove-case"' not in preview


def test_full_preview_only_projects_active_environment_fields():
    preview = HTML_TEMPLATE.split("function renderDocumentPreviewPanel", 1)[1].split(
        "function renderCandidateNotice", 1
    )[0]

    assert 'const groupedConditionBody = type =>' in preview
    assert '.filter(([key]) => Object.prototype.hasOwnProperty.call(fields, key))' in preview
    assert '.map(([key, label]) => kv(label, conditionFieldDisplayWithUnit(type, key, fields[key])))' in preview
    assert 'environmentBody ? `<div><h5>공간 환경 조건</h5>' in preview
    assert 'supplyBody ? `<div><h5>취출 공기 조건</h5>' in preview


def test_full_preview_heat_exchanger_columns_use_balanced_fixed_widths():
    preview = HTML_TEMPLATE.split("function renderDocumentPreviewPanel", 1)[1].split(
        "function renderCandidateNotice", 1
    )[0]

    assert 'class="preview-table preview-specification-table"' in preview
    assert '<col class="preview-spec-name"><col class="preview-spec-type"><col class="preview-spec-dimension"><col class="preview-spec-fin"><col class="preview-spec-rows"><col class="preview-spec-pitch">' in preview
    assert '.preview-spec-name{width:14%}' in HTML_TEMPLATE
    assert ':is(.preview-spec-type,.preview-spec-dimension,.preview-spec-fin){width:22%}' in HTML_TEMPLATE
    assert ':is(.preview-spec-rows,.preview-spec-pitch){width:10%}' in HTML_TEMPLATE
