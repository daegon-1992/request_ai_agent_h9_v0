from __future__ import annotations

from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_screen_six_uses_final_review_labels_and_the_existing_review_actions():
    assert '<span>최종 검토</span>' in HTML_TEMPLATE
    assert '제출하기 전에 작성한 해석 의뢰 내용을 최종 확인합니다.' in HTML_TEMPLATE
    assert '다음: 최종 검토' in HTML_TEMPLATE
    assert 'id="wordExportSlotBtn"' in HTML_TEMPLATE


def test_global_preview_modal_reuses_the_review_renderer_without_word_action():
    modal_start = HTML_TEMPLATE.index('id="requestPreviewModal"')
    modal_end = HTML_TEMPLATE.index('</div>\n\n  <script>', modal_start)
    modal = HTML_TEMPLATE[modal_start:modal_end]
    renderer_start = HTML_TEMPLATE.index('function renderDocumentPreviewPanel(sourceState, previewReceipt, targetPanel)')
    renderer_end = HTML_TEMPLATE.index('function defaultChatHistory()', renderer_start)
    renderer = HTML_TEMPLATE[renderer_start:renderer_end]

    assert 'id="requestPreviewBtn"' in HTML_TEMPLATE
    assert 'id="requestPreviewModalPanel"' in modal
    assert 'id="requestPreviewModalCoverageWarning"' in modal
    assert 'wordExportSlotBtn' not in modal
    assert 'const panel = targetPanel || $("documentPreviewPanel");' in renderer
    assert 'renderDocumentPreviewPanel(requestState, undefined, panel);' in renderer
    assert 'const compactMissingPresentation = panel === $("requestPreviewModalPanel");' in renderer
    assert 'missing && compactMissingPresentation ? "미입력" : text' in renderer
    assert 'renderCompactPreviewCaseMatrixStatus(state, $("requestPreviewModalCoverageWarning"));' in renderer
    assert 'request-preview-case-errors' in HTML_TEMPLATE


def test_preview_open_close_keeps_workflow_navigation_untouched():
    open_start = HTML_TEMPLATE.index('function openRequestPreview()')
    close_start = HTML_TEMPLATE.index('function closeRequestPreview()', open_start)
    close_end = HTML_TEMPLATE.index('function defaultChatHistory()', close_start)
    opener = HTML_TEMPLATE[open_start:close_start]
    closer = HTML_TEMPLATE[close_start:close_end]

    assert 'requestState = collectState();' in opener
    assert 'modal.hidden = false;' in opener
    assert 'activeScreen' not in opener
    assert 'modal.hidden = true;' in closer
    assert 'activeScreen' not in closer
    assert '$("requestPreviewBtn")?.focus();' in closer
