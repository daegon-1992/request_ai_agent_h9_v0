from __future__ import annotations

from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_step_navigation_stays_in_the_main_workspace_and_keeps_all_six_labels():
    workspace_start = HTML_TEMPLATE.index('<div class="workspace-shell"')
    navigation_start = HTML_TEMPLATE.index('<nav class="step-navigation"', workspace_start)
    agent_start = HTML_TEMPLATE.index('<aside class="panel chat agent-dock"')

    assert navigation_start < agent_start
    for label in (
        "의뢰 대상·시작",
        "요청 내용",
        "해석 제품",
        "해석 조건",
        "Case Matrix",
        "전체 확인",
    ):
        assert label in HTML_TEMPLATE


def test_step_navigation_uses_v3_inline_circles_without_chevrons_or_connectors():
    assert 'grid-template-columns:repeat(6,minmax(0,1fr));gap:0' in HTML_TEMPLATE
    assert 'align-items:center;justify-content:center;gap:8px;min-width:0' in HTML_TEMPLATE
    assert '.step-navigation{background:transparent}' in HTML_TEMPLATE
    assert 'scrollbar-width:thin;background:transparent;box-shadow:none' in HTML_TEMPLATE
    assert 'border:0;border-radius:0' in HTML_TEMPLATE
    assert 'width:32px;height:32px;flex:0 0 32px;display:grid;place-items:center;border-radius:50%' in HTML_TEMPLATE
    assert '.screen-map-item[aria-current="page"] .screen-map-number{background:var(--ui-active);color:#fff}' in HTML_TEMPLATE
    assert '.screen-map-item[aria-current="page"] .screen-map-label{color:var(--ui-text-primary);font-weight:600}' in HTML_TEMPLATE
    assert 'clip-path:polygon(0 0,calc(100% - 18px)' not in HTML_TEMPLATE
    assert 'clip-path:polygon(0 0,100% 0,100% 100%,0 100%,18px 50%)' not in HTML_TEMPLATE
    assert '.workspace-shell .screen-map-item:not(:first-child){margin-left:-18px}' not in HTML_TEMPLATE
    assert '.screen-map-item:nth-child(n+2):not(:last-child)::after{' not in HTML_TEMPLATE
    assert 'content:"›"' not in HTML_TEMPLATE
    assert '@media (max-width:1039px)' in HTML_TEMPLATE
    assert 'position:fixed' in HTML_TEMPLATE


def test_locked_steps_keep_the_existing_surface_and_show_only_a_leading_lock_icon():
    navigation_start = HTML_TEMPLATE.index('<nav class="step-navigation"')
    navigation_end = HTML_TEMPLATE.index('</nav>', navigation_start)
    navigation = HTML_TEMPLATE[navigation_start:navigation_end]
    item_lines = {
        screen_id: next(line for line in navigation.splitlines() if f'data-screen="{screen_id}"' in line)
        for screen_id in ("SCREEN-01", "SCREEN-02", "SCREEN-03", "SCREEN-04", "SCREEN-05", "SCREEN-06")
    }

    for screen_id in ("SCREEN-02", "SCREEN-03", "SCREEN-04", "SCREEN-05"):
        assert 'class="screen-map-lock"' in item_lines[screen_id]
    for screen_id in ("SCREEN-01", "SCREEN-06"):
        assert 'class="screen-map-lock"' not in item_lines[screen_id]

    assert '.screen-map-item[aria-disabled="true"]{cursor:not-allowed}' in HTML_TEMPLATE
    assert '.screen-map-item[aria-disabled="true"] .screen-map-number{background:var(--ui-step-inactive);opacity:.72}' in HTML_TEMPLATE
    assert '.screen-map-item[aria-disabled="true"] .screen-map-label{color:var(--ui-text-muted);opacity:.72}' in HTML_TEMPLATE
    assert '.screen-map-item[aria-disabled="true"] .screen-map-lock{display:grid;opacity:.65}' in HTML_TEMPLATE


def test_requested_headings_omit_icons_while_agent_keeps_its_identity_icon():
    assert 'class="screen-heading title-with-icon" id="screen01Heading"' not in HTML_TEMPLATE
    assert 'class="screen-heading title-with-icon" id="screen02Heading"' not in HTML_TEMPLATE
    assert 'id="agentDockHeading" class="title-with-icon"' in HTML_TEMPLATE
    assert 'aria-hidden="true"><svg viewBox="0 0 24 24">' in HTML_TEMPLATE


def test_completed_steps_use_muted_green_check_without_changing_navigation_spacing():
    assert '--ui-step-complete:#79B88A' in HTML_TEMPLATE
    assert '.screen-map-item[data-completed="true"] .screen-map-number{background:var(--ui-step-complete);color:#fff;font-size:16px}' in HTML_TEMPLATE
    assert 'data-step-number="01"' in HTML_TEMPLATE
    assert 'numberNode.textContent = completed ? "✓" : contextText(item.dataset.stepNumber)' in HTML_TEMPLATE
    assert 'screen?.id === "SCREEN-06"' in HTML_TEMPLATE
    assert 'finalSubmissionCompleted()' in HTML_TEMPLATE
    assert 'submission.status === "OK" && submission.can_submit === true' in HTML_TEMPLATE
    assert 'screenIndex < screenOrder.findIndex(candidate => candidate.id === active.id)' in HTML_TEMPLATE
    assert '&& !blocked && !missingRequiredControl(screen.id) && !blockingScreenError(screen.id)' in HTML_TEMPLATE
    assert 'item.dataset.completed = String(completed)' in HTML_TEMPLATE
    assert '.screen-map-item[aria-current="page"]:not([data-completed="true"]) .screen-map-number{background:var(--ui-active);color:#fff;font-size:13px}' in HTML_TEMPLATE
    assert 'grid-template-columns:repeat(6,minmax(0,1fr));gap:0' in HTML_TEMPLATE
