from django.urls import path
from editor_app import views, generic_views

urlpatterns = [
    path('new_project/', views.new_project_view, name='new_project'),
    path('project_detail/', views.new_project_view, name='project_detail'),
    path('new-assignment/', views.fake_new_assignment_view, name='fake_new_assignment'),
    path('assignment-detail/<int:assignment_id>/', generic_views.assignment_detail_view, name='assignment_detail'),
    path('all-assignments/', generic_views.all_assignments_view, name='all_assignments'),
    path('my-assignments/', generic_views.my_assignments_view, name='my_assignments'),
]