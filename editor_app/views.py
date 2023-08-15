import django.core.exceptions
import signoffs.models
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse, get_object_or_404
from signoffs.forms import signoff_form_factory
from editor_app.forms import AssignmentForm
from editor_app.models.models import Assignment
from editor_app.approvals import NewAssignmentApproval


def create_assignment_view(request):
    if not request.user.is_staff:
        raise django.core.exceptions.PermissionDenied("You must be registered as staff to create a new project.")
    form = AssignmentForm

    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.save()
            return HttpResponseRedirect(reverse("assignment_detail", args=(assignment.id,)))
    return render(request, 'editor_app/create_assignment.html', context={'form': form,})

def assignment_detail_view(request, assignment_id):
    if not request.user.is_staff:
        raise django.core.exceptions.PermissionDenied("You must be registered as staff to create a new project.")

    # The Assignment object must exist already for a detail_view - get it
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    # A. it would be better to maintain a separate view to handle the signoff POSTs - lets circle back to that
    if request.method == "POST":
        signoff = assignment.approval.get_next_signoff(for_user=request.user)
        signoff_form = signoff.forms.get_signoff_form(request.POST)
        if signoff_form.is_valid():
            signoff_form.sign(request.user)

    return render(request, 'editor_app/project_detail.html', context={'assignment': assignment})
