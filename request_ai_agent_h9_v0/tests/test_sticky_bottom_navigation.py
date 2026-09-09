from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_step_navigation_actions_stay_at_the_bottom_of_the_form_workspace():
    assert '.screen-action-bar{position:sticky;z-index:5;bottom:-6px;' in HTML_TEMPLATE
    assert 'margin-top:auto;padding:12px 0;border-top:1px solid var(--ui-border-subtle);background:var(--ui-surface)' in HTML_TEMPLATE
    assert '.workspace-form > .screen-group:not([hidden]){min-height:100%;display:flex;flex-direction:column}' in HTML_TEMPLATE
    assert '.workspace-form > .screen-group:not([hidden]) > .screen-action-bar{flex:0 0 auto}' in HTML_TEMPLATE
    assert '.workspace-shell .workspace{height:100%;min-height:0;overflow-y:auto;overscroll-behavior:contain}' in HTML_TEMPLATE
