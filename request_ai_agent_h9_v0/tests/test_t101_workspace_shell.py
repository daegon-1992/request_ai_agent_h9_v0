from __future__ import annotations

import re

from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_visual_foundation_uses_engineering_ui_v3_tokens_and_compatibility_aliases():
    for token in (
        "--ui-content-max:1536px",
        "--ui-page:#FDFDFE",
        "--ui-header:#FFFFFF",
        "--ui-nav-bg:#F6F7F9",
        "--ui-surface:#FFFFFF",
        "--ui-surface-subtle:#F6F7F9",
        "--ui-input-bg:#F8F9FA",
        "--ui-preview-canvas:#CED1D6",
        "--ui-text-primary:#111214",
        "--ui-text-secondary:#50535A",
        "--ui-text-muted:#7A7E86",
        "--ui-border:#D3D6DB",
        "--ui-border-subtle:#E7E9EC",
        "--ui-active:#34373E",
        "--ui-primary:#56595E",
        "--ui-primary-hover:#45484D",
        "--ui-step-inactive:#B8BCC3",
        "--ui-agent-blue:#5F8FEA",
        "--ui-user-bubble:#EDF2F9",
        "--ui-warning-bg:#FEF9EA",
        "--ui-warning-border:#F2D58A",
        "--ui-warning:#F2B447",
        "--ui-warning-text:#7A3B16",
        "--ui-error:#DA1E28",
        "--ui-error-bg:#FFF1F1",
        "--ui-radius-control:7px",
        "--ui-radius-panel:8px",
        "--ui-shadow-paper:0 2px 8px rgba(0,0,0,.08)",
        "--ui-space-1:4px",
        "--ui-space-2:8px",
        "--ui-space-3:12px",
        "--ui-space-4:16px",
        "--ui-space-5:20px",
        "--ui-space-6:24px",
        "--ui-space-7:32px",
    ):
        assert token in HTML_TEMPLATE
    for alias in (
        "--ink:var(--ui-text-primary)",
        "--muted:var(--ui-text-muted)",
        "--bg:var(--ui-page)",
        "--paper:var(--ui-surface)",
        "--soft:var(--ui-surface-subtle)",
        "--line:var(--ui-border-subtle)",
        "--line-strong:var(--ui-border)",
        "--brand-strong:var(--ui-primary)",
        "--accent:var(--ui-active)",
        "--request-workspace-shadow:none",
    ):
        assert alias in HTML_TEMPLATE
    assert "linear-gradient" not in HTML_TEMPLATE
    assert '*{box-sizing:border-box;font-weight:400}' not in HTML_TEMPLATE
    assert 'font-family:"Noto Sans KR","Malgun Gothic","Segoe UI",sans-serif' in HTML_TEMPLATE
    assert 'font-weight:650' not in HTML_TEMPLATE


def test_common_controls_use_v3_radius_primary_and_soft_blue_focus():
    assert 'min-height:40px;\n      border:1px solid var(--ui-border);\n      border-radius:var(--ui-radius-control);' in HTML_TEMPLATE
    assert 'button.primary{border-color:var(--ui-primary);background:var(--ui-primary);color:#fff}' in HTML_TEMPLATE
    assert 'button.primary:hover:not(:disabled){border-color:var(--ui-primary-hover);background:var(--ui-primary-hover)}' in HTML_TEMPLATE
    assert 'button.danger{border-color:var(--ui-error);background:var(--ui-surface);color:var(--ui-error)}' in HTML_TEMPLATE
    assert 'button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible,[tabindex]:focus-visible{border-color:var(--ui-agent-blue);outline:2px solid rgba(95,143,234,.24);outline-offset:1px}' in HTML_TEMPLATE
    assert '.workspace-shell .screen-description{margin:0 0 8px;color:var(--request-workspace-muted);font-size:14px;font-weight:400;line-height:1.45}' in HTML_TEMPLATE


def test_global_shell_moves_request_values_into_portal_header_and_removes_summary_surfaces():
    assert "--global-header-height:60px" in HTML_TEMPLATE
    assert "height:var(--global-header-height);padding:8px 24px" in HTML_TEMPLATE
    assert "min-height:calc(100vh - var(--global-header-height))" in HTML_TEMPLATE
    assert 'class="portal-heading"' in HTML_TEMPLATE
    assert '.brand-mark{\n      width:auto;height:auto;border-radius:0;background:transparent;color:var(--ui-text-primary);' in HTML_TEMPLATE
    assert '.portal-heading{padding-left:16px;border-left:1px solid var(--ui-border-subtle)}' in HTML_TEMPLATE
    assert 'class="header-request-summary" aria-label="현재 의뢰 정보"' in HTML_TEMPLATE
    assert 'class="header-request-title" id="heroTitle"' in HTML_TEMPLATE
    assert 'class="header-request-number" id="requestNoDisplay"' in HTML_TEMPLATE
    assert ".header-request-title{min-width:0;max-width:560px" in HTML_TEMPLATE
    assert "font-size:14px;font-weight:500" in HTML_TEMPLATE
    assert ".header-request-number{flex:0 0 auto" in HTML_TEMPLATE
    assert "font-size:13px;font-weight:400" in HTML_TEMPLATE
    assert 'data-shell="WorkspaceBar"' not in HTML_TEMPLATE
    assert "workspace-title-summary" not in HTML_TEMPLATE
    assert "workspace-number-block" not in HTML_TEMPLATE
    assert "의뢰 제목 (자동 생성)" not in HTML_TEMPLATE
    assert ">의뢰 번호<" not in HTML_TEMPLATE
    assert '.workspace-shell .screen-map-item[aria-current="page"]{background:transparent;color:var(--ui-text-primary)}' in HTML_TEMPLATE
    assert '.workspace-shell .screen-map-item[aria-current="page"] .screen-map-number{background:var(--ui-active);color:#fff}' in HTML_TEMPLATE
    assert "grid-template-columns:minmax(0,2.285fr) 16px minmax(0,1fr)" in HTML_TEMPLATE


def test_workspace_and_agent_follow_v3_surface_hierarchy_without_shell_shadow():
    assert ".workspace-shell .panel.main{" in HTML_TEMPLATE
    assert "border:1px solid var(--ui-border-subtle);border-radius:var(--ui-radius-panel);" in HTML_TEMPLATE
    assert "background:var(--ui-page);box-shadow:none;outline:0" in HTML_TEMPLATE
    assert "background:var(--ui-surface-subtle);" in HTML_TEMPLATE
    assert ".step-navigation{background:transparent}" in HTML_TEMPLATE
    assert "scrollbar-width:thin;background:transparent;box-shadow:none" in HTML_TEMPLATE
    assert ".workspace-shell .workspace{" in HTML_TEMPLATE
    assert ".workspace-content{row-gap:0}" in HTML_TEMPLATE
    assert "padding:16px 18px;border:0;border-radius:0;" in HTML_TEMPLATE
    assert "background:transparent;box-shadow:none" in HTML_TEMPLATE
    assert ".agent-dock{" in HTML_TEMPLATE
    assert "border:1px solid var(--ui-border);border-radius:var(--ui-radius-panel);background:var(--ui-surface);box-shadow:none" in HTML_TEMPLATE
    assert ".chat-head{padding:16px 18px;border-bottom-color:var(--ui-border);background:var(--ui-surface)}" in HTML_TEMPLATE
    assert ".chat-log{padding:18px 16px 20px 12px;background:var(--ui-surface)}" in HTML_TEMPLATE
    assert ".msg.user{border-color:var(--ui-border-subtle);background:var(--ui-user-bubble)}" in HTML_TEMPLATE
    assert ".chat-input{padding:14px;border-top-color:var(--ui-border);background:var(--ui-input-bg)}" in HTML_TEMPLATE
    assert ".panel-resizer::before{width:1px;height:46px;background:#d4d5d5}" in HTML_TEMPLATE
    assert "border-bottom:1px solid var(--ui-border);background:var(--ui-header);box-shadow:none" in HTML_TEMPLATE
    assert ".workspace-shell .workspace-form :is(input,textarea,select):disabled{border-color:var(--ui-disabled-border);background:var(--ui-disabled-bg);color:#9A9EA5;opacity:1}" in HTML_TEMPLATE


def test_guided_workspace_shell_preserves_the_six_screen_map_and_existing_sections():
    expected_screens = (
        ("SCREEN-01", "의뢰 대상·시작", "requestPrepCard"),
        ("SCREEN-02", "요청 내용", "section-basic"),
        ("SCREEN-03", "해석 제품", "section-geometry"),
        ("SCREEN-04", "해석 조건", "section-conditions"),
        ("SCREEN-05", "Case Matrix", "section-case"),
        ("SCREEN-06", "전체 확인", "documentPreviewPanel"),
    )

    positions = []
    for screen, label, marker in expected_screens:
        assert screen in HTML_TEMPLATE
        assert label in HTML_TEMPLATE
        positions.append(HTML_TEMPLATE.index(f'id="{marker}"'))
    assert positions == sorted(positions)

    for wrapper in ("GlobalHeader", "StepNavigation", "MainWorkspace", "AgentDock", "GlobalFooter"):
        assert wrapper in HTML_TEMPLATE
    assert 'class="screen-map"' in HTML_TEMPLATE
    assert 'id="stageRail"' not in HTML_TEMPLATE
    assert 'id="chatLog"' in HTML_TEMPLATE
    assert 'id="chatInput"' in HTML_TEMPLATE
    assert "width:min(100%,1536px);padding:18px 22px 22px" in HTML_TEMPLATE
    assert 'class="app-footer"' in HTML_TEMPLATE


def test_user_facing_screen_text_uses_navigation_names_without_internal_ids():
    navigation = (
        ("SCREEN-01", "01", "의뢰 대상·시작"),
        ("SCREEN-02", "02", "요청 내용"),
        ("SCREEN-03", "03", "해석 제품"),
        ("SCREEN-04", "04", "해석 조건"),
        ("SCREEN-05", "05", "Case Matrix"),
        ("SCREEN-06", "06", "전체 확인"),
    )

    for screen_id, number, label in navigation:
        assert f'data-screen="{screen_id}"' in HTML_TEMPLATE
        assert f'<span class="screen-map-number">{number}</span>' in HTML_TEMPLATE
        assert label in HTML_TEMPLATE

    headings = re.findall(r'<h2 class="screen-heading"[^>]*>(.*?)</h2>', HTML_TEMPLATE, re.DOTALL)
    assert headings and all("SCREEN-" not in heading for heading in headings)
    assert "function userScreenName(screenId)" in HTML_TEMPLATE
    assert "현재 화면: ${active.id}" not in HTML_TEMPLATE
    assert "SCREEN-06 전체 확인은 항상 열 수 있습니다." not in HTML_TEMPLATE


def test_word_cta_is_only_in_the_screen_six_preview_workspace():
    assert HTML_TEMPLATE.count('id="wordExportSlotBtn"') == 1
    screen_six_start = HTML_TEMPLATE.index('data-screen="SCREEN-06"')
    word_cta = HTML_TEMPLATE.index('id="wordExportSlotBtn"')
    assert word_cta > screen_six_start


def test_screen_one_guidance_preserves_copy_and_uses_subtle_emphasis():
    expected_copy = (
        "요청자 소속이 아니라, 해석 대상 제품을 기준으로 선택합니다."
        "제품 분류를 선택한 후 수행할 해석유형을 지정합니다."
    )
    guidance = re.search(
        r'<p class="prep-guidance">(?P<content>.*?)</p>',
        HTML_TEMPLATE,
        flags=re.DOTALL,
    )
    responsive = re.search(
        r"@media \(max-width:1180px\)\{(?P<content>.*?)\n\s*\}",
        HTML_TEMPLATE,
        flags=re.DOTALL,
    )

    assert '<h3 class="visually-hidden">해석 대상 제품 선택</h3>' in HTML_TEMPLATE
    assert 'class="prep-info-icon"' in HTML_TEMPLATE
    assert guidance is not None
    assert re.sub(r"<[^>]+>", "", guidance.group("content")) == expected_copy
    assert HTML_TEMPLATE.count('class="prep-guidance-emphasis"') == 3
    assert 'class="prep-guidance-line prep-guidance-next"' in guidance.group("content")
    assert "border:1px solid var(--line-strong)" in HTML_TEMPLATE
    assert "background:#F7F7F7" in HTML_TEMPLATE
    assert "border-left:2px solid var(--line)" not in HTML_TEMPLATE
    assert ".prep-guidance-line:first-child{color:var(--ink);font-size:15px;font-weight:600;line-height:1.55}" in HTML_TEMPLATE
    assert ".prep-guidance-next{margin-top:4px;color:#55585B;font-size:13px;font-weight:400;line-height:1.55}" in HTML_TEMPLATE
    assert ".prep-guidance-next .prep-guidance-emphasis{color:#55585B;font-weight:400}" in HTML_TEMPLATE
    assert ".prep-guidance-emphasis{color:var(--ink);font-weight:600}" in HTML_TEMPLATE
    assert responsive is not None
    assert ".prep-quick-groups" in responsive.group("content")
    assert "grid-template-columns:1fr" in responsive.group("content")
    assert ".prep-actions{justify-content:flex-start}" in responsive.group("content")


def test_screen_one_uses_single_row_product_classification_and_analysis_detail():
    screen = HTML_TEMPLATE.split('<section class="screen-group" data-screen="SCREEN-01"', 1)[1].split(
        '<section class="screen-group request-content-screen" data-screen="SCREEN-02"', 1
    )[0]
    render = HTML_TEMPLATE.split("function renderRequestPrepCard(){", 1)[1].split(
        "function renderContextChip(){", 1
    )[0]

    assert ">제품 분류</h4>" in screen
    assert ">해석 설정</h4>" in screen
    assert ".prep-quick-group-analysis{padding:24px 0 0;border-top:1px solid var(--ui-border-subtle)}" in HTML_TEMPLATE
    for control_id in (
        "quickDivisionSelect",
        "quickProductLineupSelect",
        "quickPlatformSelect",
        "quickChassisSelect",
        "quickAnalysisTypeSelect",
    ):
        assert f'id="{control_id}"' in screen

    assert "<strong>선택한 내용</strong>" not in screen
    assert 'id="prepSelection"' not in screen
    assert 'id="analysisTypeDetail"' in screen
    assert "선택한 해석유형" in screen
    assert "이런 경우에 적합합니다" in render
    assert "제품의 흡입·토출 또는 관심 위치에서의 풍량을 확인하는 해석입니다." in HTML_TEMPLATE
    assert "제품의 풍량이 충분한지 확인하려는 경우" in HTML_TEMPLATE
    assert 'id="prepStartBtn"' in screen
    assert "grid-template-columns:repeat(4,minmax(0,1fr));gap:12px" in HTML_TEMPLATE
    assert "grid-template-columns:minmax(240px,.38fr) minmax(0,.62fr)" in HTML_TEMPLATE
