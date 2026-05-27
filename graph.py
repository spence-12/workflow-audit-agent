import logging
import time
from functools import wraps
from typing import Callable, TypedDict

from langgraph.graph import END, START, StateGraph

from models import (
    AutomationOpportunity,
    FinalAuditReport,
    PainPoint,
    ROIEstimate,
    RiskAssessment,
    WorkflowStep,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("workflow_audit_agent")


class WorkflowAuditState(TypedDict, total=False):
    raw_input: str
    workflow_steps: list[WorkflowStep]
    pain_points: list[PainPoint]
    automation_opportunities: list[AutomationOpportunity]
    roi_estimate: ROIEstimate
    risks: list[RiskAssessment]
    final_report: FinalAuditReport


def log_node_execution(node_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(state: WorkflowAuditState) -> WorkflowAuditState:
            start_time = time.perf_counter()
            logger.info("Node started: %s", node_name)
            result = func(state)
            duration = time.perf_counter() - start_time
            logger.info("Node finished: %s (%.3fs)", node_name, duration)
            return result

        return wrapper

    return decorator


@log_node_execution("extract_workflow")
def extract_workflow(state: WorkflowAuditState) -> WorkflowAuditState:
    raw_input = state.get("raw_input", "")
    lines = [line.strip("- ").strip() for line in raw_input.splitlines() if line.strip()]

    if not lines:
        lines = [
            "Receive workflow intake request",
            "Review request details and validate completeness",
            "Route request for approval and complete follow-up actions",
        ]

    workflow_steps: list[WorkflowStep] = []
    for index, line in enumerate(lines, start=1):
        workflow_steps.append(
            WorkflowStep(
                step_id=f"step_{index}",
                name=line[:80],
                description=line,
                owner_role="Business Operations",
                system_name="Email and line-of-business systems",
                inputs=["Prior step output"],
                outputs=["Next step input"],
                frequency="unknown",
                estimated_minutes=15,
                manual_handoffs=1,
                dependencies=[],
                business_rules=[],
                pain_signals=["Manual coordination"],
                risk_notes="Manual processing may introduce delays, inconsistent execution, or missing audit evidence.",
            )
        )

    return {"workflow_steps": workflow_steps}


@log_node_execution("analyze_pain_points")
def analyze_pain_points(state: WorkflowAuditState) -> WorkflowAuditState:
    pain_points: list[PainPoint] = []

    for step in state.get("workflow_steps", []):
        pain_points.append(
            PainPoint(
                title=f"Manual effort in {step.name}",
                step_id=step.step_id,
                category="handoff" if step.manual_handoffs else "delay",
                description=f"{step.name} relies on manual coordination and operator judgment.",
                impact="Longer cycle times, variable throughput, and higher risk of missed work.",
                root_cause="The workflow depends on human follow-up instead of structured routing and validation.",
                severity="high" if step.manual_handoffs else "medium",
                frequency=step.frequency,
                evidence=step.pain_signals or ["Manual step identified during extraction."],
            )
        )

    return {"pain_points": pain_points}


@log_node_execution("identify_automation_opportunities")
def identify_automation_opportunities(state: WorkflowAuditState) -> WorkflowAuditState:
    opportunities: list[AutomationOpportunity] = []

    for step in state.get("workflow_steps", []):
        opportunities.append(
            AutomationOpportunity(
                title=f"Automate {step.name}",
                step_id=step.step_id,
                description=f"Reduce manual effort and improve consistency in {step.name}.",
                current_state=f"{step.name} is handled manually by {step.owner_role}.",
                proposed_solution=f"Add workflow routing, validation, and status tracking around {step.system_name}.",
                expected_benefit="Lower processing effort, better auditability, and fewer execution delays.",
                complexity="medium",
                estimated_time_saved_hours_per_month=float(max(step.estimated_minutes * 4, 2)),
                dependencies=[step.system_name, "Business rule definition", "Stakeholder sign-off"],
            )
        )

    return {"automation_opportunities": opportunities}


@log_node_execution("estimate_roi")
def estimate_roi(state: WorkflowAuditState) -> WorkflowAuditState:
    opportunities = state.get("automation_opportunities", [])
    total_hours_saved = sum(item.estimated_time_saved_hours_per_month for item in opportunities)
    monthly_savings_usd = round(total_hours_saved * 50, 2)
    implementation_cost_usd = round(max(len(opportunities), 1) * 5000, 2)
    annual_benefit_usd = round(monthly_savings_usd * 12, 2)
    payback_period_months = round(
        implementation_cost_usd / monthly_savings_usd, 1
    ) if monthly_savings_usd else 0.0

    roi_estimate = ROIEstimate(
        initiative_name="Workflow automation program",
        implementation_cost_usd=implementation_cost_usd,
        monthly_savings_usd=monthly_savings_usd,
        annual_benefit_usd=annual_benefit_usd,
        payback_period_months=payback_period_months,
        confidence_level="medium",
        assumptions=[
            "Average fully loaded labor cost is $50 per hour.",
            "Estimated time savings reflect recoverable operational capacity.",
            "Implementation cost covers initial design, build, and rollout only.",
        ],
    )

    return {"roi_estimate": roi_estimate}


@log_node_execution("analyze_risks")
def analyze_risks(state: WorkflowAuditState) -> WorkflowAuditState:
    risks: list[RiskAssessment] = []

    for step in state.get("workflow_steps", []):
        risks.append(
            RiskAssessment(
                title=f"Control risk in {step.name}",
                step_id=step.step_id,
                risk_type="operational" if "manual" in step.risk_notes.lower() else "compliance",
                description=step.risk_notes,
                likelihood="high" if step.manual_handoffs else "medium",
                impact="high",
                current_controls=["Human review"],
                control_gaps=["No consistent automated control evidence", "Execution depends on manual follow-up"],
                recommendation=f"Introduce system-based tracking, approvals, and exception logging for {step.name}.",
                owner_role=step.owner_role,
            )
        )

    return {"risks": risks}


@log_node_execution("generate_report")
def generate_report(state: WorkflowAuditState) -> WorkflowAuditState:
    workflow_steps = state.get("workflow_steps", [])
    pain_points = state.get("pain_points", [])
    opportunities = state.get("automation_opportunities", [])
    risks = state.get("risks", [])
    roi_estimate = state.get("roi_estimate")

    executive_summary = (
        f"The workflow contains {len(workflow_steps)} core steps, {len(pain_points)} major pain points, "
        f"{len(opportunities)} automation opportunities, and {len(risks)} notable risks. "
        f"Primary value comes from reducing manual coordination, improving control consistency, and increasing visibility."
    )

    priority_recommendations = [
        "Standardize workflow routing and status tracking across all steps.",
        "Implement validation and approval controls in the system of record.",
        "Prioritize quick-win automations with the shortest payback period.",
    ]

    final_report = FinalAuditReport(
        workflow_name="Workflow Audit",
        workflow_description=state.get("raw_input", "No workflow description provided."),
        audit_scope="Operational workflow review covering pain points, automation, ROI, and risks.",
        overall_maturity="developing",
        executive_summary=executive_summary,
        workflow_steps=workflow_steps,
        pain_points=pain_points,
        automation_opportunities=opportunities,
        risk_assessments=risks,
        roi_estimates=[roi_estimate] if roi_estimate else [],
        priority_recommendations=priority_recommendations,
    )

    return {"final_report": final_report}


def build_workflow():
    graph_builder = StateGraph(WorkflowAuditState)
    graph_builder.add_node("extract_workflow", extract_workflow)
    graph_builder.add_node("analyze_pain_points", analyze_pain_points)
    graph_builder.add_node("identify_automation_opportunities", identify_automation_opportunities)
    graph_builder.add_node("estimate_roi", estimate_roi)
    graph_builder.add_node("analyze_risks", analyze_risks)
    graph_builder.add_node("generate_report", generate_report)
    graph_builder.add_edge(START, "extract_workflow")
    graph_builder.add_edge("extract_workflow", "analyze_pain_points")
    graph_builder.add_edge("analyze_pain_points", "identify_automation_opportunities")
    graph_builder.add_edge("identify_automation_opportunities", "estimate_roi")
    graph_builder.add_edge("estimate_roi", "analyze_risks")
    graph_builder.add_edge("analyze_risks", "generate_report")
    graph_builder.add_edge("generate_report", END)
    return graph_builder.compile()


def run_workflow_audit(state: WorkflowAuditState) -> WorkflowAuditState:
    start_time = time.perf_counter()
    logger.info("Audit started")
    workflow = build_workflow()
    result = workflow.invoke(state)
    duration = time.perf_counter() - start_time
    report_generated = bool(result.get("final_report"))
    logger.info("Final report generated successfully: %s", report_generated)
    logger.info("Audit finished in %.3fs", duration)
    return result
