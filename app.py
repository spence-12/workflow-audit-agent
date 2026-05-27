import streamlit as st

from graph import WorkflowAuditState, run_workflow_audit
from models import FinalAuditReport
from sample_inputs import SAMPLE_WORKFLOWS, SAMPLE_WORKFLOW_INPUT


DEFAULT_WORKFLOW_TEXT = SAMPLE_WORKFLOW_INPUT["raw_input"]


def build_markdown_report(report: FinalAuditReport) -> str:
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
        "## Pain Points",
    ]

    for pain_point in report.pain_points:
        lines.extend(
            [
                f"### {pain_point.title}",
                f"- Step ID: `{pain_point.step_id}`",
                f"- Category: {pain_point.category}",
                f"- Severity: {pain_point.severity}",
                f"- Description: {pain_point.description}",
                f"- Impact: {pain_point.impact}",
                f"- Root Cause: {pain_point.root_cause}",
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
                f"- Proposed Solution: {opportunity.proposed_solution}",
                f"- Estimated Time Saved: {opportunity.estimated_time_saved_hours_per_month} hours/month",
                "",
            ]
        )

    lines.append("## ROI Estimate")
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

    lines.append("## Risks")
    for risk in report.risk_assessments:
        lines.extend(
            [
                f"### {risk.title}",
                f"- Step ID: `{risk.step_id}`",
                f"- Risk Type: {risk.risk_type}",
                f"- Likelihood: {risk.likelihood}",
                f"- Impact: {risk.impact}",
                f"- Recommendation: {risk.recommendation}",
                "",
            ]
        )

    lines.append("## Implementation Roadmap")
    for index, recommendation in enumerate(report.priority_recommendations, start=1):
        lines.append(f"{index}. {recommendation}")

    return "\n".join(lines)


def render_workflow_summary(report: FinalAuditReport) -> None:
    st.subheader("Workflow Summary")
    st.markdown(report.executive_summary)
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    summary_col1.metric("Steps", len(report.workflow_steps))
    summary_col2.metric("Pain Points", len(report.pain_points))
    summary_col3.metric("Opportunities", len(report.automation_opportunities))
    summary_col4.metric("Risks", len(report.risk_assessments))
    st.caption(f"Maturity: {report.overall_maturity.replace('_', ' ').title()}")


def render_pain_points(report: FinalAuditReport) -> None:
    st.subheader("Pain Points")
    for pain_point in report.pain_points:
        with st.expander(f"{pain_point.title} ({pain_point.severity})", expanded=False):
            st.markdown(f"**Step:** `{pain_point.step_id}`")
            st.markdown(f"**Category:** {pain_point.category}")
            st.markdown(f"**Description:** {pain_point.description}")
            st.markdown(f"**Impact:** {pain_point.impact}")
            st.markdown(f"**Root Cause:** {pain_point.root_cause}")


def render_automation_opportunities(report: FinalAuditReport) -> None:
    st.subheader("Automation Opportunities")
    for opportunity in report.automation_opportunities:
        with st.expander(opportunity.title, expanded=False):
            st.markdown(f"**Step:** `{opportunity.step_id}`")
            st.markdown(f"**Complexity:** {opportunity.complexity}")
            st.markdown(f"**Current State:** {opportunity.current_state}")
            st.markdown(f"**Proposed Solution:** {opportunity.proposed_solution}")
            st.markdown(f"**Expected Benefit:** {opportunity.expected_benefit}")
            st.markdown(
                f"**Estimated Time Saved:** {opportunity.estimated_time_saved_hours_per_month} hours per month"
            )


def render_roi(report: FinalAuditReport) -> None:
    st.subheader("ROI Estimate")
    if not report.roi_estimates:
        st.info("No ROI estimate was generated.")
        return

    roi = report.roi_estimates[0]
    roi_col1, roi_col2, roi_col3, roi_col4 = st.columns(4)
    roi_col1.metric("Implementation Cost", f"${roi.implementation_cost_usd:,.0f}")
    roi_col2.metric("Monthly Savings", f"${roi.monthly_savings_usd:,.0f}")
    roi_col3.metric("Annual Benefit", f"${roi.annual_benefit_usd:,.0f}")
    roi_col4.metric("Payback", f"{roi.payback_period_months} mo")
    st.markdown(f"**Confidence:** {roi.confidence_level}")
    st.markdown("**Assumptions**")
    for assumption in roi.assumptions:
        st.markdown(f"- {assumption}")


def render_risks(report: FinalAuditReport) -> None:
    st.subheader("Risks")
    for risk in report.risk_assessments:
        with st.expander(f"{risk.title} ({risk.impact})", expanded=False):
            st.markdown(f"**Step:** `{risk.step_id}`")
            st.markdown(f"**Type:** {risk.risk_type}")
            st.markdown(f"**Likelihood:** {risk.likelihood}")
            st.markdown(f"**Impact:** {risk.impact}")
            st.markdown(f"**Description:** {risk.description}")
            st.markdown(f"**Recommendation:** {risk.recommendation}")


def render_roadmap(report: FinalAuditReport) -> None:
    st.subheader("Implementation Roadmap")
    phases = [
        ("Phase 1", report.priority_recommendations[:1]),
        ("Phase 2", report.priority_recommendations[1:2]),
        ("Phase 3", report.priority_recommendations[2:]),
    ]

    for phase_name, items in phases:
        if not items:
            continue
        st.markdown(f"**{phase_name}**")
        for item in items:
            st.markdown(f"- {item}")


def run_audit(raw_input: str) -> WorkflowAuditState:
    return run_workflow_audit({"raw_input": raw_input})


def main() -> None:
    st.set_page_config(page_title="Workflow Audit Agent", page_icon=":clipboard:", layout="wide")
    st.title("Workflow Audit Agent")
    st.write("Paste a business workflow description, run the audit, and review the generated analysis.")

    example_names = ["custom"] + list(SAMPLE_WORKFLOWS.keys())
    selected_example = st.selectbox("Example workflow", example_names)

    default_text = (
        SAMPLE_WORKFLOWS[selected_example]["raw_input"]
        if selected_example != "custom"
        else DEFAULT_WORKFLOW_TEXT
    )
    workflow_text = st.text_area(
        "Workflow description",
        value=default_text,
        height=220,
        placeholder="Describe the workflow as a sequence of business steps.",
    )

    if st.button("Run Audit", type="primary"):
        if not workflow_text.strip():
            st.warning("Enter a workflow description before running the audit.")
            return

        with st.spinner("Running workflow audit..."):
            result = run_audit(workflow_text)

        report = result["final_report"]
        markdown_report = build_markdown_report(report)

        render_workflow_summary(report)
        render_pain_points(report)
        render_automation_opportunities(report)
        render_roi(report)
        render_risks(report)
        render_roadmap(report)

        st.download_button(
            "Download Final Report",
            data=markdown_report,
            file_name="workflow_audit_report.md",
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()
