from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_v17_agent_header_uses_icon_only_actions_without_changing_hooks():
    assert 'id="agentClearBtn"' in HTML_TEMPLATE
    assert 'aria-label="대화창 비우기"' in HTML_TEMPLATE
    assert 'id="agentHideBtn"' in HTML_TEMPLATE
    assert 'aria-label="Agent 숨기기"' in HTML_TEMPLATE
    assert '.chat-head-actions button svg{' in HTML_TEMPLATE
    assert '>대화창 비우기</button>' not in HTML_TEMPLATE
    assert '>Agent 숨기기</button>' not in HTML_TEMPLATE


def test_v17_removes_legacy_global_footer_from_dom():
    assert 'data-shell="GlobalFooter"' not in HTML_TEMPLATE
    assert 'class="app-footer"' not in HTML_TEMPLATE
    assert '개인정보처리방침' not in HTML_TEMPLATE
    assert '이용약관' not in HTML_TEMPLATE
    assert '시스템 문의' not in HTML_TEMPLATE
