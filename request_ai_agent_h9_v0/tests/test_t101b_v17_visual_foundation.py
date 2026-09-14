from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_canonical_visual_foundation_contract():
    for token in (
        "--ui-content-max:1400px",
        "--ui-agent-width:390px",
        "--ui-agent-width-compact:360px",
        "--ui-panel-split:14px",
        "--ui-workspace-padding:24px",
        "--ui-control-border:#BFC4CB",
        "--ui-field-label:#34373E",
        "--ui-field-value:#242629",
        "--ui-agent-surface:#F8F9FA",
        "--ui-shadow-panel:0 1px 2px rgba(17,24,39,.04),0 5px 14px rgba(17,24,39,.045)",
        "--ui-shadow-header:0 1px 2px rgba(17,24,39,.035),0 3px 8px rgba(17,24,39,.035)",
    ):
        assert token in HTML_TEMPLATE
    assert "--v17-workspace-max" not in HTML_TEMPLATE


def test_desktop_shell_uses_canonical_navigation_panel_and_agent_geometry():
    assert 'width:min(calc(100% - 48px),var(--ui-content-max));padding:10px 0 16px' in HTML_TEMPLATE
    assert 'grid-template-columns:minmax(0,1fr) var(--ui-panel-split) var(--ui-agent-width)' in HTML_TEMPLATE
    assert 'grid-template-rows:56px 10px minmax(0,1fr);row-gap:0' in HTML_TEMPLATE
    assert '.workspace-shell .panel.main{grid-row:3}' in HTML_TEMPLATE
    assert '.workspace-shell .workspace{height:100%;min-height:0;overflow-y:auto;overscroll-behavior:contain}' in HTML_TEMPLATE
    assert '.chat-log{min-height:0;overflow-y:auto;overscroll-behavior:contain}' in HTML_TEMPLATE


def test_desktop_canvas_uses_full_available_height_without_legacy_footer():
    assert 'body{display:grid;grid-template-rows:auto minmax(0,1fr);overflow:hidden}' in HTML_TEMPLATE
    assert '.layout{\n        height:100%;max-height:none;min-height:0;' in HTML_TEMPLATE
    assert 'class="app-footer"' not in HTML_TEMPLATE
