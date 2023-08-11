from django.forms import ModelForm, TextInput, Textarea, HiddenInput
from signoffs.forms import ApprovalSignoffForm
from signoffs.models import ApprovalSignet
from editor_app.models.models import Assignment
from editor_app import approvals

class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['assignment_name', 'assigned_to', 'details']
        hidden = ['assigned_by']
        widgets = {
            'assignment_name': TextInput(attrs={'style': 'width:75%'}),
            'details': Textarea(attrs={'rows': 4, 'style': 'width:100%'}),
            'assigned_by': HiddenInput()
        }


# class NewProjectApprovalForm(ApprovalSignoffForm):
#     signoff_id = "editor_app.approvals.NewProjectApproval"
#     class Meta(ApprovalSignoffForm.Meta):
#         model = ApprovalSignet
#         fields = ['signed_off']