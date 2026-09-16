from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_screens_two_through_five_keep_actions_outside_scroll_content():
    for screen in ("SCREEN-02", "SCREEN-03", "SCREEN-04", "SCREEN-05"):
        start = HTML_TEMPLATE.index(f'data-screen="{screen}" aria-labelledby=')
        action = HTML_TEMPLATE.index('screen-action-bar', start)
        screen_html = HTML_TEMPLATE[start:action]
        assert '<div class="screen-scroll-content">' in screen_html
        assert screen_html.rfind('</div>') > screen_html.index('<div class="screen-scroll-content">')

    assert '.workspace-shell .workspace{height:100%;min-height:0;padding:0;overflow:hidden}' in HTML_TEMPLATE
    assert 'grid-template-rows:minmax(0,1fr) auto' in HTML_TEMPLATE
    assert '.workspace-form > .screen-group:not([hidden]) > .screen-scroll-content{min-height:0;padding:var(--ui-workspace-padding) var(--ui-workspace-padding) 0;overflow-y:auto;overscroll-behavior:contain}' in HTML_TEMPLATE


def test_fixed_action_architecture_does_not_use_positioning_hacks():
    assert 'screen-scroll-content{min-height:0;padding:var(--ui-workspace-padding) var(--ui-workspace-padding) 0;overflow-y:auto;overscroll-behavior:contain}' in HTML_TEMPLATE
    assert 'screen-scroll-content{position:sticky' not in HTML_TEMPLATE
    assert 'screen-scroll-content{position:absolute' not in HTML_TEMPLATE
    assert 'screen-scroll-content{position:fixed' not in HTML_TEMPLATE


def test_screen_one_keeps_its_existing_cta_architecture():
    start = HTML_TEMPLATE.index('data-screen="SCREEN-01" aria-labelledby=')
    end = HTML_TEMPLATE.index('data-screen="SCREEN-02" aria-labelledby=', start)
    assert 'screen-scroll-content' not in HTML_TEMPLATE[start:end]


def test_desktop_scroll_viewport_owns_the_workspace_edge_without_geometry_hacks():
    assert '.workspace-form > .screen-group[data-screen="SCREEN-01"]:not([hidden]){padding:var(--ui-workspace-padding)}' in HTML_TEMPLATE
    assert '.workspace-tab#tab-preview.active{padding:var(--ui-workspace-padding)}' not in HTML_TEMPLATE
    assert '.workspace-form > .screen-group:not([hidden]) > .screen-scroll-content{min-height:0;padding:var(--ui-workspace-padding) var(--ui-workspace-padding) 0;overflow-y:auto;overscroll-behavior:contain}' in HTML_TEMPLATE
    assert '.workspace-form > .screen-group:not([hidden]) > .screen-action-bar{flex:0 0 auto;margin:0 var(--ui-workspace-padding) var(--ui-workspace-padding)}' in HTML_TEMPLATE
    assert 'width:calc(100% + var(--ui-workspace-padding))' not in HTML_TEMPLATE
    assert 'margin-right:calc(-1 * var(--ui-workspace-padding))' not in HTML_TEMPLATE
    assert 'right:calc(-1 * var(--ui-workspace-padding))' not in HTML_TEMPLATE
