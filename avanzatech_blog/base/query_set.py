# DJANGO IMPORTS
from django.db.models import Q

# MODELS
from posts.models import Posts


class BasePostsQuerySet():
    def get_queryset(self, *args, **kwargs):
        user = self.request.user

        if hasattr(user, 'role'):
            if user.role == 'admin':
                return Posts.objects.all()

            if self.request.method == 'GET' or self.request.method == 'POST':
                # Check read permissions
                return Posts.objects.filter((Q(read_permission='public') | Q(read_permission='authenticated') | (Q(read_permission='team') & Q(author__team=user.team)) | (Q(read_permission='owner') & Q(author=user))) & Q(is_active=True))

            if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
                # Check edit permissions
                return Posts.objects.filter((Q(edit_permission='public') | Q(edit_permission='authenticated') | (Q(edit_permission='team') & Q(author__team=user.team)) | (Q(edit_permission='owner') & Q(author=user))) & Q(is_active=True))
        else:
            return Posts.objects.filter(Q(read_permission='public') & Q(is_active=True))
