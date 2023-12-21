from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class Posts(BaseModel):
    PERMISSIONS = [
        ('owner', 'Owner'),
        ('team', 'Team'),
        ('authenticated', 'Authenticated'),
        ('public', 'Public'),
    ]

    author = models.ForeignKey('user.CustomUsers', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    read_permission = models.CharField(max_length=13, choices=PERMISSIONS, default='owner')
    edit_permission = models.CharField(max_length=13, choices=PERMISSIONS, default='owner')
