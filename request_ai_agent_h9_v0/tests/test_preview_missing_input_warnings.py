from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def _preview_renderer() -> str:
    return HTML_TEMPLATE.split("function renderDocumentPreviewPanel", 1)[1].split(
        "function renderCandidateNotice", 1
    )[0]


def test_preview_marks_missing_field_labels_with_a_red_warning_icon():
    preview = _preview_renderer()

    assert ".preview-missing-icon" in HTML_TEMPLATE
    assert "color:var(--ui-error)" in HTML_TEMPLATE
    assert 'data-preview-missing="${missing}"' in preview
    assert "previewFieldLabel(label, missing" in preview
    assert 'previewFieldLabel("총조립도 도면번호 (NPDM MCAD)", productDrawingMissing)' in preview
    assert 'previewTableValue("팬 회전 설정", setting, display.missing)' in preview


def test_word_button_shows_required_input_warning_only_for_missing_required_input():
    navigation = HTML_TEMPLATE.split("function renderScreenNavigation", 1)[1].split(
        "function focusScreenHeading", 1
    )[0]

    assert 'id="wordExportRequiredWarning"' in HTML_TEMPLATE
    assert "필수 입력 누락" in HTML_TEMPLATE
    assert "wordRequiredWarning.hidden = firstIncompleteIndex < 0" in navigation
    assert "wordButton.disabled = wordExportInProgress || firstIncompleteIndex >= 0" in navigation


def test_screen_six_uses_flat_read_only_review_sections_and_action_contracts():
    screen_start = HTML_TEMPLATE.index('class="screen-group" data-screen="SCREEN-06"')
    screen_end = HTML_TEMPLATE.index('data-shell="AgentDock"', screen_start)
    screen = HTML_TEMPLATE[screen_start:screen_end]

    assert '<div class="section-title"><h3>의뢰서 미리보기</h3></div>' in screen
    assert 'class="section-title-icon"' not in screen
    assert 'class="title-icon"' in HTML_TEMPLATE[screen_end:]
    assert (
        '.workspace-shell .screen-group[data-screen="SCREEN-06"] > .screen-scroll-content > #section-preview{'
        'margin-bottom:var(--request-workspace-card-section-gap);border:0;border-radius:0;'
        'background:transparent;box-shadow:none;overflow:visible}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-section{'
        'padding:0;border:0;border-radius:0;background:transparent;box-shadow:none}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-section + .preview-section{'
        'margin-top:24px;padding-top:24px;border-top:1px solid var(--ui-border-subtle)}'
    ) in HTML_TEMPLATE
    assert '.preview-review-narrative{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));' in HTML_TEMPLATE
    assert '.preview-condition-pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));' in HTML_TEMPLATE
    assert '.preview-actions{display:flex;align-items:center;justify-content:flex-end;' in HTML_TEMPLATE
    assert (
        '.workspace-shell :is(.screen-action-bar button,.workflow-action-button){'
        'min-width:0;width:auto;height:36px;min-height:36px;padding:0 13px;'
        'border-radius:6px;font-size:13px;font-weight:600}'
    ) in HTML_TEMPLATE
    assert 'class="primary workflow-action-button" id="wordExportSlotBtn"' in screen
    assert '#wordExportSlotBtn{' not in HTML_TEMPLATE


def test_screen_six_keeps_missing_markers_inline_at_semantic_icon_size():
    assert (
        '.workspace-shell .screen-group[data-screen="SCREEN-06"] '
        ':is(.preview-missing-icon,.preview-missing-icon svg){width:14px;height:14px}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .screen-group[data-screen="SCREEN-06"] .preview-missing-icon{'
        'flex:0 0 14px;color:var(--ui-error)}'
    ) in HTML_TEMPLATE
    assert '<span class="preview-missing-icon" aria-hidden="true"><svg' in HTML_TEMPLATE
    assert 'word-export-required-warning' in HTML_TEMPLATE
