# DJANGO IMPORTS
from django.db import models

# MODELS
from base.models import BaseModel


class Posts(BaseModel):
    PERMISSIONS = [
        ('owner', 'Owner'),
        ('team', 'Team'),
        ('authenticated', 'Authenticated'),
        ('public', 'Public'),
    ]

    author = models.ForeignKey('user.CustomUsers', blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True, blank=True)
    content = models.TextField(blank=True)
    read_permission = models.CharField(max_length=13, choices=PERMISSIONS, default='owner')
    edit_permission = models.CharField(max_length=13, choices=PERMISSIONS, default='owner')
