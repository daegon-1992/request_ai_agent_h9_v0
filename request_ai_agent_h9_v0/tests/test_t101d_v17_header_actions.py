from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_header_typography_uses_canonical_contract():
    assert 'font-size:17px;font-weight:700;letter-spacing:normal;' in HTML_TEMPLATE
    assert '.portal-heading h1{display:inline;font-size:16px;font-weight:600;letter-spacing:normal;vertical-align:middle}' in HTML_TEMPLATE
    assert 'color:#525252;font-size:12px;font-weight:400;line-height:1.35' in HTML_TEMPLATE
    assert 'color:#8A8A8A;font-size:11px;font-weight:400;line-height:1.35' in HTML_TEMPLATE


def test_shared_primary_action_colors_are_charcoal():
    assert '.top-actions #newRequestBtn{height:36px;min-height:36px;padding:0 15px;border:0;border-radius:6px;background:#34373E;color:#fff;font-size:13px;font-weight:600}' in HTML_TEMPLATE
    assert '.workspace-shell .screen-action-bar button.primary{border-color:#2F3033;background:#2F3033;color:#fff}' in HTML_TEMPLATE
    assert '.workspace-shell .screen-action-bar button:not(.primary){border:1px solid #C9CDD3;background:#fff;color:#404348}' in HTML_TEMPLATE
