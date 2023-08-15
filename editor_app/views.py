import django.core.exceptions
import signoffs.models
from django.shortcuts import render, HttpResponse
from signoffs.forms import signoff_form_factory
from editor_app.forms import AssignmentForm
from editor_app.models.models import Assignment
from editor_app.approvals import NewAssignmentApproval


def new_project_view_old(request):
    if not request.user.is_staff:
        return HttpResponse("You must be registered as staff to create a new assignment.")
    assignment_form = AssignmentForm
    signoff_form = signoff_form_factory(signoff_type=NewAssignmentApproval.assign_project_signoff)

    # signoff_form = NewAssignmentApproval.assign_project_signoff.forms.get_signoff_form

    if request.method == "POST":
        assignment_form = assignment_form(request.POST)
        signoff_form = signoff_form(request.POST)
        if assignment_form.is_valid() and signoff_form.is_valid():
            assignment = assignment_form.save()
            signoff = NewAssignmentApproval.assign_project_signoff.get(Assignment = assignment)
            signoff.sign(request.user)
            # get next signoff from approval.
            # sign it
            # approve_assignment = assignment.approval
            signoff_form = signoff_form(request.POST)
            approval = signoff_form.sign(user=request.user)
            approval.save()
            assignment.save()
            return render(request, 'editor_app/basic_rendered_approval.html', context={'assignment': assignment})
    return render(request, 'editor_app/new_project.html', context={'assignment_form': assignment_form,
                                                                   'signoff_form': signoff_form()})


def new_project_view(request):
    if not request.user.is_staff:
        return HttpResponse("You must be registered as staff to create a new project.")

    signoff_form = signoff_form_factory(signoff_type=NewAssignmentApproval.assign_project_signoff)

    assignment_form = AssignmentForm
    if request.method == "POST":
        assignment_form = assignment_form(request.POST)
        signoff_form = signoff_form(request.POST)
        if assignment_form.is_valid() and signoff_form.is_valid():
            signoff = signoff_form.save(commit=False)
            assignment = assignment_form.save(commit=False)
            assignment = signoff
            assignment.save()
            return render(request, 'editor_app/basic_rendered_approval.html', context={'assignment': assignment})
        else:
            print(f"\nassignment_form: {assignment_form.is_valid()}\napproval_form: {signoff_form.is_valid()}\n\n")
            # return HttpResponse(approval_form)
            raise django.core.exceptions.ValidationError("Invalid form")
    return render(request, 'editor_app/new_project.html', context={'assignment_form': assignment_form,
                                                                   'signoff_form': signoff_form})


def fake_new_assignment_view(request):
    if not request.user.is_staff:
        return HttpResponse("You must be registered as staff to create a new project.")

    form = AssignmentForm
    signoff_form = NewAssignmentApproval.assign_project_signoff.forms.get_signoff_form
    signoff = NewAssignmentApproval.assign_project_signoff.get()

    # signoff_form = Assignment.approval.get_next_signoff()
    if request.method == "POST":
        form = form(request.POST)
        signoff_form = signoff_form(request.POST)
        print(signoff_form, signoff_form.is_valid())
        if form.is_valid() and signoff_form.is_valid():
            assignment = form.save(commit=False)
            assignment.assigned_by = request.user
            assignment.save()
            return render(request, 'editor_app/project_detail.html', context={'assignment': assignment})
        else:
            return render(request, 'editor_app/demo_new_assignment.html', context={'form': form,
                                                                                   "signoff_form": signoff_form,
                                                                            'assignment_approval': NewAssignmentApproval(),
                                                                            'messages': signoff_form.errors})

    return render(request, 'editor_app/demo_new_assignment.html', context={'form': form,
                                                                           'signoff_form': signoff_form,
                                                                       'assignment_approval': NewAssignmentApproval()})


def project_detail_view(request):
    return new_project_view(request)