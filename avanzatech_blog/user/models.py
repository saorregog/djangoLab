from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        
        email = self.normalize_email(email)        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('role') != 'admin':
            raise ValueError(_('Superuser must have role=admin.'))

        return self.create_user(email, password, **extra_fields)


class CustomUsers(AbstractBaseUser, BaseModel, PermissionsMixin):
    ROLES = [
        ('blogger', 'Blogger'),
        ('admin', 'Admin')
    ]

    email = models.EmailField(_('email address'), unique=True, blank=True)
    password = models.CharField(_("password"), max_length=128, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, null=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=True)
    role = models.CharField(_('role'), max_length=7, choices=ROLES, default='blogger')
    team = models.CharField(_('team'), max_length=30, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
