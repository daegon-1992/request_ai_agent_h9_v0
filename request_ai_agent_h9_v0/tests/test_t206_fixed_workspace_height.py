from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_desktop_workspace_fills_available_canvas_without_legacy_reference_height():
    assert '--stage-panel-reference-height' not in HTML_TEMPLATE
    assert 'body{display:grid;grid-template-rows:auto minmax(0,1fr);overflow:hidden}' in HTML_TEMPLATE
    assert 'height:100%;max-height:none;min-height:0;' in HTML_TEMPLATE


def test_form_and_agent_keep_equal_height_with_independent_scroll_regions():
    assert '.workspace-content{height:100%;grid-template-rows:56px 10px minmax(0,1fr);row-gap:0;overflow:visible}' in HTML_TEMPLATE
    assert '.workspace-shell .main{min-height:0;overflow:hidden}' in HTML_TEMPLATE
    assert '.workspace-shell .workspace{height:100%;min-height:0;padding:0;overflow:hidden}' in HTML_TEMPLATE
    assert '.workspace-form > .screen-group:not([hidden]) > .screen-scroll-content{min-height:0;padding:var(--ui-workspace-padding) var(--ui-workspace-padding) 0;overflow-y:auto;overscroll-behavior:contain}' in HTML_TEMPLATE
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


def test_screen_six_uses_the_same_canonical_scroll_hierarchy_as_editing_screens():
    preview_tab = HTML_TEMPLATE.split('<div class="workspace-tab" id="tab-preview"', 1)[1].split('data-shell="AgentDock"', 1)[0]

    assert '<div class="workspace-form">' in preview_tab
    assert '<div class="screen-group" data-screen="SCREEN-06" aria-labelledby="screen06Heading">' in preview_tab
    assert '<div class="screen-scroll-content">' in preview_tab
    assert preview_tab.index('class="screen-group" data-screen="SCREEN-06"') < preview_tab.index('class="screen-scroll-content"')
    assert preview_tab.index('class="screen-scroll-content"') < preview_tab.index('id="section-preview"')
    assert 'class="workspace-form screen-group" data-screen="SCREEN-06"' not in HTML_TEMPLATE
    assert '.workspace-form > .screen-group:not([hidden]) > .screen-scroll-content{min-height:0;padding:var(--ui-workspace-padding) var(--ui-workspace-padding) 0;overflow-y:auto;overscroll-behavior:contain}' in HTML_TEMPLATE
    assert '.workspace-shell .screen-group[data-screen="SCREEN-06"] > .screen-scroll-content > #section-preview{margin-bottom:var(--request-workspace-card-section-gap);border:0;border-radius:0;background:transparent;box-shadow:none;overflow:visible}' in HTML_TEMPLATE
