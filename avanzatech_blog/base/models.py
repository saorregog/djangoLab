# DJANGO IMPORTS
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("created at"), auto_now=True)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        abstract = True
        ordering = ['created_at']
