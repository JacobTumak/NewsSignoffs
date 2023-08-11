from django.db import models
from django.contrib.auth.models import User
from signoffs.models import ApprovalField
from editor_app.approvals import NewAssignmentApproval


class Assignment(models.Model):
    assignment_name = models.CharField(max_length=200)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_assigned_by", null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_assigned_to", null=True)
    details = models.TextField(max_length=1000)
    approval, approval_stamp = ApprovalField(NewAssignmentApproval)

    def assignee(self):
        if self.assigned_to.get_full_name():
            return self.assigned_to.get_full_name()
        else:
            return self.assigned_to.username
