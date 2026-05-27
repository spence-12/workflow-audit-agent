SYSTEM_PROMPT = """
You are a senior business workflow consultant and audit agent.
Your job is to analyze how work is performed across teams, systems, approvals, and handoffs.
Focus on operational efficiency, control quality, scalability, service levels, compliance exposure, and business value.
Be direct, structured, and practical.
Prefer specific observations, quantified assumptions, and implementation-ready recommendations over generic advice.
""".strip()


WORKFLOW_EXTRACTION_PROMPT = """
Analyze the business workflow information below and extract the workflow into a structured sequence of steps.

Objectives:
- Identify each meaningful workflow step in execution order.
- Capture the owner role, system, inputs, outputs, timing, dependencies, and business rules.
- Surface ambiguity or missing information that would block reliable audit conclusions.

Instructions:
- Normalize the workflow into discrete operational steps.
- Merge only clearly duplicate activities.
- Keep role names and system names business-friendly and specific.
- If information is incomplete, make a cautious inference and label it as an assumption.
- Highlight handoffs, approvals, manual data entry, and exception handling.

Workflow context:
{workflow_context}

Business constraints:
{business_constraints}

Output requirements:
- Return a structured workflow decomposition suitable for populating `WorkflowStep` records.
- Include a short assumptions section.
- Include a short list of missing data needed for a stronger audit.
""".strip()


PAIN_POINT_ANALYSIS_PROMPT = """
Review the workflow steps below and identify the most important pain points from a business workflow consulting perspective.

Objectives:
- Detect friction that causes delay, rework, errors, poor visibility, compliance risk, cost, or customer impact.
- Explain why each pain point matters to leadership and operators.
- Separate symptoms from likely root causes.

Instructions:
- Prioritize the highest-value pain points instead of listing every minor issue.
- Pay close attention to manual handoffs, spreadsheet workarounds, duplicated entry, unclear ownership, and inconsistent rules.
- Consider process, people, data, policy, and tooling causes.
- Where possible, connect the issue to measurable outcomes such as cycle time, SLA misses, throughput, or error rates.

Workflow steps:
{workflow_steps}

Audit focus:
{audit_focus}

Output requirements:
- Return pain points suitable for populating `PainPoint` records.
- For each pain point, provide title, step reference, category, description, impact, root cause, severity, frequency, and evidence.
- End with the top 3 pain points that should be addressed first.
""".strip()


AUTOMATION_OPPORTUNITY_PROMPT = """
Identify automation and AI augmentation opportunities in the workflow below.

Objectives:
- Find practical opportunities to reduce manual effort, improve control consistency, and increase throughput.
- Recommend solutions that fit realistic business operations rather than speculative transformation programs.
- Distinguish between basic automation, system integration, workflow orchestration, and AI-assisted decision support.

Instructions:
- Focus on opportunities with clear operational value.
- Consider document intake, classification, routing, validation, approvals, monitoring, exception handling, and reporting.
- Note technical or process dependencies that would affect implementation.
- Estimate the likely complexity and monthly time savings with conservative assumptions.

Workflow steps:
{workflow_steps}

Known pain points:
{pain_points}

Available systems and constraints:
{systems_and_constraints}

Output requirements:
- Return opportunities suitable for populating `AutomationOpportunity` records.
- For each item, provide title, step reference, description, current state, proposed solution, expected benefit, complexity, estimated time savings, and dependencies.
- Rank opportunities by business value and implementation practicality.
""".strip()


ROI_ESTIMATION_PROMPT = """
Estimate the financial return of the workflow improvements described below.

Objectives:
- Translate workflow improvements into practical ROI scenarios.
- Use conservative, business-friendly assumptions.
- Show the relationship between implementation cost, time savings, and annual benefit.

Instructions:
- Base calculations on the provided assumptions when available.
- If assumptions are missing, introduce explicit assumptions and keep them modest.
- Include direct labor savings first, then mention secondary benefits separately if they are harder to quantify.
- Avoid overstating value from uncertain AI benefits.

Automation opportunities:
{automation_opportunities}

Business assumptions:
{business_assumptions}

Cost assumptions:
{cost_assumptions}

Output requirements:
- Return ROI estimates suitable for populating `ROIEstimate` records.
- For each initiative, provide implementation cost, monthly savings, annual benefit, payback period, confidence level, and assumptions.
- Include a short note explaining the biggest sensitivity in each estimate.
""".strip()


RISK_ANALYSIS_PROMPT = """
Assess workflow risks across operations, compliance, security, data quality, finance, and customer experience.

Objectives:
- Identify meaningful workflow risks and describe their business consequences.
- Evaluate the likelihood and impact of each risk.
- Assess whether current controls are adequate and identify gaps.

Instructions:
- Focus on risks tied to approvals, segregation of duties, manual overrides, missing audit trails, poor data quality, policy inconsistency, access issues, and failure-prone handoffs.
- Distinguish between the inherent risk and the residual risk implied by current controls.
- Recommend concrete mitigations that an operations or business systems team could act on.
- Assign an owner role for remediation.

Workflow steps:
{workflow_steps}

Pain points:
{pain_points}

Existing controls:
{existing_controls}

Output requirements:
- Return risk assessments suitable for populating `RiskAssessment` records.
- For each risk, provide title, step reference, risk type, description, likelihood, impact, current controls, control gaps, recommendation, and owner role.
- Close with the highest-priority risks requiring immediate attention.
""".strip()


FINAL_REPORT_PROMPT = """
Create an executive-ready workflow audit report for a business stakeholder audience.

Objectives:
- Summarize the workflow clearly.
- Explain the main pain points, automation opportunities, risks, and ROI implications.
- Recommend a practical path forward with prioritized actions.

Instructions:
- Write in a consulting style suitable for operations, finance, transformation, or functional leaders.
- Be concise, specific, and commercially relevant.
- Highlight tradeoffs, sequencing, and the difference between quick wins and larger initiatives.
- Use the evidence provided instead of generic best-practice language.

Workflow name:
{workflow_name}

Workflow description:
{workflow_description}

Audit scope:
{audit_scope}

Workflow steps:
{workflow_steps}

Pain points:
{pain_points}

Automation opportunities:
{automation_opportunities}

Risk assessments:
{risk_assessments}

ROI estimates:
{roi_estimates}

Output requirements:
- Produce content suitable for a `FinalAuditReport`.
- Include:
  1. Executive summary
  2. Overall maturity assessment
  3. Key pain points
  4. Recommended automation opportunities
  5. Key risks and controls
  6. ROI summary
  7. Priority recommendations
- Keep the recommendations action-oriented and sequenced by impact and feasibility.
""".strip()


SUMMARY_PROMPT_TEMPLATE = """
Workflow: {workflow_name}
Description: {workflow_description}
Focus: {audit_focus}

Findings:
{findings}

Write a short executive summary for a business stakeholder.
""".strip()
