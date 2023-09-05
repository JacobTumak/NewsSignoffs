from django.urls import path
from assignments import views, generic_views

urlpatterns = [
    path("new_project/", views.create_assignment_view, name="new_project"),
    # path("project_detail/", views.create_assignment_view, name="project_detail"),
    path("new-assignment/", views.create_assignment_view, name="new_assignment"),
    path("assignment-detail/<int:assignment_id>/", views.assignment_detail_view, name="assignment_detail",),
    path("all-assignments/", generic_views.all_assignments_view, name="all_assignments"),
    path("my-assignments/", generic_views.my_assignments_view, name="my_assignments"),
]
