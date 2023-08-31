from django.contrib import admin
from assignments.models import Assignment
from signoffs.models import Stamp

admin.site.register(Assignment)
admin.site.register(Stamp)
