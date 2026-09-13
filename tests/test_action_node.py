from app.agent.graph import action_node


def base_state():
    return {
        "query": "Create a software ticket",
        "user_id": "EMP0001",
        "entities": {},
        "tool_calls": [],
        "tool_results": [],
        "validation_errors": [],
        "response": None,
        "status": None,
    }


def test_create_ticket_success():
    state = base_state()
    state["entities"] = {
        "category": "Software",
        "priority": "Medium",
        "description": "Outlook is crashing repeatedly",
    }

    result = action_node(state)

    assert result["status"] == "ACTION_COMPLETED"
    assert result["tool_results"][0]["success"] is True
    assert result["tool_results"][0]["result"]["created"] is True


def test_create_ticket_missing_description():
    state = base_state()
    state["entities"] = {
        "category": "Software",
        "priority": "medium",
    }

    result = action_node(state)

    assert result["status"] == "CLARIFICATION_REQUIRED"
    assert "description" in result["response"].lower()


def test_create_ticket_missing_category():
    state = base_state()
    state["entities"] = {
        "priority": "medium",
        "description": "Outlook is crashing",
    }

    result = action_node(state)

    assert result["status"] == "CLARIFICATION_REQUIRED"
    assert "category" in result["response"].lower()


def test_create_ticket_invalid_priority():
    state = base_state()
    state["entities"] = {
        "category": "Software",
        "priority": "urgent",
        "description": "Outlook is crashing",
    }

    result = action_node(state)

    assert result["status"] == "CLARIFICATION_REQUIRED"
    assert "priority" in result["response"].lower()


def test_create_ticket_uses_authenticated_user():
    state = base_state()
    state["user_id"] = "EMP0002"
    state["entities"] = {
        "user_id": "EMP0001",
        "category": "Software",
        "priority": "low",
        "description": "Test authenticated user mapping",
    }

    result = action_node(state)

    assert result["status"] == "ACTION_COMPLETED"

    arguments = result["tool_calls"][0]["arguments"]

    assert arguments["user_id"] == "EMP0002"