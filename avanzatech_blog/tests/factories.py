# FACTORY BOY
import factory

# MODELS
from user.models import CustomUsers
from posts.models import Posts
from likes.models import Likes
from comments.models import Comments


class CustomUsersFactory(factory.Factory):

    class Meta:
        model = CustomUsers


class PostsFactory(factory.Factory):

    class Meta:
        model = Posts


class LikesFactory(factory.Factory):

    class Meta:
        model = Likes


class CommentsFactory(factory.Factory):

    class Meta:
        model = Comments
