from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_main_panel_has_single_workspace_row_for_bottom_flex_actions():
    assert '.main{display:grid;grid-template-rows:minmax(0,1fr)}' in HTML_TEMPLATE
    assert '.main{display:grid;grid-template-rows:auto minmax(0,1fr)}' not in HTML_TEMPLATE
    assert '.screen-action-bar{display:flex;flex:0 0 auto;justify-content:space-between;gap:10px;margin-top:auto;' in HTML_TEMPLATE
    assert '.workspace-form > .screen-group:not([hidden]){min-height:100%;display:flex;flex-direction:column}' in HTML_TEMPLATE
