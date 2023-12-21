from posts.models import Posts
from django.db.models import Q


class BaseQuerySet():
    def get_queryset(self, *args, **kwargs):
        user = self.request.user

        if hasattr(user, 'role'):
            if user.role == 'admin':
                return Posts.objects.all()
        
            if self.request.method == 'GET':
                # Check read permissions
                if user.is_authenticated:
                    return Posts.objects.filter(Q(read_permission='public') | Q(read_permission='authenticated') | Q(author=user) | Q(author__team=user.team) & Q(is_active=True))

            if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
                # Check edit permissions
                if user.is_authenticated:
                    return Posts.objects.filter(Q(edit_permission='public') | Q(edit_permission='authenticated') | Q(author=user) | Q(author__team=user.team) & Q(is_active=True))
        else:            
            return Posts.objects.filter(Q(read_permission='public'))
