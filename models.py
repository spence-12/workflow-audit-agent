from typing import Literal, TypedDict

from pydantic import BaseModel, Field


class WorkflowStep(BaseModel):
    step_id: str = Field(..., description="Unique identifier for the workflow step.")
    name: str = Field(..., description="Short name of the workflow step.")
    description: str = Field(..., description="What happens during the step.")
    owner_role: str = Field(..., description="Role or team responsible for the step.")
    system_name: str = Field(..., description="Primary tool or system used in the step.")
    inputs: list[str] = Field(default_factory=list, description="Information or artifacts needed to perform the step.")
    outputs: list[str] = Field(default_factory=list, description="Information or artifacts produced by the step.")
    frequency: str = Field(..., description="How often the step occurs, such as daily or per request.")
    estimated_minutes: int = Field(..., ge=0, description="Estimated time required to complete the step once.")
    manual_handoffs: int = Field(default=0, ge=0, description="Number of manual handoffs required in this step.")
    dependencies: list[str] = Field(default_factory=list, description="Upstream dependencies or prerequisite actions.")
    business_rules: list[str] = Field(default_factory=list, description="Policies or decision rules applied during the step.")
    pain_signals: list[str] = Field(default_factory=list, description="Known symptoms of friction, delay, or quality issues.")
    risk_notes: str = Field(..., description="Known control, compliance, or operational risk in the step.")


class PainPoint(BaseModel):
    title: str = Field(..., description="Short label for the pain point.")
    step_id: str = Field(..., description="Identifier of the workflow step where the issue appears.")
    category: Literal["delay", "quality", "cost", "compliance", "handoff", "visibility", "rework"] = Field(
        ..., description="Primary category of workflow friction."
    )
    description: str = Field(..., description="Detailed explanation of the problem.")
    impact: str = Field(..., description="Business impact caused by the pain point.")
    root_cause: str = Field(..., description="Likely underlying cause of the issue.")
    severity: Literal["low", "medium", "high", "critical"] = Field(..., description="Relative importance of the pain point.")
    frequency: str = Field(..., description="How often the problem occurs.")
    evidence: list[str] = Field(default_factory=list, description="Supporting examples, metrics, or observations.")


class AutomationOpportunity(BaseModel):
    title: str = Field(..., description="Short label for the automation opportunity.")
    step_id: str = Field(..., description="Identifier of the workflow step that could be improved.")
    description: str = Field(..., description="What should be automated or augmented.")
    current_state: str = Field(..., description="How the work is done today.")
    proposed_solution: str = Field(..., description="Suggested automation or AI-enabled improvement.")
    expected_benefit: str = Field(..., description="Main business value created by the change.")
    complexity: Literal["low", "medium", "high"] = Field(..., description="Implementation complexity estimate.")
    estimated_time_saved_hours_per_month: float = Field(
        ..., ge=0, description="Estimated monthly time savings from the proposed automation."
    )
    dependencies: list[str] = Field(default_factory=list, description="Systems, data, or approvals needed to implement the opportunity.")


class RiskAssessment(BaseModel):
    title: str = Field(..., description="Short label for the identified risk.")
    step_id: str = Field(..., description="Identifier of the workflow step where the risk is present.")
    risk_type: Literal["operational", "financial", "compliance", "security", "data_quality", "customer_experience"] = Field(
        ..., description="Primary risk domain."
    )
    description: str = Field(..., description="Explanation of the risk.")
    likelihood: Literal["low", "medium", "high"] = Field(..., description="Likelihood of the risk materializing.")
    impact: Literal["low", "medium", "high", "critical"] = Field(..., description="Severity of business impact.")
    current_controls: list[str] = Field(default_factory=list, description="Controls or mitigations currently in place.")
    control_gaps: list[str] = Field(default_factory=list, description="Weaknesses in the current control environment.")
    recommendation: str = Field(..., description="Recommended mitigation or control improvement.")
    owner_role: str = Field(..., description="Role that should own remediation.")


class ROIEstimate(BaseModel):
    initiative_name: str = Field(..., description="Name of the improvement initiative.")
    implementation_cost_usd: float = Field(..., ge=0, description="Estimated one-time implementation cost.")
    monthly_savings_usd: float = Field(..., ge=0, description="Estimated recurring monthly savings.")
    annual_benefit_usd: float = Field(..., ge=0, description="Estimated annual financial benefit.")
    payback_period_months: float = Field(..., ge=0, description="Estimated months required to recover the initial cost.")
    confidence_level: Literal["low", "medium", "high"] = Field(..., description="Confidence in the estimate.")
    assumptions: list[str] = Field(default_factory=list, description="Key assumptions behind the ROI calculation.")


class FinalAuditReport(BaseModel):
    workflow_name: str = Field(..., description="Name of the audited workflow.")
    workflow_description: str = Field(..., description="Summary of what the workflow does.")
    audit_scope: str = Field(..., description="Boundaries and focus of the review.")
    overall_maturity: Literal["ad_hoc", "developing", "defined", "managed", "optimized"] = Field(
        ..., description="Overall maturity assessment for the workflow."
    )
    executive_summary: str = Field(..., description="Short summary of key findings and recommendations.")
    workflow_steps: list[WorkflowStep] = Field(default_factory=list, description="Ordered steps included in the audit.")
    pain_points: list[PainPoint] = Field(default_factory=list, description="Observed issues across the workflow.")
    automation_opportunities: list[AutomationOpportunity] = Field(
        default_factory=list, description="Potential automation or AI opportunities."
    )
    risk_assessments: list[RiskAssessment] = Field(default_factory=list, description="Risk analysis for the workflow.")
    roi_estimates: list[ROIEstimate] = Field(default_factory=list, description="ROI scenarios for recommended improvements.")
    priority_recommendations: list[str] = Field(default_factory=list, description="Top actions to pursue next.")


class WorkflowAuditState(TypedDict, total=False):
    workflow_name: str
    workflow_description: str
    audit_focus: str
    steps: list[WorkflowStep]
    risk_assessments: list[RiskAssessment]
    summary: str
