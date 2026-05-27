from graph import build_workflow
from models import FinalAuditReport
from sample_inputs import SAMPLE_WORKFLOW_INPUT


def format_final_report_markdown(report: FinalAuditReport) -> str:
    lines: list[str] = [
        f"# {report.workflow_name}",
        "",
        "## Executive Summary",
        report.executive_summary,
        "",
        "## Audit Scope",
        report.audit_scope,
        "",
        "## Workflow Description",
        report.workflow_description,
        "",
        "## Overall Maturity",
        report.overall_maturity.replace("_", " ").title(),
        "",
        "## Workflow Steps",
    ]

    for step in report.workflow_steps:
        lines.extend(
            [
                f"### {step.name}",
                f"- Step ID: `{step.step_id}`",
                f"- Owner Role: {step.owner_role}",
                f"- System: {step.system_name}",
                f"- Frequency: {step.frequency}",
                f"- Estimated Minutes: {step.estimated_minutes}",
                f"- Manual Handoffs: {step.manual_handoffs}",
                f"- Description: {step.description}",
                "",
            ]
        )

    lines.append("## Pain Points")
    for pain_point in report.pain_points:
        lines.extend(
            [
                f"### {pain_point.title}",
                f"- Step ID: `{pain_point.step_id}`",
                f"- Category: {pain_point.category}",
                f"- Severity: {pain_point.severity}",
                f"- Impact: {pain_point.impact}",
                f"- Root Cause: {pain_point.root_cause}",
                f"- Description: {pain_point.description}",
                "",
            ]
        )

    lines.append("## Automation Opportunities")
    for opportunity in report.automation_opportunities:
        lines.extend(
            [
                f"### {opportunity.title}",
                f"- Step ID: `{opportunity.step_id}`",
                f"- Complexity: {opportunity.complexity}",
                f"- Expected Benefit: {opportunity.expected_benefit}",
                f"- Time Saved per Month: {opportunity.estimated_time_saved_hours_per_month} hours",
                f"- Current State: {opportunity.current_state}",
                f"- Proposed Solution: {opportunity.proposed_solution}",
                "",
            ]
        )

    lines.append("## Risk Assessments")
    for risk in report.risk_assessments:
        lines.extend(
            [
                f"### {risk.title}",
                f"- Step ID: `{risk.step_id}`",
                f"- Risk Type: {risk.risk_type}",
                f"- Likelihood: {risk.likelihood}",
                f"- Impact: {risk.impact}",
                f"- Owner Role: {risk.owner_role}",
                f"- Description: {risk.description}",
                f"- Recommendation: {risk.recommendation}",
                "",
            ]
        )

    lines.append("## ROI Estimates")
    for roi in report.roi_estimates:
        lines.extend(
            [
                f"### {roi.initiative_name}",
                f"- Implementation Cost: ${roi.implementation_cost_usd:,.2f}",
                f"- Monthly Savings: ${roi.monthly_savings_usd:,.2f}",
                f"- Annual Benefit: ${roi.annual_benefit_usd:,.2f}",
                f"- Payback Period: {roi.payback_period_months} months",
                f"- Confidence: {roi.confidence_level}",
                "",
            ]
        )

    lines.append("## Priority Recommendations")
    for recommendation in report.priority_recommendations:
        lines.append(f"- {recommendation}")

    return "\n".join(lines)


def main() -> None:
    workflow = build_workflow()
    result = workflow.invoke(SAMPLE_WORKFLOW_INPUT)
    final_report = result["final_report"]
    print(format_final_report_markdown(final_report))


if __name__ == "__main__":
    main()
