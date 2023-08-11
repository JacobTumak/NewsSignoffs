import django.core.exceptions
from django.shortcuts import render, HttpResponse
from editor_app.forms import AssignmentForm
from editor_app.models.models import Assignment
from editor_app.approvals import NewAssignmentApproval


def assignment_detail_view(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    return render(request, 'editor_app/project_detail.html', context={'assignment': assignment})


def my_assignments_view(request):
    page_title = "My Assignments"
    empty_text = "You have no assignments"
    if request.user.is_staff:
        return assignment_list_base_view(request, page_title, empty_text, assigned_by=request.user)
    return assignment_list_base_view(request, page_title, empty_text, assigned_to=request.user)


def all_assignments_view(request):
    page_title = "All Assignments"
    empty_text = "There are no assignments"
    return assignment_list_base_view(request, page_title, empty_text)


def assignment_list_base_view(request, page_title=None, empty_text=None, **filter_kwargs):
    empty_text = empty_text or "Assignments will appear here."
    if filter_kwargs:
        assignments = Assignment.objects.filter(**filter_kwargs)
    else:
        assignments = Assignment.objects.all()
    context = {'assignments': assignments,
               'page_title': page_title,
               "empty_text": empty_text}
    return render(request, 'editor_app/assignment_list_view.html', context=context)