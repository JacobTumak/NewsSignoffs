import django.core.exceptions
from django.shortcuts import (
    render,
    HttpResponseRedirect,
    reverse,
    get_object_or_404,
)
from assignments.forms import AssignmentForm
from assignments.models import Assignment


def create_assignment_view(request):
    if not request.user.is_staff:
        raise django.core.exceptions.PermissionDenied(
            "You must be registered as staff to create a new project."
        )
    form = AssignmentForm

    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid():
            assignment = form.save()
            return HttpResponseRedirect(
                reverse("assignment_detail", args=(assignment.id,))
            )
    context = {"form": form, }
    return render(request, "assignments/create_assignment.html", context=context, )


def assignment_detail_view(request, assignment_id):
    if not request.user.is_staff:
        raise django.core.exceptions.PermissionDenied("You must be registered as staff to create a new project.")

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == "POST":
        return assignment_signoffs_view(request, assignment_id)
    else:
        context = {"assignment": assignment}
        return render(request, "assignments/project_detail.html", context=context)

def assignment_signoffs_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        signoff = assignment.approval.get_next_signoff(for_user=request.user)
        signoff_form = signoff.forms.get_signoff_form(request.POST)
        if signoff_form.is_valid():
            signoff_form.sign(request.user)
    return HttpResponseRedirect(reverse("assignments/project_detail", args=(assignment.id,)))
