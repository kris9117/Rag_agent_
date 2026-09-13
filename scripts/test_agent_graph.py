from uuid import uuid4

from app.agent.graph import graph


def main() -> None:
    state = {
        "request_id": str(uuid4()),
        "user_id": "EMP0001",
        "query": "My VPN is not connecting.",
        "intent": None,
        "entities": {},
        "route": None,
        "retrieved_context": [],
        "tool_calls": [],
        "tool_results": [],
        "validation_errors": [],
        "retry_count": 0,
        "response": None,
        "status": None,
        "escalation_required": False,
    }

    result = graph.invoke(state)

    print("=== Final State ===")

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()