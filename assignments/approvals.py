from django.contrib.auth.models import User, Permission
from django.utils.functional import SimpleLazyObject

from signoffs.approvals import ApprovalSignoff, SimpleApproval
from signoffs.core.signoffs import DefaultSignoffBusinessLogic
from signoffs.models import ApprovalSignet
from signoffs.registry import register
from signoffs.signing_order import SigningOrder

# add_assignment_perm = Permission.objects.get(codename="add_assignment")
# class AssignmentAssignerApprovalLogic(DefaultSignoffBusinessLogic):
#     perm = add_assignment_perm



@register("assignments.approvals.NewAssignmentApproval")
class NewAssignmentApproval(SimpleApproval):
    S = ApprovalSignoff
    label = "Signoff for New Assignment"

    assign_project_signoff = S.register(
        signetModel=ApprovalSignet,
        id="assign_project_signoff",
        label="Assign Project",
        logic=DefaultSignoffBusinessLogic(perm="assignments.add_assignment"),
    )

    accept_project_signoff = S.register(
        signetModel=ApprovalSignet,
        id="accept_project_signoff",
        label="Accept Assignment",
    )

    submit_completed_signoff = S.register(
        signetModel=ApprovalSignet,
        id="submit_completed_signoff",
    )

    confirm_completion_signoff = S.register(
        signetModel=ApprovalSignet,
        id="confirm_completion_signoff",
        label="Confirm Completion",
        logic=DefaultSignoffBusinessLogic(perm="assignments.add_assignment"),
    )

    signing_order = SigningOrder(
        assign_project_signoff,  # pending
        accept_project_signoff,  # In-Progress
        submit_completed_signoff,  # submitted
        confirm_completion_signoff,  # completed - unrevokable?
    )

    def next_signoffs(self, for_user=None):
        if not for_user:
            return super().next_signoffs()
        if not type(for_user) in (User, SimpleLazyObject):
            raise TypeError(f"var \"for_user\" must be User instance, instead got {type(for_user)}\n")

        queried_signoffs = super().next_signoffs(for_user=for_user)

        assignment = self.subject
        if queried_signoffs:
            next_signoff_type = type(queried_signoffs[0])
            if (for_user == assignment.assigned_by and next_signoff_type in [self.assign_project_signoff, self.confirm_completion_signoff]) or\
                    (for_user == assignment.assigned_to and next_signoff_type in [self.accept_project_signoff, self.submit_completed_signoff]):
                return super().next_signoffs(for_user=for_user)
        return []

# class AssignmentApprovalBusinessLogic(DefaultApprovalBusinessLogic):
#     def can_sign(self, approval, user, signoff=None):
#         return user.has_perm("assignments.can_create_assignment") and super().can_sign(approval, user, signoff)

