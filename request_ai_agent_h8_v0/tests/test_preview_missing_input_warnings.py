from request_ai_agent_h8_v0.ui import HTML_TEMPLATE


def _preview_renderer() -> str:
    return HTML_TEMPLATE.split("function renderDocumentPreviewPanel", 1)[1].split(
        "function renderCandidateNotice", 1
    )[0]


def test_preview_marks_missing_field_labels_with_a_red_warning_icon():
    preview = _preview_renderer()

    assert ".preview-missing-icon" in HTML_TEMPLATE
    assert "color:#c62828" in HTML_TEMPLATE
    assert 'data-preview-missing="${missing}"' in preview
    assert "previewFieldLabel(label, missing" in preview
    assert 'previewFieldLabel("도면번호 (NPDM MCAD)", productDrawingMissing)' in preview
    assert 'previewFieldLabel("팬 회전수(RPM)", fanDisplay.missing)' in preview


def test_word_button_shows_required_input_warning_only_for_missing_required_input():
    navigation = HTML_TEMPLATE.split("function renderScreenNavigation", 1)[1].split(
        "function focusScreenHeading", 1
    )[0]

    assert 'id="wordExportRequiredWarning"' in HTML_TEMPLATE
    assert "필수 입력 누락" in HTML_TEMPLATE
    assert "wordRequiredWarning.hidden = firstIncompleteIndex < 0" in navigation
    assert "wordButton.disabled = wordExportInProgress || firstIncompleteIndex >= 0" in navigation
