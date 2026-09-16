from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_screen01_02_title_and_description_contract():
    assert 'font-size:22px;font-weight:600;line-height:1.35;letter-spacing:normal' in HTML_TEMPLATE
    assert 'margin:0 0 26px;color:#525252;font-size:14px;font-weight:400;line-height:1.55' in HTML_TEMPLATE
    assert '해석 대상 제품과 수행할 해석유형을 선택합니다.' in HTML_TEMPLATE
    assert '의뢰 정보와 해석 요청 내용을 입력합니다.' in HTML_TEMPLATE


def test_visible_select_chrome_matches_project_combobox_geometry_without_changing_native_selects():
    select_rule = HTML_TEMPLATE[HTML_TEMPLATE.index('.workspace-shell .workspace-form select{'):]
    select_rule = select_rule[:select_rule.index('    }') + 5]
    assert 'appearance:none;-webkit-appearance:none;height:40px;min-height:40px;padding:0 38px 0 10px;' in select_rule
    assert 'background-position:right 11px center;background-size:16px 16px;' in select_rule
    assert 'font-size:14px;font-weight:500;box-shadow:var(--ui-shadow-control)' in select_rule
    assert '.undecided-combobox-toggle svg{width:16px;height:16px;' in HTML_TEMPLATE
    assert '<select data-dropdown-path=' in HTML_TEMPLATE


def test_model_name_keeps_input_visual_while_undecided_behavior_remains_available():
    assert 'class="undecided-field request-model-field"' in HTML_TEMPLATE
    assert '.request-model-field .undecided-combobox{position:relative;grid-template-columns:minmax(0,1fr)}' in HTML_TEMPLATE
    assert 'opacity:0;pointer-events:none' in HTML_TEMPLATE
    assert '.request-model-field .undecided-combobox:hover .undecided-combobox-toggle' in HTML_TEMPLATE
    assert 'data-undecided-mode="undecided"' in HTML_TEMPLATE


def test_screen01_start_cta_keeps_current_inline_position_and_style():
    assert '.prep-start-actions{display:flex;justify-content:flex-end;margin:20px 0 0;' in HTML_TEMPLATE
    assert '.prep-start-actions .primary{min-width:0;width:auto;height:36px;min-height:36px;' in HTML_TEMPLATE
    assert 'id="prepStartBtn" type="button">의뢰서 작성 시작</button>' in HTML_TEMPLATE
    prep_rule = HTML_TEMPLATE[HTML_TEMPLATE.index('.prep-start-actions{'):HTML_TEMPLATE.index('.prep-custom-control{')]
    assert 'margin-top:auto' not in prep_rule
    assert 'position:sticky' not in prep_rule
    assert 'position:absolute' not in prep_rule


def test_screen02_to_05_actions_use_real_flex_bottom_layout_without_position_hacks():
    assert '.screen-action-bar{display:flex;flex:0 0 auto;justify-content:space-between;gap:10px;margin-top:auto;' in HTML_TEMPLATE
    assert '.workspace-form{height:100%;min-height:0;display:flex;flex-direction:column}' in HTML_TEMPLATE
    assert '.workspace-form > .screen-group:not([hidden]){min-height:100%;display:flex;flex-direction:column}' in HTML_TEMPLATE
    action_rule = HTML_TEMPLATE[HTML_TEMPLATE.index('.screen-action-bar{'):HTML_TEMPLATE.index('/* SCREEN-01~06 workspace-only')]
    for forbidden in ('position:sticky', 'position:absolute', 'position:fixed', 'bottom:-24px', 'margin-left:-24px', 'margin-right:-24px'):
        assert forbidden not in action_rule


def test_screen02_to_05_navigation_buttons_share_one_compact_contract():
    assert '.workspace-shell :is(.screen-action-bar button,.workflow-action-button){min-width:0;width:auto;height:36px;min-height:36px;padding:0 13px;border-radius:6px;font-size:13px;font-weight:600}' in HTML_TEMPLATE
    assert '.workspace-shell :is(.screen-action-bar button.primary,.workflow-action-button.primary){border-color:#2F3033;background:#2F3033;color:#fff}' in HTML_TEMPLATE
    assert '.workspace-shell .screen-action-bar button:not(.primary){border:1px solid #C9CDD3;background:#fff;color:#404348}' in HTML_TEMPLATE


def test_screen02_form_density_matches_approved_contract():
    assert 'column-gap:12px;row-gap:14px;align-items:end' in HTML_TEMPLATE
    assert 'grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;align-items:start' in HTML_TEMPLATE
    assert '.workspace-shell .request-content-screen textarea{min-height:96px;padding:10px 11px;' in HTML_TEMPLATE
    assert '.workspace-shell .request-content-screen .undecided-combobox{height:40px;min-height:40px;' in HTML_TEMPLATE
