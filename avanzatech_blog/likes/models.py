from django.db import models

from base.models import BaseModel


class Likes(BaseModel):
    user = models.ForeignKey('user.CustomUsers', blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Posts', blank=True, on_delete=models.CASCADE)
