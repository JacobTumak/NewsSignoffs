from signoffs.approvals import BaseApproval, ApprovalSignoff
from signoffs.registry import register

@register("NewProjectApproval")
class NewProjectApproval(BaseApproval):
    # TODO: Add Both Approval Signoffs here
    pass

