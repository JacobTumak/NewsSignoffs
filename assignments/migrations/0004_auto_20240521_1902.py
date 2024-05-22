# Generated by Django 3.2.20 on 2024-05-21 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignments', '0003_assignment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='assigned_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_assignment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_assignment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('requested', 'Requested'), ('in_progress', 'In Progress'), ('pending_review', 'Pending Review'), ('completed', 'Completed')], default='draft', max_length=15),
        ),
    ]
