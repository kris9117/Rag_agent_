from app.agent.graph import agent_graph


def main() -> None:
    

    result = agent_graph.invoke(
        {
            "request_id": "REQ-RAG-001",
            "user_id": None,
            "query": "My VPN authentication keeps failing.",
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
    )

    print("Intent:", result.get("intent"))
    print("Route:", result.get("route"))
    print("Status:", result.get("status"))
    print("Response:")
    print(result.get("response"))

    print("\nRetrieved context count:")
    print(len(result.get("retrieved_context", [])))


if __name__ == "__main__":
    main()