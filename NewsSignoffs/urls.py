from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('article.urls')),
    path('', include('assignments.urls')),
    path('admin/', admin.site.urls),
]
