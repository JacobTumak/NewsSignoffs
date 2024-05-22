"""
CRUD and list views for Assignment app
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
# from django.contrib.auth.models import Permission
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, reverse
from django.db.models import Q

from .forms import AssignmentForm
from .models import Assignment
from ..registration import permissions


@login_required
@user_passes_test(permissions.has_signed_terms, login_url="terms_of_service")
def create_assignment_view(request):
    if not request.user.has_perm("assignments.add_assignment"):
        messages.error(
            request, "You don't have permission to create an assignment."
        )

    form = AssignmentForm

    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid() and request.user.has_perm("assignments.add_assignment"):
            assignment = form.save(commit=False)
            assignment.assigned_by = request.user
            assignment.save()
            return HttpResponseRedirect(
                reverse("assignment:detail", args=(assignment.id,))
            )
    context = {
        "form": form,
    }
    return render(
        request,
        "assignments/create_assignment.html",
        context=context,
    )


@login_required
@user_passes_test(permissions.has_signed_terms, login_url="terms_of_service")
def assignment_detail_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    # signoff = assignment.approval.get_next_signoff(for_user=request.user)
    if request.method == "POST": # and signoff:
        return sign_assignment_view(request, assignment_id)
    else:
        context = {"assignment": assignment}#, "signoff": signoff}
        return render(request, "assignments/assignment_detail.html", context=context)


@login_required
@user_passes_test(permissions.has_signed_terms, login_url="terms_of_service")
def sign_assignment_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    signoff = assignment.approval.get_next_signoff(for_user=request.user)
    if request.method == "POST" and signoff:
        signoff_form = signoff.forms.get_signoff_form(request.POST)
        if signoff_form.is_valid() and signoff_form.is_signed_off():

            print(signoff_form.cleaned_data)

            signoff.sign(request.user, commit=True)
            assignment.bump_status()
            assignment.save()
        else:
            messages.error(request, "You must check the box before submitting signoff")
    return HttpResponseRedirect(reverse("assignment:detail", args=(assignment.id,)))


# List views

def my_assignments_view(request):
    page_title = "My Assignments"
    empty_text = "You have no assignments"
    return assignment_list_base_view(
        request, page_title, empty_text, Q(assigned_by=request.user) | Q(assigned_to=request.user)
    )


def all_assignments_view(request):
    page_title = "All Assignments"
    empty_text = "There are no assignments"
    return assignment_list_base_view(request, page_title, empty_text)


@login_required
@user_passes_test(permissions.has_signed_terms, login_url="terms_of_service")
def assignment_list_base_view(
    request, page_title=None, empty_text=None, query=None
):
    empty_text = empty_text or "Assignments will appear here."

    assignments = Assignment.objects.filter(query) if query else Assignment.objects.all()

    context = {
        "assignments": assignments,
        "page_title": page_title,
        "empty_text": empty_text,
    }
    return render(request, "assignments/assignment_list_view.html", context=context)
