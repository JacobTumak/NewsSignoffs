from django.urls import path
from editor_app import views

urlpatterns = [
    path('new_project/', views.new_project_view, name='new_project'),
    path('project_detail/', views.new_project_view, name='project_detail'),
]