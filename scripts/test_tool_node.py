from app.agent.graph import agent_graph


def run_test(query: str) -> None:
    print("\n" + "=" * 70)
    print(f"QUERY: {query}")
    print("=" * 70)

    result = agent_graph.invoke(
        {
            "request_id": "TEST-001",
            "query": query,
            "retry_count": 0,
            "tool_calls": [],
            "tool_results": [],
            "validation_errors": [],
        }
    )

    print("Intent:", result.get("intent"))
    print("Route:", result.get("route"))
    print("Status:", result.get("status"))
    print("Entities:", result.get("entities"))
    print("Tool calls:", result.get("tool_calls"))
    print("Tool results:", result.get("tool_results"))
    print("Validation errors:", result.get("validation_errors"))
    print("Response:", result.get("response"))


def main() -> None:
    run_test(
        "What is the status of my account? My employee ID is EMP0001."
    )

    run_test(
        "What is the status of my account?"
    )


if __name__ == "__main__":
    main()