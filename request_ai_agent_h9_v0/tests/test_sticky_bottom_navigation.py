from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_step_navigation_actions_use_flex_bottom_layout_without_position_hacks():
    assert '.screen-action-bar{display:flex;flex:0 0 auto;justify-content:space-between;gap:10px;margin-top:auto;' in HTML_TEMPLATE
    assert '.workspace-form{height:100%;min-height:0;display:flex;flex-direction:column}' in HTML_TEMPLATE
    assert '.workspace-form > .screen-group:not([hidden]){min-height:100%;display:flex;flex-direction:column}' in HTML_TEMPLATE
    action_rule = HTML_TEMPLATE[HTML_TEMPLATE.index('.screen-action-bar{'):HTML_TEMPLATE.index('/* SCREEN-01~06 workspace-only')]
    for forbidden in ('position:sticky', 'position:absolute', 'position:fixed', 'bottom:-24px'):
        assert forbidden not in action_rule
