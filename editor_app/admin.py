from django.contrib import admin
from editor_app.models.models import Assignment
from signoffs.models import Stamp

admin.site.register(Assignment)
admin.site.register(Stamp)
