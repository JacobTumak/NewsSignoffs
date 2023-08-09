import django.core.exceptions
from django.shortcuts import render, HttpResponse
from editor_app.forms import ProjectForm
from editor_app.models import Project
from editor_app.approvals import NewProjectApproval


def new_project_view_old_ish(request):
    if not request.user.is_staff:
        return HttpResponse("You must be registered as staff to create a new project.")
    project_form = ProjectForm
    approval_form = NewProjectApproval.assign_project_signoff.forms.get_signoff_form

    if request.method == "POST":
        project_form = project_form(request.POST)
        # approval_form = approval_form(request.POST)
        if project_form.is_valid():
            project = project_form.save()
            # approve_assignment = project.approval
            approval_form = approval_form(request.POST)
            approval_form.clean()
            approval = approval_form.sign(user=request.user)
            approval.save()
            project.save()
            return render(request, 'editor_app/basic_rendered_approval.html', context={'project': project})
    return render(request, 'editor_app/new_project.html', context={'project_form': project_form,
                                                                   'approval_form': approval_form()})





def new_project_view(request):
    if not request.user.is_staff:
        return HttpResponse("You must be registered as staff to create a new project.")
    project_form = ProjectForm
    approval_form = NewProjectApproval.assign_project_signoff.forms.get_signoff_form

    if request.method == "POST":
        project_form = project_form(request.POST)
        approval_form = approval_form(request.POST).clean()
        if project_form.is_valid() and approval_form.is_valid():
            project = project_form.save(commit=False)
            approval = approval_form.sign(user=request.user)
            project.save()
            return render(request, 'editor_app/basic_rendered_approval.html', context={'project': project})
        else:
            print(f"\nproject_form: {project_form.is_valid()}\napproval_form: {approval_form.is_valid()}\n\n")
            # return HttpResponse(approval_form)
            raise django.core.exceptions.ValidationError("Invalid form")
    return render(request, 'editor_app/new_project.html', context={'project_form': project_form,
                                                                   'approval_form': approval_form()})

def project_detail_view(request):
    return new_project_view(request)