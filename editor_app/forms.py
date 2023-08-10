from django.forms import ModelForm
from signoffs.forms import ApprovalSignoffForm
from signoffs.models import ApprovalSignet
import editor_app.models as models
from editor_app import approvals

class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = ['project_name', 'details', 'assigned_to']


# class NewProjectApprovalForm(ApprovalSignoffForm):
#     signoff_id = "editor_app.approvals.NewProjectApproval"
#     class Meta(ApprovalSignoffForm.Meta):
#         model = ApprovalSignet
#         fields = ['signed_off']