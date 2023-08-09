from signoffs.approvals import SimpleApproval, ApprovalSignoff, BaseApproval
# from signoffs.approvals.signing_order import SigningOrder
from signoffs.core.signing_order import SigningOrder
from signoffs.models import Stamp
from signoffs.registry import register


#TODO: Why do I need to define a stamp for the Approval class and the Signoffs it contains? Why not just either/or?
@register("editor_app.approvals.NewProjectApproval")
class NewProjectApproval(BaseApproval):
    S = ApprovalSignoff
    stampModel = Stamp
    label = "New Assignment"

    assign_project_signoff = S.register(
        stampModel=Stamp,
        id="assign_project_signoff",
        label="Assign Project",
        perm="is_staff",
    )

    confirm_project_signoff  = S.register(
        stampModel=Stamp,
        id="confirm_project_signoff",
        label="Project Confirmation",
    )

    signing_order = SigningOrder(
        assign_project_signoff,
        confirm_project_signoff
    )
