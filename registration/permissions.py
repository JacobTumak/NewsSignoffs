"""
Permissions logic
"""
from django.contrib.auth.models import User, Group, Permission
from .signoffs import terms_signoff
from django.contrib.contenttypes.models import ContentType



def has_signed_terms(user):
    """Return True iff the user has signed ToS"""
    signoff = terms_signoff.get(user=user)
    return signoff.is_signed()

# content_type = ContentType.objects.get(app_label='assignments', model='Assignment')
# create_assignment_perm = Permission.objects.create(codename='can_create_assignment',
#                                        name='Can create Assignment',
#                                        content_type=content_type)
#
# edit_assignment_perm = Permission.objects.create(codename='can_edit_assignment',
#                                        name='Can edit Assignment',
#                                        content_type=content_type)
#
#
#
# group = Group.objects.get(name='HR')
# group.permissions.add()
