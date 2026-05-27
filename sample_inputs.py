from graph import WorkflowAuditState


CUSTOMER_SUPPORT_WORKFLOW: WorkflowAuditState = {
    "raw_input": """
    Receive inbound customer support requests from email, chat, and web forms.
    Triage each ticket by product area, urgency, and customer tier.
    Search the knowledge base and previous tickets for likely resolutions.
    Route technical issues to the appropriate support queue when first-line resolution fails.
    Respond to the customer with troubleshooting steps or a status update.
    Confirm resolution, close the ticket, and tag the outcome for reporting.
    """.strip()
}


INVOICE_PROCESSING_WORKFLOW: WorkflowAuditState = {
    "raw_input": """
    Collect supplier invoices from the shared AP inbox and vendor portal.
    Verify that each invoice includes a purchase order, correct vendor details, and required tax fields.
    Match the invoice against purchase orders and goods receipt records in the ERP.
    Route invoices with discrepancies to buyers or requestors for clarification.
    Send invoices above approval thresholds to finance managers for approval.
    Post approved invoices for payment and notify the treasury team of upcoming disbursements.
    """.strip()
}


SALES_LEAD_QUALIFICATION_WORKFLOW: WorkflowAuditState = {
    "raw_input": """
    Capture inbound sales leads from the website, events, partner referrals, and outbound campaigns.
    Enrich lead records with company size, industry, geography, and contact details.
    Score leads based on fit, engagement, buying signals, and target account status.
    Assign qualified leads to the appropriate sales development representative by territory and segment.
    Conduct discovery outreach by email and phone to confirm need, timing, and decision process.
    Convert qualified leads to opportunities and hand them off to account executives with meeting notes.
    """.strip()
}


EMPLOYEE_ONBOARDING_WORKFLOW: WorkflowAuditState = {
    "raw_input": """
    Receive a signed offer confirmation and create a new hire onboarding request.
    Collect employee details and trigger account provisioning for email, HRIS, payroll, and collaboration tools.
    Coordinate equipment ordering, shipping, and workplace access with IT and facilities.
    Schedule orientation sessions, manager introductions, and required compliance training.
    Confirm that system access, hardware, and policy acknowledgments are completed before the start date.
    Check in during the first two weeks and resolve open onboarding issues from managers or the new hire.
    """.strip()
}


MEETING_FOLLOW_UP_WORKFLOW: WorkflowAuditState = {
    "raw_input": """
    Capture meeting notes, decisions, and action items from the call recording or meeting document.
    Review the notes and confirm owners, deadlines, and unresolved questions.
    Update the CRM, project tracker, or shared workspace with decisions and next steps.
    Send a follow-up summary to attendees and stakeholders who need visibility.
    Track action items to completion and escalate overdue tasks before the next checkpoint meeting.
    Archive the final materials and update status reporting for leadership or the client team.
    """.strip()
}


SAMPLE_WORKFLOWS: dict[str, WorkflowAuditState] = {
    "customer_support": CUSTOMER_SUPPORT_WORKFLOW,
    "invoice_processing": INVOICE_PROCESSING_WORKFLOW,
    "sales_lead_qualification": SALES_LEAD_QUALIFICATION_WORKFLOW,
    "employee_onboarding": EMPLOYEE_ONBOARDING_WORKFLOW,
    "meeting_follow_up": MEETING_FOLLOW_UP_WORKFLOW,
}


SAMPLE_WORKFLOW_INPUT: WorkflowAuditState = INVOICE_PROCESSING_WORKFLOW
