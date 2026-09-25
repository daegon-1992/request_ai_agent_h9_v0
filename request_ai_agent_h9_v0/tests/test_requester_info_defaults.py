from __future__ import annotations

from request_ai_agent_h9_v0.state import create_initial_state, field_value
from request_ai_agent_h9_v0.ui import HTML_TEMPLATE


def test_requester_information_starts_blank_with_clear_control_guidance():
    state = create_initial_state()

    assert {
        key: field_value(state["basic_info"][key])
        for key in ("division", "department", "requester_name", "requester_role")
    } == {
        "division": "",
        "department": "",
        "requester_name": "",
        "requester_role": "",
    }
    assert '<input data-path="basic_info.department" placeholder="부서를 입력하세요"' in HTML_TEMPLATE
    assert '<input data-path="basic_info.requester_name" placeholder="성함을 입력하세요"' in HTML_TEMPLATE
    assert '<option value="" disabled hidden>선택</option>' in HTML_TEMPLATE
