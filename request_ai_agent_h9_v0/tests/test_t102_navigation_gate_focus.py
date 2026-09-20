from __future__ import annotations

from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_six_screen_navigation_has_gate_focus_and_screen_six_for_review():
    assert 'const screenOrder = [' in HTML_TEMPLATE
    assert 'function navigateScreen(screenId, options={})' in HTML_TEMPLATE
    assert 'function renderScreenNavigation()' in HTML_TEMPLATE
    assert 'function focusScreenHeading(screen)' in HTML_TEMPLATE
    assert 'aria-current' in HTML_TEMPLATE
    assert HTML_TEMPLATE.count('id="previewSlotBtn"') == 0
    assert 'data-screen="SCREEN-06"' in HTML_TEMPLATE


def test_navigation_blocks_incomplete_required_inputs_without_collecting_or_refreshing_state():
    start = HTML_TEMPLATE.index('function navigateScreen(screenId, options={})')
    end = HTML_TEMPLATE.index('function valuesFromRows(selector)', start)
    navigation = HTML_TEMPLATE[start:end]
    assert 'screen.requiresContext && !isContextLocked()' in navigation
    assert 'screen.id !== "SCREEN-06"' not in navigation
    assert 'targetIndex > currentIndex' in navigation
    assert 'focusRequiredControl(first.screen, first.control)' in navigation
    assert 'SCREEN-01' in navigation
    assert 'collectState(' not in navigation
    assert 'refreshPreview(' not in navigation
    assert 'postState(' not in navigation


def test_navigation_locks_only_steps_after_the_first_incomplete_screen():
    start = HTML_TEMPLATE.index('function renderScreenNavigation()')
    end = HTML_TEMPLATE.index('function focusScreenHeading(screen)', start)
    navigation = HTML_TEMPLATE[start:end]

    assert 'const firstIncomplete = firstIncompleteScreenBefore(reviewScreen)' in navigation
    assert 'screenIndex > firstIncompleteIndex' in navigation
    assert '!!screen?.requiresContext' in navigation
    assert '{id:"SCREEN-06", headingId:"screen06Heading", tab:"preview", requiresContext:true}' in HTML_TEMPLATE
    assert 'renderScreenNavigation();\n      orchestratorPanelState.dirty = true;' in HTML_TEMPLATE


def test_screen_six_uses_the_same_required_input_gate_as_other_forward_steps():
    start = HTML_TEMPLATE.index('function navigateScreen(screenId, options={})')
    end = HTML_TEMPLATE.index('function valuesFromRows(selector)', start)
    navigation = HTML_TEMPLATE[start:end]

    assert 'screen.id !== "SCREEN-06"' not in navigation
    assert 'if (!options.bypassRequiredGate && targetIndex > currentIndex)' in navigation
    assert '{id:"SCREEN-06", headingId:"screen06Heading", tab:"preview", requiresContext:true}' in HTML_TEMPLATE


def test_navigation_required_gate_lists_each_screen_and_focuses_first_missing_control():
    assert 'function missingRequiredControl(screenId)' in HTML_TEMPLATE
    assert 'function blockingScreenError(screenId)' in HTML_TEMPLATE
    assert 'function firstIncompleteScreenBefore(targetScreen)' in HTML_TEMPLATE
    for screen_id in ("SCREEN-01", "SCREEN-02", "SCREEN-03", "SCREEN-04", "SCREEN-05"):
        assert f'screenId === "{screen_id}"' in HTML_TEMPLATE
    assert 'target?.focus?.({preventScroll:true});' in HTML_TEMPLATE
    assert 'if (!isError && control && target) {' in HTML_TEMPLATE
    assert 'else target.classList.add("required-field-highlight");' in HTML_TEMPLATE
    assert 'missingRequiredControl(screen.id) || blockingScreenError(screen.id)' in HTML_TEMPLATE
    assert 'screenId === "SCREEN-03" && geometryDrawingDuplicateIssues().length' in HTML_TEMPLATE
    assert 'screenId === "SCREEN-05" && caseConfigurationIssues().length' in HTML_TEMPLATE
    assert '의 오류를 수정한 뒤 다음 단계로 이동할 수 있습니다.' in HTML_TEMPLATE


def test_screen_one_missing_context_focuses_a_red_required_control_without_agent_chat():
    start = HTML_TEMPLATE.index('async function confirmRequestContext()')
    end = HTML_TEMPLATE.index('async function updateOperationMode', start)
    confirmation = HTML_TEMPLATE[start:end]

    assert 'focusRequiredControl(screen, control);' in confirmation
    assert 'control.querySelectorAll("button[data-analysis-scope]").forEach(button => button.classList.add("required-field-highlight"));' in confirmation
    assert 'window.setTimeout(() => control.classList.remove("required-field-highlight"), 1800);' not in confirmation
    assert 'pushMessage(' not in confirmation
    assert '.required-field-highlight{outline:0;border-color:#E7A1A1;box-shadow:' in HTML_TEMPLATE
    assert '.required-field-highlight:focus-visible{border-color:#E7A1A1;outline:0;box-shadow:' in HTML_TEMPLATE
    assert 'return $("analysisScopeField");' in HTML_TEMPLATE
    assert '.analysis-scope-field .direct-choice button.required-field-highlight{border-color:#E7A1A1;box-shadow:' in HTML_TEMPLATE
    assert 'const focusTarget = target?.id === "analysisScopeField"' in HTML_TEMPLATE
    assert 'event.target.classList.remove("required-field-highlight");' in HTML_TEMPLATE
    assert 'document.querySelectorAll("#analysisScopeField .required-field-highlight").forEach(control => control.classList.remove("required-field-highlight"));' in HTML_TEMPLATE
    assert 'function focusConditionValidationIssue(issue)' in HTML_TEMPLATE
    assert 'control.classList.add("required-field-highlight");' in HTML_TEMPLATE
    assert 'function focusCaseValidationIssue(issue)' in HTML_TEMPLATE
    assert 'target.classList.add("required-field-highlight");' in HTML_TEMPLATE


def test_screen_navigation_marks_current_screen_and_supports_keyboard_activation():
    assert '.screen-map-item[data-screen]' in HTML_TEMPLATE
    assert 'item.setAttribute("aria-current", screen?.id === active.id ? "page" : "false")' in HTML_TEMPLATE
    assert 'event.key !== "Enter" && event.key !== " "' in HTML_TEMPLATE


def test_word_generation_is_disabled_and_guarded_while_required_inputs_are_incomplete():
    assert 'wordButton.disabled = wordExportInProgress || firstIncompleteIndex >= 0' in HTML_TEMPLATE
    assert '필수 입력을 완료하면 의뢰서를 생성할 수 있습니다.' in HTML_TEMPLATE
    export_start = HTML_TEMPLATE.index('async function exportWordFromPreview({useExistingPreviewDom=false}={})')
    export_end = HTML_TEMPLATE.index('function mutateRows(listName, action, index)', export_start)
    export_action = HTML_TEMPLATE[export_start:export_end]
    assert 'const firstIncomplete = firstIncompleteScreenBefore(reviewScreen)' in export_action
    assert 'focusRequiredControl(firstIncomplete.screen, firstIncomplete.control)' in export_action
    assert 'return false;' in export_action
