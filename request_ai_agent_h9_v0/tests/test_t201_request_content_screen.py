from __future__ import annotations

from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_screen_two_groups_basic_information_and_two_request_detail_fields():
    screen_start = HTML_TEMPLATE.index('class="screen-group request-content-screen" data-screen="SCREEN-02"')
    screen_end = HTML_TEMPLATE.index('data-screen="SCREEN-03"', screen_start)
    screen = HTML_TEMPLATE[screen_start:screen_end]

    assert screen.index('id="section-basic"') < screen.index('id="section-overview"')
    assert 'id="section-request-basic"' in screen
    requester_start = screen.index('id="section-basic"')
    request_basic_start = screen.index('id="section-request-basic"')
    overview_start = screen.index('id="section-overview"')
    requester_section = screen[requester_start:request_basic_start]
    request_basic_section = screen[request_basic_start:overview_start]
    assert 'class="grid request-basic-grid"' in screen
    assert '의뢰자 정보' in requester_section
    assert '의뢰 기본 정보' in request_basic_section
    for path in ('division', 'department', 'requester_name', 'requester_role'):
        assert f'data-path="basic_info.{path}"' in requester_section
        assert f'data-path="basic_info.{path}"' not in request_basic_section
    for key in (
        'request_type', 'project_name', 'development_grade', 'npi_stage', 'model_suffix',
        'desired_completion_date',
    ):
        assert f'data-path="analysis_overview.{key}"' in request_basic_section
    for key in ('request_description', 'additional_result_request'):
        assert f'data-path="analysis_overview.{key}"' in screen
    overview_section = screen[overview_start:]
    assert overview_section.count('<textarea') == 2
    assert 'id="decisionUseSelect"' not in overview_section
    assert '해석 결과 안내' not in overview_section


def test_request_content_layout_uses_three_columns_at_wide_widths():
    assert '.grid.compact{grid-template-columns:repeat(3,minmax(0,1fr))}' in HTML_TEMPLATE


def test_request_content_sections_use_dividers_instead_of_cards():
    assert '.workspace-shell .request-content-screen{background:transparent}' in HTML_TEMPLATE
    assert '.workspace-shell .request-content-screen > .section{margin:0;border:0;border-radius:0;background:transparent;box-shadow:none;overflow:visible}' in HTML_TEMPLATE
    assert '.workspace-shell .request-content-screen > .section + .section{margin-top:24px;padding-top:24px;border-top:1px solid var(--ui-border-subtle)}' in HTML_TEMPLATE
    assert '.workspace-shell .request-content-screen > .section > .section-body{padding:16px 0 0;border-top:0}' in HTML_TEMPLATE
    assert '.workspace-shell .request-content-screen > .section > .section-head{min-height:0;padding:0;background:transparent;border-bottom:0}' in HTML_TEMPLATE


def test_request_content_uses_canonical_heading_and_control_density():
    assert (
        '.workspace-shell .request-content-screen .screen-heading{margin-bottom:8px;'
        'padding:3px 0;font-size:24px;font-weight:600;line-height:1.3;'
        'letter-spacing:-.02em;color:var(--ink)}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .request-content-screen input,.workspace-shell .request-content-screen select{'
        'min-height:46px;padding:10px 12px;border:1px solid var(--line-strong);'
        'border-radius:8px;background-color:var(--paper);color:var(--ink)}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .request-content-screen textarea{min-height:70px;padding:10px 12px;'
        'border:1px solid var(--line-strong);border-radius:8px;background:var(--paper)}'
    ) in HTML_TEMPLATE


def test_request_content_combobox_density_is_scoped_to_screen_two():
    assert (
        '.workspace-shell .request-content-screen .undecided-combobox{height:46px;min-height:46px;'
        'grid-template-columns:minmax(0,1fr) 42px;'
    ) in HTML_TEMPLATE
    assert '.workspace-shell .request-content-screen .undecided-combobox input{height:44px;min-height:44px;' in HTML_TEMPLATE
    assert '.workspace-shell .request-content-screen .undecided-combobox-toggle{width:42px;height:44px;min-height:44px;' in HTML_TEMPLATE
    assert (
        '.workspace-shell .request-content-screen .undecided-combobox input:focus-visible,\n'
        '    .workspace-shell .request-content-screen .undecided-combobox-toggle:focus-visible{'
        'border:0;outline:0;outline-offset:0}'
    ) in HTML_TEMPLATE
    assert (
        '.undecided-combobox{\n      position:relative;min-width:0;height:36px;display:grid;'
        'grid-template-columns:minmax(0,1fr) 36px;'
    ) in HTML_TEMPLATE


def test_request_content_custom_dropdown_restore_button_matches_input_density():
    assert (
        '.prep-custom-control{display:grid;grid-template-columns:minmax(0,1fr) 42px;'
        'gap:6px;align-items:center}'
    ) in HTML_TEMPLATE
    assert (
        '.prep-custom-control button{width:42px;min-width:42px;height:46px;min-height:46px;'
        'padding:0;font-size:18px;line-height:1}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .request-content-screen .dropdown-custom-control{'
        'grid-template-columns:minmax(0,1fr) 42px}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .request-content-screen .dropdown-custom-control > button{'
        'width:42px;min-width:42px;height:46px;min-height:46px}'
    ) in HTML_TEMPLATE


def test_screen_one_fixed_taxonomy_selects_do_not_render_a_restore_action():
    screen_start = HTML_TEMPLATE.index('class="screen-group" data-screen="SCREEN-01"')
    screen_end = HTML_TEMPLATE.index('data-screen="SCREEN-02"', screen_start)
    screen = HTML_TEMPLATE[screen_start:screen_end]

    assert 'data-dropdown-restore-path' not in screen


def test_screen_three_uses_canonical_typography_and_navigation_density():
    assert (
        '.workspace-shell .geometry-screen .screen-heading{margin-bottom:8px;'
        'padding:3px 0;font-size:24px;font-weight:600;line-height:1.3;'
        'letter-spacing:-.02em;color:var(--ink)}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .geometry-screen :is(label,.field-label){'
        'font-family:var(--request-workspace-font);font-size:13px;font-style:normal;'
        'font-weight:500;line-height:1.45;letter-spacing:normal;'
        'color:var(--request-workspace-ink)}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .geometry-screen > .screen-action-bar button{min-height:44px;'
        'padding:0 18px;border-radius:8px}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .geometry-screen > .screen-action-bar button.primary{'
        'font-size:15px;font-weight:600}'
    ) in HTML_TEMPLATE


def test_screen_four_uses_canonical_typography_and_navigation_density():
    assert (
        '.workspace-shell .stage-static-screen[data-screen="SCREEN-04"] '
        '.screen-heading{margin-bottom:8px;padding:3px 0;font-size:24px;'
        'font-weight:600;line-height:1.3;letter-spacing:-.02em;color:var(--ink)}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .stage-static-screen[data-screen="SCREEN-04"] '
        ':is(label,.field-label){font-family:var(--request-workspace-font);font-size:13px;'
        'font-style:normal;font-weight:500;line-height:1.45;letter-spacing:normal;'
        'color:var(--request-workspace-ink)}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .stage-static-screen[data-screen="SCREEN-04"] '
        ':is(input,select,textarea,.analysis-result-guidance){'
        'font-family:var(--request-workspace-font);font-size:14px;font-style:normal;'
        'font-weight:400;line-height:1.45;letter-spacing:normal;'
        'color:var(--request-workspace-ink)}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .stage-static-screen[data-screen="SCREEN-04"] '
        '> .screen-action-bar button{min-height:44px;padding:0 18px;border-radius:8px}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .stage-static-screen[data-screen="SCREEN-04"] '
        '> .screen-action-bar button.primary{font-size:15px;font-weight:600}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .workspace-form[data-screen="SCREEN-06"] .screen-heading{'
        'margin-bottom:8px;padding:3px 0;font-size:24px;font-weight:600;line-height:1.3;'
        'letter-spacing:-.02em;color:var(--ink)}'
    ) in HTML_TEMPLATE


def test_request_content_has_navigation_only_action_bar_without_save_or_preview_work():
    screen_start = HTML_TEMPLATE.index('class="screen-group request-content-screen" data-screen="SCREEN-02"')
    screen_end = HTML_TEMPLATE.index('data-screen="SCREEN-03"', screen_start)
    screen = HTML_TEMPLATE[screen_start:screen_end]

    assert 'class="screen-action-bar"' in screen
    assert 'data-screen-action="SCREEN-01">이전: 의뢰 대상·시작</button>' in screen
    assert 'data-screen-action="SCREEN-03">다음: 해석 제품</button>' in screen
    assert 'navigateScreen(screenAction.dataset.screenAction || "SCREEN-01")' in HTML_TEMPLATE


def test_screen_two_sections_are_always_expanded_and_shell_uses_content_row():
    screen_start = HTML_TEMPLATE.index('class="screen-group request-content-screen" data-screen="SCREEN-02"')
    screen_end = HTML_TEMPLATE.index('data-screen="SCREEN-03"', screen_start)
    screen = HTML_TEMPLATE[screen_start:screen_end]

    assert 'data-toggle-section="section-basic"' not in screen
    assert 'data-toggle-section="section-overview"' not in screen
    assert 'class="section open" id="section-basic"' in screen
    assert 'class="section open" id="section-overview"' in screen
    assert '.request-content-screen .section-body{display:block}' in HTML_TEMPLATE
    assert '.request-content-screen .section-head{cursor:default}' in HTML_TEMPLATE
    assert '.workspace-shell{min-width:0;min-height:0;display:grid;grid-template-rows:minmax(0,1fr);gap:10px;overflow:hidden}' in HTML_TEMPLATE
    assert 'width:min(100%,820px)' not in HTML_TEMPLATE
    assert 'if ($("requestNoDisplay")) $("requestNoDisplay").textContent = requestNo;' in HTML_TEMPLATE
    assert 'if ($("requestNoDisplay")) $("requestNoDisplay").textContent = `해석의뢰 번호: ${requestNo}`;' not in HTML_TEMPLATE
    assert '<span>요청 내용</span></h2>' in screen
    assert '<p class="screen-description">기본정보와 해석 요청 배경, 확인하고 싶은 내용을 작성합니다.</p>' in screen
    assert '.workspace-shell .screen-heading-code{display:none}' in HTML_TEMPLATE


def test_navigation_form_and_agent_use_the_full_layout_row_below_header():
    header = HTML_TEMPLATE[HTML_TEMPLATE.index('<header class="topbar"'):HTML_TEMPLATE.index('</header>')]
    assert 'class="top-actions"' in header
    assert HTML_TEMPLATE.count('id="newRequestBtn"') == 1
    assert HTML_TEMPLATE.count('id="previewSlotBtn"') == 0
    assert HTML_TEMPLATE.count('id="orchestratorPanelToggle"') == 0
    assert '.layout{grid-template-areas:"workspace-content agent";grid-template-rows:minmax(0,1fr)}' in HTML_TEMPLATE
    assert '.workspace-shell{display:contents}' in HTML_TEMPLATE
    assert '.workspace-content{grid-area:workspace-content;min-width:0;min-height:0;display:grid;grid-template-rows:auto auto;gap:10px;overflow:visible}' in HTML_TEMPLATE
    assert '.agent-dock{grid-area:agent;height:100%}' in HTML_TEMPLATE
    assert 'id="agentDock"' in HTML_TEMPLATE
    assert 'id="agentWorkPanel"' not in HTML_TEMPLATE
    assert 'id="orchestratorPanel"' not in HTML_TEMPLATE
    assert 'data-shell="WorkspaceBar"' not in HTML_TEMPLATE
    assert '<nav class="step-navigation" data-shell="StepNavigation"' in HTML_TEMPLATE
    assert '<div class="screen-navigation-status" id="screenNavigationStatus"' in HTML_TEMPLATE


def test_request_content_visual_corrections_use_inline_circle_navigation_and_page_scroll():
    assert 'clip-path:polygon(0 0,calc(100% - 18px)' not in HTML_TEMPLATE
    assert 'clip-path:polygon(0 0,100% 0,100% 100%,0 100%,18px 50%)' not in HTML_TEMPLATE
    assert '.workspace-shell .screen-map-item:not(:first-child){margin-left:-18px}' not in HTML_TEMPLATE
    assert '.workspace-shell .screen-map-item[aria-current="page"] .screen-map-number{background:var(--ui-active);color:#fff}' in HTML_TEMPLATE
    assert '.workspace-shell .screen-map-label{font-size:13px;font-weight:500;line-height:1.25;color:var(--ui-text-secondary)}' in HTML_TEMPLATE
    assert '.workspace{min-height:0;overflow:visible;padding:12px}' in HTML_TEMPLATE
    assert '.workspace-content{grid-area:workspace-content;min-width:0;min-height:0;display:grid;grid-template-rows:auto auto;gap:10px;overflow:visible}' in HTML_TEMPLATE
    assert '.workspace-shell .main{overflow:visible}' in HTML_TEMPLATE


def test_screen_two_request_details_are_two_line_fields_in_two_columns():
    screen_start = HTML_TEMPLATE.index('class="screen-group request-content-screen" data-screen="SCREEN-02"')
    screen_end = HTML_TEMPLATE.index('data-screen="SCREEN-03"', screen_start)
    screen = HTML_TEMPLATE[screen_start:screen_end]

    assert '필수' not in screen
    assert '>선택</span>' not in screen
    assert 'id="meta-basic_info" hidden aria-hidden="true"' in screen
    assert 'id="meta-analysis_overview" hidden aria-hidden="true"' in screen
    assert '의뢰자 정보' in screen
    assert '의뢰 기본 정보' in screen
    assert 'class="grid request-basic-grid"' in screen
    assert 'class="request-basic-divider" aria-hidden="true"' not in screen
    assert 'class="request-detail-grid"' in screen
    assert '.request-detail-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;align-items:start}' in HTML_TEMPLATE
    assert '해석을 요청하게 된 배경<textarea data-path="analysis_overview.request_description" rows="2"' in screen
    assert '해석으로 확인하고 싶은 내용<textarea data-path="analysis_overview.additional_result_request" rows="2"' in screen
    assert screen.count('rows="2"') == 2
    assert '.workspace-shell .request-content-screen > #section-overview{background:var(--request-workspace-surface)}' in HTML_TEMPLATE
    assert '결과 활용 목적' not in screen
    assert '해석 결과 안내' not in screen
    assert '결과에서 더 확인하고 싶은 내용' not in screen


def test_screen_two_uses_divider_sections_and_request_type_two_column_project_layout():
    screen_start = HTML_TEMPLATE.index('class="screen-group request-content-screen" data-screen="SCREEN-02"')
    screen_end = HTML_TEMPLATE.index('data-screen="SCREEN-03"', screen_start)
    screen = HTML_TEMPLATE[screen_start:screen_end]

    assert '.workspace-shell .request-content-screen > .section{margin:0;border:0;border-radius:0;background:transparent;box-shadow:none;overflow:visible}' in HTML_TEMPLATE
    assert '.workspace-shell .request-content-screen > .section + .section{margin-top:24px;padding-top:24px;border-top:1px solid var(--ui-border-subtle)}' in HTML_TEMPLATE
    assert 'class="request-type-field">의뢰 유형<select data-dropdown-path="analysis_overview.request_type"' in screen
    assert 'class="undecided-field request-project-field"' in screen
    assert '.request-type-field{grid-column:span 1}' in HTML_TEMPLATE
    assert '.request-project-field{grid-column:span 2}' in HTML_TEMPLATE
    assert '.request-basic-row2-start{grid-column-start:1}' in HTML_TEMPLATE
    assert 'class="request-basic-row2-start">개발 등급<select data-dropdown-path="analysis_overview.development_grade"' in screen
    assert '의뢰 요청일' not in screen
    assert 'data-path="analysis_overview.request_date"' not in screen


def test_request_type_supports_presets_other_direct_input_and_restore_in_same_slot():
    assert '"analysis_overview.request_type": ["개발 프로젝트","품질 개선","필드 이슈","선행 검토","기타(직접 입력)"]' in HTML_TEMPLATE
    assert 'data-dropdown-custom-path="analysis_overview.request_type"' in HTML_TEMPLATE
    assert 'data-path="analysis_overview.request_type" aria-label="의뢰 유형 직접 입력"' in HTML_TEMPLATE
    assert 'data-dropdown-restore-path="analysis_overview.request_type"' in HTML_TEMPLATE
    assert 'option === "직접 입력" || String(option).includes("(직접 입력)")' in HTML_TEMPLATE


def test_request_type_replaces_request_date_across_active_screen_two_contract():
    from request_ai_agent_h9_v0.constants import ANALYSIS_OVERVIEW_FIELD_DEFS
    from request_ai_agent_h9_v0.form_context import _GENERAL_UI_BINDINGS
    from request_ai_agent_h9_v0.chat_patch import _SET_ALLOWED_PATHS

    overview_keys = {item["key"] for item in ANALYSIS_OVERVIEW_FIELD_DEFS}
    assert "request_type" in overview_keys
    assert "request_date" not in overview_keys
    binding_paths = {row[0] for row in _GENERAL_UI_BINDINGS}
    assert "analysis_overview.request_type" in binding_paths
    assert "analysis_overview.request_date" not in binding_paths
    assert "analysis_overview.request_type" in _SET_ALLOWED_PATHS
    assert "analysis_overview.request_date" not in _SET_ALLOWED_PATHS


def test_screen_six_review_and_word_serializer_include_request_type_not_request_date():
    screen_start = HTML_TEMPLATE.index('class="workspace-tab" id="tab-preview"')
    screen_end = HTML_TEMPLATE.index('class="agent"', screen_start) if 'class="agent"' in HTML_TEMPLATE[screen_start:] else len(HTML_TEMPLATE)
    source = HTML_TEMPLATE[screen_start:screen_end]
    assert 'kv("의뢰 유형", overview.request_type)' in HTML_TEMPLATE
    assert 'kv("의뢰 요청일", overview.request_date)' not in HTML_TEMPLATE
    assert 'function previewDomForWord()' in HTML_TEMPLATE
    assert 'document.querySelector(\'[data-preview-document="current-state"]\')' in HTML_TEMPLATE
    assert 'label:clean(node.textContent)' in HTML_TEMPLATE
    assert "value:clean(row?.querySelector('[data-preview-value]')?.textContent)" in HTML_TEMPLATE
