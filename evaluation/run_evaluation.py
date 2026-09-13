import sys
import json
from pathlib import Path
from uuid import uuid4


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.agent.graph import agent_graph


DATASET_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "dataset"
    / "support_scenarios.jsonl"
)

RESULTS_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "results"
    / "evaluation_results.jsonl"
)

def load_scenarios() -> list[dict]:
    """Load evaluation scenarios from JSONL."""

    with DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return [
            json.loads(line)
            for line in file
            if line.strip()
        ]


def run_scenario(scenario: dict) -> dict:
    """Run one scenario through the agent."""

    request_id = f"EVAL-{uuid4().hex[:12].upper()}"

    initial_state = {
        "request_id": request_id,
        "user_id": "EMP0001",
        "query": scenario["query"],
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

    result = agent_graph.invoke(initial_state)

    return {
        "scenario_id": scenario["id"],
        "query": scenario["query"],
        "expected_intent": scenario["expected_intent"],
        "actual_intent": result.get("intent"),
        "expected_route": scenario["expected_route"],
        "actual_route": result.get("route"),
        "expected_escalation": scenario["should_escalate"],
        "actual_escalation": result.get(
            "escalation_required",
            False,
        ),
        "status": result.get("status"),
        "response": result.get("response"),
        "retrieved_context_count": len(
            result.get("retrieved_context", [])
        ),
        "tool_call_count": len(
            result.get("tool_calls", [])
        ),
    }


def main() -> None:
    """Run and save the evaluation."""

    scenarios = load_scenarios()
    results = []

    for index, scenario in enumerate(scenarios, start=1):
        print(
            f"[{index}/{len(scenarios)}] "
            f"Running {scenario['id']}: "
            f"{scenario['query']}"
        )

        result = run_scenario(scenario)
        results.append(result)

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with RESULTS_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        for result in results:
            file.write(
                json.dumps(
                    result,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print()
    print(
        f"Saved {len(results)} results to "
        f"{RESULTS_PATH}"
    )


if __name__ == "__main__":
    main()