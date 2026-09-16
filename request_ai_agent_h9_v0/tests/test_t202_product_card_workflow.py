from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess

from request_ai_agent_h9_v0.geometry_engine import generate_geometry_axis
from request_ai_agent_h9_v0.state import create_initial_state, sanitize_state
from request_ai_agent_h9_v0.ui import HTML_TEMPLATE
from request_ai_agent_h9_v0.validator import validate_state


def test_target_products_render_as_one_geo_row_list_with_focus_recovery():
    assert '<h3>총 조립 형상</h3>' in HTML_TEMPLATE
    assert 'id="productRows"' in HTML_TEMPLATE
    assert 'id="baseProductCard"' not in HTML_TEMPLATE
    assert 'id="comparisonProductCards"' not in HTML_TEMPLATE
    assert 'data-product-role="${comparison ? "comparison" : "base"}"' in HTML_TEMPLATE
    assert 'data-action="add-comparison"' in HTML_TEMPLATE
    assert 'data-action="remove-comparison"' in HTML_TEMPLATE
    assert '${geometryLabel}</div>' in HTML_TEMPLATE
    assert 'window.requestAnimationFrame(() => document.querySelector(focusSelector)?.focus())' in HTML_TEMPLATE
    assert 'values.push({geometry_id:`comparison_${Date.now()}_${values.length + 1}`' in HTML_TEMPLATE
    assert 'const values = [...asArray(state.geometry.comparison_products)];' in HTML_TEMPLATE


def test_product_rows_have_geometry_drawing_description_and_row_actions():
    assert '<span class="field-label" aria-hidden="true"></span><span class="field-label">총조립도 도면번호 (NPDM MCAD)</span><span class="field-label">Base 대비 변경점</span>' in HTML_TEMPLATE
    assert 'aria-readonly="true">기존 형상</div>' in HTML_TEMPLATE
    assert 'data-product-field="description"' in HTML_TEMPLATE
    assert 'placeholder="CAD에 반영된 변경사항"' in HTML_TEMPLATE
    assert 'title="해석 대상 제품 행 추가"' in HTML_TEMPLATE
    assert 'title="해석 대상 제품 행 삭제"' in HTML_TEMPLATE
    assert 'class="primary condition-row-action"' in HTML_TEMPLATE
    assert 'class="condition-row-action remove"' in HTML_TEMPLATE
    assert (
        'const drawingPlaceholder = comparison ? "변경사항이 반영된 총조립도 도면번호" '
        ': "총조립도 도면번호";'
    ) in HTML_TEMPLATE
    assert 'placeholder="${drawingPlaceholder}" pattern="[A-Za-z0-9-]+"' in HTML_TEMPLATE


def test_total_assembly_drawing_guidance_is_shown_without_changing_product_structure():
    screen_start = HTML_TEMPLATE.index('class="screen-group geometry-screen" data-screen="SCREEN-03"')
    screen_end = HTML_TEMPLATE.index('class="screen-group stage-static-screen condition-input-screen" data-screen="SCREEN-04"', screen_start)
    screen = HTML_TEMPLATE[screen_start:screen_end]

    assert '<p class="screen-description">해석 대상 제품의 도면번호와 비교 제품의 Base 대비 차이를 입력합니다.</p>' in screen
    assert '<strong class="geometry-policy-heading">해석은 입력된 총 조립도 CAD 형상을 기준으로 진행합니다.</strong>' in screen
    assert '<p class="geometry-policy-body">형상 변경·조립 변경 등은 CAD에 먼저 반영한 뒤, 변경된 도면번호로 의뢰해 주세요.</p>' in screen
    assert '첫 번째 형상은 Base 제품이며, 추가한 형상은 비교 제품으로 사용됩니다.' not in screen
    assert '각도·위치·부품 구성이 다르면 +로 비교 형상을 추가하세요.' not in screen
    assert 'placeholder="CAD에 반영된 변경사항"' in HTML_TEMPLATE
    assert 'id="geometryDrawingDuplicateWarning"' in screen
    assert screen.index('class="geometry-policy-guidance"') < screen.index('class="product-table"')


def test_target_product_table_uses_v17_case_matrix_visual_language():
    assert (
        '.workspace-shell .geometry-screen > .screen-scroll-content > #section-geometry{margin:0;border:0;border-radius:0;'
        'background:transparent;box-shadow:none;overflow:visible}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .geometry-screen > .screen-scroll-content > #section-geometry > .section-head{'
        'min-height:0;padding:0;background:transparent;border-bottom:0}'
    ) in HTML_TEMPLATE
    assert (
        '.workspace-shell .geometry-screen > .screen-scroll-content > #section-geometry > .section-body{padding:0;border-top:0}'
    ) in HTML_TEMPLATE
    assert '.product-table{display:flex;flex-direction:column;border:1px solid var(--ui-border);border-radius:7px;' in HTML_TEMPLATE
    assert '.product-table .row-list{display:flex;flex-direction:column;gap:0}' in HTML_TEMPLATE
    assert 'grid-template-columns:100px minmax(230px,.9fr) minmax(270px,1.1fr) 56px' in HTML_TEMPLATE
    assert '.product-table-row>*:not(:last-child){border-right:1px solid #EEF0F2}' in HTML_TEMPLATE
    assert '.product-table-head{align-items:stretch;background:#F7F8FA;color:#45484D;font-size:13px;font-weight:500}' in HTML_TEMPLATE
    assert 'product-comparison-card' not in HTML_TEMPLATE


def test_screen_three_column_headers_and_shared_modal_use_canonical_surface_spacing():
    screen_start = HTML_TEMPLATE.index('class="screen-group geometry-screen" data-screen="SCREEN-03"')
    screen_end = HTML_TEMPLATE.index('class="screen-group stage-static-screen condition-input-screen" data-screen="SCREEN-04"', screen_start)
    screen = HTML_TEMPLATE[screen_start:screen_end]
    assert '<span class="field-label">총조립도 도면번호 (NPDM MCAD)</span>' in screen
    assert '<span class="field-label">Base 대비 변경점</span>' in screen
    assert '<span class="product-action-heading" aria-hidden="true"></span>' in screen
    assert '행 작업' not in screen
    assert '.product-table-head .product-action-heading{justify-content:center}' in HTML_TEMPLATE
    assert 'width:min(420px,100%);border:1px solid var(--line);border-radius:10px;' in HTML_TEMPLATE


def test_product_field_names_and_values_use_screen_three_style_levels():
    assert '.screen-heading{margin:0 0 6px;padding:0;font-size:22px;font-weight:600;line-height:1.35;letter-spacing:normal;color:var(--muted)}' in HTML_TEMPLATE
    assert '.workspace-shell .workspace-form :is(label,.field-label){gap:6px;color:var(--ui-field-label);font-size:13px;font-weight:500;line-height:1.45}' in HTML_TEMPLATE
    assert (
        '.workspace-shell .geometry-screen input{min-height:40px;padding:0 10px;background:var(--paper);color:var(--ui-field-value)}'
    ) in HTML_TEMPLATE
    assert '.workspace-shell .geometry-screen .product-geometry-name{min-height:40px;padding:8px 10px}' in HTML_TEMPLATE
    assert '.row-identity{font-size:13px;font-weight:600;line-height:1.45;color:var(--ink)}' in HTML_TEMPLATE
    assert '.workspace-shell .geometry-screen .base-product-description{min-height:40px;padding:8px 10px;font-size:14px;font-weight:400}' in HTML_TEMPLATE
    assert '.workspace-shell .geometry-screen .condition-row-actions{min-height:40px;align-items:center;justify-content:center}' in HTML_TEMPLATE
    assert '.condition-row-action.primary{border-color:#34373E;background:#34373E;color:#fff}' in HTML_TEMPLATE
    assert '.condition-row-action.remove{border-color:#C9CDD3;background:#fff;color:#444}' in HTML_TEMPLATE
    assert 'border:1.5px solid var(--ui-control-border);border-radius:var(--ui-radius-control);box-shadow:var(--ui-shadow-control)' in HTML_TEMPLATE
    assert '.product-table-head{align-items:stretch;background:#F7F8FA;color:#45484D;font-size:13px;font-weight:500}' in HTML_TEMPLATE
    assert '.product-table-row{display:grid;grid-template-columns:100px minmax(230px,.9fr) minmax(270px,1.1fr) 56px;' in HTML_TEMPLATE
    assert '.product-table-row>*{min-width:0;padding:8px 10px;display:flex;align-items:center}' in HTML_TEMPLATE


def test_add_and_remove_collect_current_values_before_mutating_only_selected_row():
    assert 'const products = collectProductCards();' in HTML_TEMPLATE
    assert 'values.splice(index, 1);' in HTML_TEMPLATE
    assert 'reindexProductRows();' in HTML_TEMPLATE
    assert 'display_name:description' in HTML_TEMPLATE
    assert 'difference_from_base:role === "comparison" ? description : ""' in HTML_TEMPLATE


def test_geometry_axis_uses_the_system_geo_row_names():
    state = create_initial_state()
    state["geometry"]["base_product"].update({"drawing_no": "DRAW-A"})
    state["geometry"]["comparison_products"] = [
        {"geometry_id": "comparison_001", "role": "comparison", "drawing_no": "DRAW-B", "difference_from_base": "베인 각도 변경"},
    ]

    axis = generate_geometry_axis(sanitize_state(state))

    assert [item["geometry_label"] for item in axis["geometry_variants"]] == ["Base", "비교 1"]


def test_geometry_issues_target_the_specific_comparison_card_and_required_fields():
    assert 'match(/comparison_products\\[(\\d+)\\]/)' in HTML_TEMPLATE
    assert 'const productRole = indexMatch ? "comparison" : "base";' in HTML_TEMPLATE
    assert 'includes("difference_from_base") ? "description" : "drawing_no"' in HTML_TEMPLATE

    state = create_initial_state()
    state["geometry"]["base_product"].update({"drawing_no": "DRAW-A"})
    state["geometry"]["comparison_products"] = [
        {"geometry_id": "comparison_001", "role": "comparison", "drawing_no": "DRAW-A", "difference_from_base": ""},
    ]
    issues = validate_state(sanitize_state(state))["blocking"]
    duplicate = next(issue for issue in issues if issue["code"] == "geometry.product.drawing_no.duplicate")
    assert duplicate["path"] == "geometry.comparison_products[0].drawing_no"
    assert duplicate["action"] == "Use a different drawing number."
    assert any(issue["code"] == "geometry.comparison.difference.required_missing" and issue["path"] == "geometry.comparison_products[0].difference_from_base" for issue in issues)


def test_duplicate_drawing_validator_issue_controls_product_table_error_message():
    start = HTML_TEMPLATE.index("function caseValidatorState(state=requestState)")
    end = HTML_TEMPLATE.index("function caseDuplicateIssues(state=requestState)", start)
    renderer = HTML_TEMPLATE[start:end]
    script = f"""
const target = {{innerHTML:""}};
const $ = id => id === "geometryDrawingDuplicateWarning" ? target : null;
const asObj = value => value && typeof value === "object" && !Array.isArray(value) ? value : {{}};
const asArray = value => Array.isArray(value) ? value : [];
const contextText = value => String(value ?? "").trim();
let requestState = {{review:{{validator:{{blocking:[{{code:"geometry.product.drawing_no.duplicate"}}]}}}}}};
{renderer}
renderGeometryDrawingDuplicateWarning();
const duplicateHtml = target.innerHTML;
requestState.review.validator.blocking = [{{code:"geometry.product.drawing_no.invalid"}}];
renderGeometryDrawingDuplicateWarning();
process.stdout.write(JSON.stringify({{duplicateHtml, resolvedHtml:target.innerHTML}}));
"""
    result = subprocess.run(
        ["node", "-e", script], capture_output=True, text=True, encoding="utf-8", check=False
    )

    assert result.returncode == 0, result.stderr
    rendered = json.loads(result.stdout)
    assert "오류 · 해석 제품을 확인해 주세요." in rendered["duplicateHtml"]
    assert "이미 입력된 도면번호입니다." in rendered["duplicateHtml"]
    assert "형상이나 조립 상태가 다른 경우에는 다른 도면번호를 입력해 주세요." in rendered["duplicateHtml"]
    assert "필요 시 임시 도면번호를 사용할 수 있습니다." in rendered["duplicateHtml"]
    assert rendered["resolvedHtml"] == ""


def test_screen_three_duplicate_error_uses_shared_feedback_surface_and_blocks_forward_gate():
    feedback_scope = (
        '.workspace-shell :is(.geometry-screen,.stage-static-screen[data-screen="SCREEN-05"],'
        '.screen-group[data-screen="SCREEN-06"]) '
    )
    assert f'{feedback_scope}.case-review-message.error{{border:1px solid var(--ui-error);background:var(--ui-error-bg)}}' in HTML_TEMPLATE
    assert f'{feedback_scope}.case-review-message:empty{{display:none}}' in HTML_TEMPLATE
    assert 'if (screenId === "SCREEN-03" && geometryDrawingDuplicateIssues().length) return $("geometryDrawingDuplicateWarning");' in HTML_TEMPLATE


def test_geometry_is_not_an_accordion_and_drawing_changes_refresh_preview():
    assert 'class="screen-group geometry-screen" data-screen="SCREEN-03"' in HTML_TEMPLATE
    assert '<div class="section-head" data-toggle-section="section-geometry">' not in HTML_TEMPLATE
    assert '.geometry-screen .section-body{display:block}' in HTML_TEMPLATE
    assert 'event.target.matches(\'[data-product-field="drawing_no"]\')' in HTML_TEMPLATE
    assert 'if (event.target.matches(\'[data-product-field="drawing_no"]\')) schedulePreviewRefresh();' in HTML_TEMPLATE
