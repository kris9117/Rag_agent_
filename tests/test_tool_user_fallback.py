from app.agent.graph import tool_node


def test_password_reset_uses_state_user_id():
    state = {
        "query": "How do I reset my corporate password?",
        "intent": "PASSWORD_RESET",
        "entities": {},
        "user_id": "EMP0001",
        "tool_calls": [],
        "tool_results": [],
        "validation_errors": [],
        "response": None,
        "status": None,
    }

    result = tool_node(state)

    assert result["status"] == "TOOL_COMPLETED"
    assert result["tool_calls"][0]["tool_name"] == "PASSWORD_RESET"
    assert (
        result["tool_calls"][0]["arguments"]["user_id"]
        == "EMP0001"
    )