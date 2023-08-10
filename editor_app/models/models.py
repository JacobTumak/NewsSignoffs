from django.db import models
from django.contrib.auth.models import User
from signoffs.models import ApprovalField, SignoffField
from editor_app.approvals import NewProjectApproval

class Project(models.Model):
    project_name = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_assigned_to", null=True)
    details = models.TextField(max_length=1000)
    approval, approval_stamp = ApprovalField(NewProjectApproval)
