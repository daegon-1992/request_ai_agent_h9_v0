from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_desktop_workspace_fills_available_canvas_without_legacy_reference_height():
    assert '--stage-panel-reference-height' not in HTML_TEMPLATE
    assert 'body{display:grid;grid-template-rows:auto minmax(0,1fr);overflow:hidden}' in HTML_TEMPLATE
    assert 'height:100%;max-height:none;min-height:0;' in HTML_TEMPLATE


def test_form_and_agent_keep_equal_height_with_independent_scroll_regions():
    assert '.workspace-content{height:100%;grid-template-rows:56px 10px minmax(0,1fr);row-gap:0;overflow:hidden}' in HTML_TEMPLATE
    assert '.workspace-shell .main{min-height:0;overflow:hidden}' in HTML_TEMPLATE
    assert '.workspace-shell .workspace{height:100%;min-height:0;overflow-y:auto;overscroll-behavior:contain}' in HTML_TEMPLATE
    assert '.agent-dock{grid-area:agent;height:100%;min-width:0;' in HTML_TEMPLATE
    assert '.chat-log{min-height:0;overflow-y:auto;overscroll-behavior:contain}' in HTML_TEMPLATE
    assert '.chat-input{position:relative;z-index:1}' in HTML_TEMPLATE


def test_existing_mobile_page_scroll_fallback_is_preserved():
    assert '@media (max-width:1039px)' in HTML_TEMPLATE
    assert 'body{overflow:auto;overflow-x:hidden}' in HTML_TEMPLATE


def test_desktop_screen_one_uses_approved_workspace_spacing():
    assert '--ui-workspace-padding:24px' in HTML_TEMPLATE
    assert '--ui-workspace-padding:24px' in HTML_TEMPLATE
    assert 'padding:var(--ui-workspace-padding)' in HTML_TEMPLATE
    assert '.prep-start-actions{display:flex;justify-content:flex-end;margin:20px 0 0;' in HTML_TEMPLATE
