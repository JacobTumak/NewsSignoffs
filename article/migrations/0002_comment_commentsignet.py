# Generated by Django 3.2.20 on 2023-08-09 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signoffs_signets', '0001_initial'),
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=250)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommentSignet',
            fields=[
                ('signet_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='signoffs_signets.signet')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signatories', to='article.comment')),
            ],
            options={
                'ordering': ['timestamp'],
                'abstract': False,
            },
            bases=('signoffs_signets.signet',),
        ),
    ]