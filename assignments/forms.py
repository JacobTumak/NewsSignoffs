from django.forms import ModelForm, Textarea, TextInput

from .models import Assignment


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ["assignment_name", "assigned_to", "details"]
        widgets = {
            "assignment_name": TextInput(attrs={"style": "width:75%"}),
            "details": Textarea(attrs={"rows": 4, "style": "width:100%"}),
        }
