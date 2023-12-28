from django.db import models

from base.models import BaseModel


class Posts(BaseModel):
    PERMISSIONS = [
        ('owner', 'Owner'),
        ('team', 'Team'),
        ('authenticated', 'Authenticated'),
        ('public', 'Public'),
    ]

    author = models.ForeignKey('user.CustomUsers', blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)
    read_permission = models.CharField(max_length=13, choices=PERMISSIONS, default='owner')
    edit_permission = models.CharField(max_length=13, choices=PERMISSIONS, default='owner')
