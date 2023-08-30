from signoffs.approvals import IrrevokableApproval
from signoffs.signoffs import SignoffRenderer


publication_request_signoff = IrrevokableApproval.register(
    id="publication_request_signoff",
    label="Submit for Publication",
    render=SignoffRenderer(
        form_context=dict(help_text="Publication Request - applicant signoff")
    ),
)

publication_approval_signoff = IrrevokableApproval.register(
    id="publication_approval_signoff",
    label="Publish Article",
    perms=["is_staff"],
    render=SignoffRenderer(
        form_context=dict(help_text="Publication Request - staff signoff")
    ),
)
