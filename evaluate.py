from graph import run_workflow_audit
from sample_inputs import SAMPLE_WORKFLOWS


def has_workflow_steps(result: dict) -> bool:
    return bool(result.get("workflow_steps"))


def has_pain_points(result: dict) -> bool:
    return bool(result.get("pain_points"))


def has_automation_opportunities(result: dict) -> bool:
    return bool(result.get("automation_opportunities"))


def has_roi_estimate(result: dict) -> bool:
    return result.get("roi_estimate") is not None


def has_risks(result: dict) -> bool:
    return bool(result.get("risks"))


def has_implementation_roadmap(result: dict) -> bool:
    final_report = result.get("final_report")
    return bool(final_report and final_report.priority_recommendations)


def score_result(result: dict) -> dict[str, bool]:
    return {
        "workflow_steps": has_workflow_steps(result),
        "pain_points": has_pain_points(result),
        "automation_opportunities": has_automation_opportunities(result),
        "roi_estimate": has_roi_estimate(result),
        "risks": has_risks(result),
        "implementation_roadmap": has_implementation_roadmap(result),
    }


def run_evaluation() -> None:
    aggregate_passes = {
        "workflow_steps": 0,
        "pain_points": 0,
        "automation_opportunities": 0,
        "roi_estimate": 0,
        "risks": 0,
        "implementation_roadmap": 0,
    }

    print("# Workflow Audit Agent Evaluation")
    print()

    for workflow_name, workflow_input in SAMPLE_WORKFLOWS.items():
        result = run_workflow_audit(workflow_input)
        checks = score_result(result)
        passed = sum(checks.values())
        total = len(checks)

        print(f"## {workflow_name}")
        for check_name, status in checks.items():
            marker = "PASS" if status else "FAIL"
            print(f"- {check_name}: {marker}")
            aggregate_passes[check_name] += int(status)
        print(f"- score: {passed}/{total}")
        print()

    workflow_count = len(SAMPLE_WORKFLOWS)
    overall_passes = sum(aggregate_passes.values())
    overall_total = workflow_count * len(aggregate_passes)

    print("## Summary")
    for check_name, passed_count in aggregate_passes.items():
        print(f"- {check_name}: {passed_count}/{workflow_count}")
    print(f"- overall_score: {overall_passes}/{overall_total}")


if __name__ == "__main__":
    run_evaluation()
