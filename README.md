# Workflow Audit Agent

LangGraph-based workflow analysis app that turns a plain-English business process description into a structured audit report with workflow steps, pain points, automation opportunities, ROI estimates, risks, and an implementation roadmap.

## Problem

Business workflows are often documented loosely across email, meetings, SOPs, and tribal knowledge. That creates predictable problems:

- manual handoffs are hard to see
- process bottlenecks are diagnosed too late
- automation opportunities are identified inconsistently
- ROI is discussed qualitatively instead of quantitatively
- risks and control gaps are scattered across teams

Teams usually need a consultant, analyst, or operations lead to convert an unstructured workflow description into an actionable improvement plan.

## Solution

This project is a `Workflow Audit Agent` built with `LangGraph`, `Pydantic`, and `Streamlit`.

It accepts a workflow description, runs it through a multi-step audit flow, and produces:

- extracted workflow steps
- pain point analysis
- automation opportunities
- ROI estimate
- risk assessment
- implementation roadmap
- a final report suitable for business review

The current version uses deterministic node logic so the full pipeline is inspectable and testable locally. The repo also includes prompt templates and model structures designed for a later LLM-backed implementation.

## Demo

### 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Streamlit app

```bash
streamlit run app.py
```

The app lets you:

- paste a workflow description
- choose from built-in sample workflows
- click `Run Audit`
- review the generated summary, pain points, automation opportunities, ROI, risks, and roadmap
- download the final report as markdown

### 3. Run the CLI version

```bash
python main.py
```

### 4. Run the evaluation script

```bash
python evaluate.py
```

### 5. Run tests

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest tests/test_graph.py -q
```

## Architecture

The project is structured as a lightweight workflow intelligence application:

- `app.py`: Streamlit UI
- `main.py`: CLI entry point that prints the final report in markdown
- `graph.py`: LangGraph workflow definition, node logic, and runtime logging
- `models.py`: Pydantic models for workflow steps, pain points, automation opportunities, risks, ROI, and final reports
- `prompts.py`: business-consulting prompt templates for future LLM integration
- `sample_inputs.py`: five sample business workflows
- `evaluate.py`: simple evaluation harness across all sample workflows
- `tests/`: basic graph test coverage

## Tech Stack

- `Python`
- `LangGraph`
- `LangChain`
- `OpenAI` client library
- `Pydantic`
- `Streamlit`
- `pandas`
- `python-dotenv`
- `pytest`

## LangGraph Flow

The audit pipeline is implemented as a `StateGraph` with this sequence:

1. `extract_workflow`
2. `analyze_pain_points`
3. `identify_automation_opportunities`
4. `estimate_roi`
5. `analyze_risks`
6. `generate_report`

The graph state includes:

- `raw_input`
- `workflow_steps`
- `pain_points`
- `automation_opportunities`
- `roi_estimate`
- `risks`
- `final_report`

Each node is logged at start and finish, and the full audit duration is recorded in `graph.py`.

## Sample Input

Example workflow:

```text
Collect supplier invoices from the shared AP inbox and vendor portal.
Verify that each invoice includes a purchase order, correct vendor details, and required tax fields.
Match the invoice against purchase orders and goods receipt records in the ERP.
Route invoices with discrepancies to buyers or requestors for clarification.
Send invoices above approval thresholds to finance managers for approval.
Post approved invoices for payment and notify the treasury team of upcoming disbursements.
```

The repo also includes sample workflows for:

- customer support
- invoice processing
- sales lead qualification
- employee onboarding
- meeting follow-up

## Sample Output

Representative output sections:

```md
# Workflow Audit

## Executive Summary
The workflow contains 6 core steps, 6 major pain points, 6 automation opportunities, and 6 notable risks.

## Pain Points
- Manual effort in Verify that each invoice includes a purchase order...

## Automation Opportunities
- Automate Match the invoice against purchase orders and goods receipt records...

## ROI Estimates
- Implementation Cost: $30,000.00
- Monthly Savings: $18,000.00

## Priority Recommendations
- Standardize workflow routing and status tracking across all steps.
- Implement validation and approval controls in the system of record.
- Prioritize quick-win automations with the shortest payback period.
```

The exact output depends on the workflow text, but the evaluation script checks that the required sections are present.

## Evaluation Method

The project includes a simple structural evaluation script in `evaluate.py`.

It runs the agent on all five sample workflows and scores whether the output contains:

- workflow steps
- pain points
- automation opportunities
- ROI estimate
- risks
- implementation roadmap

The roadmap check is based on `final_report.priority_recommendations`, which is the current roadmap representation in this scaffold.

## Future Improvements

- replace deterministic node logic with LLM-backed reasoning
- add structured prompt execution per node using `prompts.py`
- persist reports to `outputs/`
- expand evaluation from presence checks to quality scoring
- add golden test cases and regression benchmarks
- support CSV, process map, and policy document ingestion
- add human review and approval loops for recommendations
- generate visual workflow maps and executive dashboards

## Portfolio / Case Study Angle

This project is a strong portfolio piece because it demonstrates more than a basic chatbot:

- it models a real business consulting workflow
- it uses graph-based orchestration instead of a single prompt call
- it defines typed intermediate artifacts with `Pydantic`
- it includes a UI, CLI path, evaluation script, and test scaffold
- it frames AI work in terms of operational value, controls, and ROI

From a case study perspective, this can be positioned as:

`How I built a workflow audit agent that converts unstructured business process descriptions into structured improvement plans using LangGraph.`

That framing is useful for roles and clients focused on:

- AI product engineering
- operations automation
- internal tools
- workflow intelligence
- business systems modernization

## Notes

- The current implementation is a scaffold designed for extension.
- Prompt templates are included, but the nodes are not yet calling an LLM.
- Logging is built in for node-level execution and end-to-end audit timing.
