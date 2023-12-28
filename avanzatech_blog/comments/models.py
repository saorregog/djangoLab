from django.db import models

from base.models import BaseModel


class Comments(BaseModel):
    user = models.ForeignKey('user.CustomUsers', blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Posts', blank=True, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
