import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = PROJECT_ROOT / "evaluation" / "results" / "evaluation_results.jsonl"

with RESULTS_PATH.open(encoding="utf-8") as file:
    rows = [json.loads(line) for line in file if line.strip()]

total = len(rows)


def accuracy(expected_field: str, actual_field: str) -> float:
    correct = sum(
        row[expected_field] == row[actual_field]
        for row in rows
    )
    return correct / total * 100 if total else 0.0


print(f"Total scenarios: {total}")
print(f"Intent accuracy: {accuracy('expected_intent', 'actual_intent'):.1f}%")
print(f"Route accuracy: {accuracy('expected_route', 'actual_route'):.1f}%")
print(
    "Escalation accuracy: "
    f"{accuracy('expected_escalation', 'actual_escalation'):.1f}%"
)

print("\nMismatches:")

mismatch_found = False

for row in rows:
    mismatches = []

    if row["expected_intent"] != row["actual_intent"]:
        mismatches.append(
            f"intent: expected={row['expected_intent']}, "
            f"actual={row['actual_intent']}"
        )

    if row["expected_route"] != row["actual_route"]:
        mismatches.append(
            f"route: expected={row['expected_route']}, "
            f"actual={row['actual_route']}"
        )

    if row["expected_escalation"] != row["actual_escalation"]:
        mismatches.append(
            f"escalation: expected={row['expected_escalation']}, "
            f"actual={row['actual_escalation']}"
        )

    if mismatches:
        mismatch_found = True
        print(f"- {row['scenario_id']}: {row['query']}")
        for mismatch in mismatches:
            print(f"  {mismatch}")

if not mismatch_found:
    print("None. All evaluated fields matched.")