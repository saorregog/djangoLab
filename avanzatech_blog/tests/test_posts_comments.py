# DJANGO IMPORTS
from django.urls import reverse

# DJANGO REST FRAMEWORK IMPORTS
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# MODELS
from user.models import CustomUsers
from posts.models import Posts
from comments.models import Comments

# FACTORIES
from . import factories


class PostsListComments(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('posts-list_comments', kwargs={'pk': 1})
        self.user = factories.CustomUsersFactory()
    
    def test_1_access_to_browsable_api_by_authenticated_admins(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1)).save()

        factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=1)).save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [{'id': 1, 'user': 1, 'post': 1, 'content': ''}])
    
    def test_2_access_to_browsable_api_by_authenticated_bloggers(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1)).save()

        factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=1)).save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [{'id': 1, 'user': 1, 'post': 1, 'content': ''}])
    
    def test_3_access_to_browsable_api_by_unauthenticated_users(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), read_permission='public').save()

        factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=1)).save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [{'id': 1, 'user': 1, 'post': 1, 'content': ''}])
    
    def test_4_list_all_comments_from_posts_visible_for_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        for i in range(1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=i)).save()

            response = self.client.get(reverse('posts-list_comments', kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['results'], [{'id': i, 'user': 1, 'post': i, 'content': ''}])
    
    def test_5_list_all_comments_from_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_blogger_from_same_team(self):
        self.user.role = 'blogger'
        self.user.team = 'team 1'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 1').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        for i in range(1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=2), post=Posts.objects.get(pk=i)).save()

            response = self.client.get(reverse('posts-list_comments', kwargs={'pk': i}))

            if i == 1:
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
            else:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['results'], [{'id': i, 'user': 2, 'post': i, 'content': ''}])
    
    def test_6_list_all_comments_from_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_blogger_from_different_team(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 2').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        for i in range(1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=2), post=Posts.objects.get(pk=i)).save()

            response = self.client.get(reverse('posts-list_comments', kwargs={'pk': i}))

            if i == 1 or i == 2:
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
            else:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['results'], [{'id': i, 'user': 2, 'post': i, 'content': ''}])
    
    def test_7_list_all_comments_from_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_him_or_herself(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        for i in range(1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=i)).save()

            response = self.client.get(reverse('posts-list_comments', kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['results'], [{'id': i, 'user': 1, 'post': i, 'content': ''}])
    
    def test_8_list_all_comments_from_posts_visible_for_unauthenticated_user(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        for i in range(1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=i)).save()

            response = self.client.get(reverse('posts-list_comments', kwargs={'pk': i}))

            if i == 4:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['results'], [{'id': i, 'user': 1, 'post': i, 'content': ''}])
            else:
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_9_list_all_comments_from_posts_visible_for_authenticated_admin_if_some_posts_were_deleted(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)
    
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', is_active=False).save()

        for i in range(1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=i)).save()

            response = self.client.get(reverse('posts-list_comments', kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['results'], [{'id': i, 'user': 1, 'post': i, 'content': ''}])
    
    def test_10_list_all_comments_from_posts_visible_for_authenticated_blogger_if_he_or_she_is_author_of_all_posts_and_some_posts_were_deleted(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', is_active=False).save()

        for i in range(1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=i)).save()

            response = self.client.get(reverse('posts-list_comments', kwargs={'pk': i}))

            if i == 1 or i == 3:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['results'], [{'id': i, 'user': 1, 'post': i, 'content': ''}])
            else:
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_11_list_all_comments_from_posts_visible_for_unauthenticated_user_if_all_posts_have_public_read_permission_and_some_posts_were_deleted(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='public').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='public', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='public').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public', is_active=False).save()

        for i in range(1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=i)).save()

            response = self.client.get(reverse('posts-list_comments', kwargs={'pk': i}))

            if i == 1 or i == 3:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['results'], [{'id': i, 'user': 1, 'post': i, 'content': ''}])
            else:
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_12_list_all_comments_from_non_existent_post_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='public').save()

        factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=1)).save()

        response = self.client.get(reverse('posts-list_likes', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_13_list_all_comments_from_non_existent_post_by_authenticated_blogger(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='public').save()

        factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=1)).save()

        response = self.client.get(reverse('posts-list_likes', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_14_list_all_comments_from_non_existent_post_by_unauthenticated_user(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='public').save()

        factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=1)).save()

        response = self.client.get(reverse('posts-list_likes', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_15_results_pagination_for_unauthenticated_user_if_all_posts_have_public_read_permission(self):
        factories.CustomUsersFactory(email='test_1@example.com').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='public').save()

        for i in range(1, 16):
            factories.CustomUsersFactory(email=f'test_{i + 1}@example.com').save()

            factories.CommentsFactory(user=CustomUsers.objects.get(pk=i + 1), post=Posts.objects.get(pk=1)).save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 2)
        self.assertEqual(response.data['total_count'], 15)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 10)


class PostsComment(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('posts-comment', kwargs={'pk': 1})
        self.user = factories.CustomUsersFactory()
    
    def test_1_access_to_browsable_api_by_authenticated_admins(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], 'Method \"GET\" not allowed.')
    
    def test_2_access_to_browsable_api_by_authenticated_bloggers(self):
        self.user.role = 'blogger'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], 'Method \"GET\" not allowed.')
    
    def test_3_access_to_browsable_api_by_unauthenticated_users(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_4_comment_all_posts_visible_for_authenticated_admin(self):
        self.user.role = 'admin'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        for i in range (1, 5):
            data = {'content': 'Lorem Ipsum'}

            response = self.client.post(reverse('posts-comment', kwargs={'pk': i}), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, {'content': 'Lorem Ipsum'})
            self.assertTrue(Comments.objects.filter(post__id=i).exists())
    
    def test_5_comment_all_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_blogger_from_same_team(self):
        self.user.role = 'blogger'
        self.user.team = 'team 1'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 1').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        for i in range (1, 5):
            data = {'content': 'Lorem Ipsum'}

            response = self.client.post(reverse('posts-comment', kwargs={'pk': i}), data, format='json')

            if i == 1:
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
                self.assertFalse(Comments.objects.filter(post__id=i).exists())
            else:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(response.data, {'content': 'Lorem Ipsum'})
                self.assertTrue(Comments.objects.filter(post__id=i).exists())
    
    def test_6_comment_all_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_blogger_from_different_team(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 1').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        for i in range (1, 5):
            data = {'content': 'Lorem Ipsum'}

            response = self.client.post(reverse('posts-comment', kwargs={'pk': i}), data, format='json')

            if i == 1 or i == 2:
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
                self.assertFalse(Comments.objects.filter(post__id=i).exists())
            else:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(response.data, {'content': 'Lorem Ipsum'})
                self.assertTrue(Comments.objects.filter(post__id=i).exists())
    
    def test_7_comment_all_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_him_or_herself(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        for i in range (1, 5):
            data = {'content': 'Lorem Ipsum'}

            response = self.client.post(reverse('posts-comment', kwargs={'pk': i}), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, {'content': 'Lorem Ipsum'})
            self.assertTrue(Comments.objects.filter(post__id=i).exists())
    
    def test_8_comment_all_posts_visible_for_unauthenticated_user(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        for i in range (1, 5):
            data = {'content': 'Lorem Ipsum'}

            response = self.client.post(reverse('posts-comment', kwargs={'pk': i}), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_9_comment_all_posts_visible_for_authenticated_admin_if_some_posts_were_deleted(self):
        self.user.role = 'admin'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', is_active=False).save()

        for i in range (1, 5):
            data = {'content': 'Lorem Ipsum'}

            response = self.client.post(reverse('posts-comment', kwargs={'pk': i}), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, {'content': 'Lorem Ipsum'})
            self.assertTrue(Comments.objects.filter(post__id=i).exists())
    
    def test_10_comment_all_posts_visible_for_authenticated_blogger_if_he_or_she_is_author_of_all_posts_and_some_posts_were_deleted(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', is_active=False).save()

        for i in range (1, 5):
            data = {'content': 'Lorem Ipsum'}

            response = self.client.post(reverse('posts-comment', kwargs={'pk': i}), data, format='json')

            if i == 1 or i == 3:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(response.data, {'content': 'Lorem Ipsum'})
                self.assertTrue(Comments.objects.filter(post__id=i).exists())
            else:
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
                self.assertFalse(Comments.objects.filter(post__id=i).exists())
    
    def test_10_new_comment_creation_without_content_by_authenticated_user(self):
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=self.user, title='Post 1').save()

        data = {}

        response = self.client.post(reverse('posts-comment', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], ['Comments must have content.'])
    
    def test_11_comment_non_existent_post_by_authenticated_user(self):
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=self.user, title='Post 1').save()

        data = {'content': 'Lorem Ipsum'}

        response = self.client.post(reverse('posts-comment', kwargs={'pk': 2}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')


class PostsDeleteComment(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('posts-delete_comment', kwargs={'pk': 1}) + '?comment_id=1'
        self.user = factories.CustomUsersFactory()
    
    def test_1_access_to_browsable_api_by_authenticated_admins(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], 'Method \"GET\" not allowed.')
    
    def test_2_access_to_browsable_api_by_authenticated_bloggers(self):
        self.user.role = 'blogger'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], 'Method \"GET\" not allowed.')
    
    def test_3_access_to_browsable_api_by_unauthenticated_users(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_4_delete_comments_in_all_posts_visible_for_authenticated_admin_if_posts_and_comments_were_created_by_blogger(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        for i in range (1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=i)).save()

            response = self.client.delete(reverse('posts-delete_comment', kwargs={'pk': i}) + f'?comment_id={i}')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(response.data, None)
            self.assertFalse(Comments.objects.get(post__id=i).is_active)
    
    def test_5_delete_comments_in_all_posts_visible_for_authenticated_blogger_if_posts_and_comments_were_created_by_blogger_from_same_team(self):
        self.user.role = 'blogger'
        self.user.team = 'team 1'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 1').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        for i in range (1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=2), post=Posts.objects.get(pk=i)).save()

            response = self.client.delete(reverse('posts-delete_comment', kwargs={'pk': i}) + f'?comment_id={i}')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data['detail'], 'Not found.')
            self.assertTrue(Comments.objects.get(post__id=i).is_active)
    
    def test_6_delete_comments_in_all_posts_visible_for_authenticated_blogger_if_posts_and_comments_were_created_by_blogger_from_different_team(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 2').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        for i in range (1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=2), post=Posts.objects.get(pk=i)).save()

            response = self.client.delete(reverse('posts-delete_comment', kwargs={'pk': i}) + f'?comment_id={i}')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data['detail'], 'Not found.')
            self.assertTrue(Comments.objects.get(post__id=i).is_active)
    
    def test_7_delete_comments_in_all_posts_visible_for_authenticated_blogger_if_posts_and_comments_were_created_by_him_or_herself(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 2').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        for i in range (1, 5):
            factories.CommentsFactory(user=CustomUsers.objects.get(pk=1), post=Posts.objects.get(pk=i)).save()

            response = self.client.delete(reverse('posts-delete_comment', kwargs={'pk': i}) + f'?comment_id={i}')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(response.data, None)
            self.assertFalse(Comments.objects.get(post__id=i).is_active)
