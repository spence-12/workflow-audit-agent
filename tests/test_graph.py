from graph import build_workflow
from sample_inputs import SAMPLE_WORKFLOW_INPUT


def test_workflow_generates_findings_and_summary():
    graph = build_workflow()

    result = graph.invoke(SAMPLE_WORKFLOW_INPUT)

    assert result["workflow_steps"]
    assert result["pain_points"]
    assert result["automation_opportunities"]
    assert result["roi_estimate"]
    assert result["risks"]
    assert result["final_report"]
