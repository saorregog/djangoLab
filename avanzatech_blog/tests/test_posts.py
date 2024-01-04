# DJANGO IMPORTS
from django.urls import reverse

# DJANGO REST FRAMEWORK IMPORTS
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# MODELS
from user.models import CustomUsers
from posts.models import Posts

# FACTORIES
from . import factories


class PostsList(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('posts-list')
        self.user = factories.CustomUsersFactory()
    
    def test_1_access_to_browsable_api_by_authenticated_admins(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])
    
    def test_2_access_to_browsable_api_by_authenticated_bloggers(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])
    
    def test_3_access_to_browsable_api_by_unauthenticated_users(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])
    
    def test_4_list_all_posts_visible_for_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 4)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 4)
    
    def test_5_list_all_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_blogger_from_same_team(self):
        self.user.role = 'blogger'
        self.user.team = 'team 1'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 1').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 3)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 3)

    def test_6_list_all_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_blogger_from_different_team(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 2').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 2)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 2)
    
    def test_7_list_all_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_him_or_herself(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 4)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 4)
    
    def test_8_list_all_posts_visible_for_authenticated_blogger_if_he_or_she_is_author_of_first_post(self):
        self.user.role = 'blogger'
        self.user.team = 'team 1'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 2').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 3)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 3)
    
    def test_9_list_all_posts_visible_for_authenticated_blogger_if_he_or_she_is_author_of_second_post(self):
        self.user.role = 'blogger'
        self.user.team = 'team 1'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 2').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 3)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 3)
    
    def test_10_list_all_posts_visible_for_authenticated_blogger_if_he_or_she_is_author_of_third_post(self):
        self.user.role = 'blogger'
        self.user.team = 'team 1'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 2').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 2)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 2)
    
    def test_11_list_all_posts_visible_for_authenticated_blogger_if_he_or_she_is_author_of_fourth_post(self):
        self.user.role = 'blogger'
        self.user.team = 'team 1'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 2').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 2)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 2)
    
    def test_12_list_all_posts_visible_for_unauthenticated_user(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 1)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 1)
    
    def test_13_list_all_posts_visible_for_authenticated_admin_if_some_posts_were_deleted(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', is_active=False).save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 4)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 4)
    
    def test_14_list_all_posts_visible_for_authenticated_blogger_if_he_or_she_is_author_of_all_posts_and_some_posts_were_deleted(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', is_active=False).save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 2)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 2)
    
    def test_15_list_all_posts_visible_for_unauthenticated_user_if_all_posts_have_public_read_permission_and_some_posts_were_deleted(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='public').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='public', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='public').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public', is_active=False).save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 1)
        self.assertEqual(response.data['total_count'], 2)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 2)
    
    def test_16_results_pagination_for_unauthenticated_user_if_all_posts_have_public_read_permission(self):
        factories.CustomUsersFactory().save()

        for i in range(1, 16):
            factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title=f'Post {i}', read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 2)
        self.assertEqual(response.data['total_count'], 15)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 10)


class PostsRetrieve(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('posts-retrieve', kwargs={'pk': 1})
        self.user = factories.CustomUsersFactory()
    
    def test_1_access_to_browsable_api_by_authenticated_admins(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'author': 1, 'title': '', 'content': ''})
    
    def test_2_access_to_browsable_api_by_authenticated_bloggers(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'author': 2, 'title': '', 'content': ''})
    
    def test_3_access_to_browsable_api_by_unauthenticated_users(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), read_permission='public').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'author': 1, 'title': '', 'content': ''})
    
    def test_4_retrieve_posts_visible_for_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        for i in range(1, 5):
            response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {'author': 1, 'title': f'Post {i}', 'content': ''})
    
    def test_5_retrieve_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_blogger_from_same_team(self):
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
            if i == 1:
                response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
            else:
                response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data, {'author': 2, 'title': f'Post {i}', 'content': ''})
    
    def test_6_retrieve_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_blogger_from_different_team(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 2').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', read_permission='public').save()

        for i in range(1, 5):
            if i == 1 or i == 2:
                response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
            else:
                response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data, {'author': 2, 'title': f'Post {i}', 'content': ''})
    
    def test_7_retrieve_posts_visible_for_authenticated_blogger_if_posts_were_posted_by_him_or_herself(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        for i in range(1, 5):
            response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {'author': 1, 'title': f'Post {i}', 'content': ''})
    
    def test_8_retrieve_posts_visible_for_unauthenticated_user(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public').save()

        for i in range(1, 5):
            if i == 4:
                response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data, {'author': 1, 'title': f'Post {i}', 'content': ''})
            else:
                response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_9_retrieve_posts_visible_for_authenticated_admin_if_some_posts_were_deleted(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', is_active=False).save()

        for i in range(1, 5):
            response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {'author': 1, 'title': f'Post {i}', 'content': ''})
    
    def test_10_retrieve_posts_visible_for_authenticated_blogger_if_he_or_she_is_author_of_all_posts_and_some_posts_were_deleted(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', is_active=False).save()

        for i in range(1, 5):
            if i == 1 or i == 3:
                response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data, {'author': 1, 'title': f'Post {i}', 'content': ''})
            else:
                response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_11_retrieve_posts_visible_for_unauthenticated_user_if_all_posts_have_public_read_permission_and_some_posts_were_deleted(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', read_permission='public').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', read_permission='public', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', read_permission='public').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', read_permission='public', is_active=False).save()

        for i in range(1, 5):
            if i == 1 or i == 3:
                response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data, {'author': 1, 'title': f'Post {i}', 'content': ''})
            else:
                response = self.client.get(reverse('posts-retrieve', kwargs={'pk': i}))
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_12_retrieve_non_existent_post_for_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('posts-retrieve', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_13_retrieve_non_existent_post_for_authenticated_blogger(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('posts-retrieve', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_14_retrieve_non_existent_post_for_unauthenticated_user(self):
        response = self.client.get(reverse('posts-retrieve', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')


class PostsCreate(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('posts-create')
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
    
    def test_3_forbidden_access_to_browsable_api_by_unauthenticated_users(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_4_new_post_creation_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        data = {'title': 'Post 1', 'content': 'Lorem Ipsum', 'read_permission': 'public', 'edit_permission': 'authenticated'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'title': 'Post 1', 'content': 'Lorem Ipsum', 'read_permission': 'public', 'edit_permission': 'authenticated'})
        self.assertEqual(Posts.objects.get(pk=1).author.id, 1)
        self.assertEqual(Posts.objects.get(pk=1).author.role, 'admin')
    
    def test_5_new_post_creation_by_authenticated_blogger(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        data = {'title': 'Post 1', 'content': 'Lorem Ipsum', 'read_permission': 'public', 'edit_permission': 'authenticated'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'title': 'Post 1', 'content': 'Lorem Ipsum', 'read_permission': 'public', 'edit_permission': 'authenticated'})
        self.assertEqual(Posts.objects.get(pk=1).author.id, 1)
        self.assertEqual(Posts.objects.get(pk=1).author.role, 'blogger')
    
    def test_6_forbidden_new_post_creation_by_unauthenticated_user(self):
        data = {'title': 'Post 1', 'content': 'Lorem Ipsum', 'read_permission': 'public', 'edit_permission': 'authenticated'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_7_new_post_creation_with_existing_title_by_authenticated_user(self):
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=self.user, title='Post 1', content='Lorem Ipsum', read_permission='public', edit_permission='authenticated').save()

        data = {'title': 'Post 1', 'content': 'Lorem Ipsum', 'read_permission': 'public', 'edit_permission': 'authenticated'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['title'], ['posts with this title already exists.'])
    
    def test_8_new_post_creation_without_permissions_by_authenticated_user(self):
        self.user.save()
        self.client.force_authenticate(user=self.user)

        data = {'title': 'Post 1', 'content': 'Lorem Ipsum'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'title': 'Post 1', 'content': 'Lorem Ipsum', 'read_permission': 'owner', 'edit_permission': 'owner'})
        self.assertEqual(Posts.objects.get(pk=1).author.id, 1)
    
    def test_9_new_post_creation_without_title_and_permissions_by_authenticated_user(self):
        self.user.save()
        self.client.force_authenticate(user=self.user)

        data = {'content': 'Lorem Ipsum'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], ['Post must have a title.'])
    
    def test_10_new_post_creation_without_content_and_permissions_by_authenticated_user(self):
        self.user.save()
        self.client.force_authenticate(user=self.user)

        data = {'title': 'Post 1'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], ['Post must have content.'])
    
    def test_11_new_post_creation_without_title_content_and_permissions_by_authenticated_user(self):
        self.user.save()
        self.client.force_authenticate(user=self.user)

        data = {}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], ['Post must have a title.', 'Post must have content.'])


class PostsUpdate(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('posts-update', kwargs={'pk': 1})
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
    
    def test_3_forbidden_access_to_browsable_api_by_unauthenticated_users(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_4_posts_title_update_with_different_edit_permissions_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', edit_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', edit_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', edit_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', edit_permission='public').save()

        for i in range(1, 5):
            data = {'title': f'UPDATED POST {i}'}

            edit_permissions = ['owner', 'team', 'authenticated', 'public']

            response = self.client.put(reverse('posts-update', kwargs={'pk': i}), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {'title': f'UPDATED POST {i}', 'content': '', 'read_permission': 'owner', 'edit_permission': edit_permissions[i - 1]})
    
    def test_5_posts_title_update_with_different_edit_permissions_by_authenticated_blogger_if_posts_were_posted_by_blogger_from_same_team(self):
        self.user.role = 'blogger'
        self.user.team = 'team 1'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 1').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', edit_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', edit_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', edit_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', edit_permission='public').save()

        for i in range(1, 5):
            data = {'title': f'UPDATED POST {i}'}

            edit_permissions = ['owner', 'team', 'authenticated', 'public']

            if i == 1:
                response = self.client.put(reverse('posts-update', kwargs={'pk': i}), data, format='json')
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
            else:
                response = self.client.put(reverse('posts-update', kwargs={'pk': i}), data, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data, {'title': f'UPDATED POST {i}', 'content': '', 'read_permission': 'owner', 'edit_permission': edit_permissions[i - 1]})
    
    def test_6_posts_title_update_with_different_edit_permissions_by_authenticated_blogger_if_posts_were_posted_by_blogger_from_different_team(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 2').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', edit_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', edit_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', edit_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', edit_permission='public').save()

        for i in range(1, 5):
            data = {'title': f'UPDATED POST {i}'}

            edit_permissions = ['owner', 'team', 'authenticated', 'public']

            if i == 1 or i == 2:
                response = self.client.put(reverse('posts-update', kwargs={'pk': i}), data, format='json')
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
            else:
                response = self.client.put(reverse('posts-update', kwargs={'pk': i}), data, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data, {'title': f'UPDATED POST {i}', 'content': '', 'read_permission': 'owner', 'edit_permission': edit_permissions[i - 1]})
    
    def test_7_posts_title_update_with_different_edit_permissions_by_authenticated_blogger_if_posts_were_posted_by_him_or_herself(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', edit_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', edit_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', edit_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', edit_permission='public').save()

        for i in range(1, 5):
            data = {'title': f'UPDATED POST {i}'}

            edit_permissions = ['owner', 'team', 'authenticated', 'public']

            response = self.client.put(reverse('posts-update', kwargs={'pk': i}), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {'title': f'UPDATED POST {i}', 'content': '', 'read_permission': 'owner', 'edit_permission': edit_permissions[i - 1]})
    
    def test_8_forbidden_posts_title_update_with_different_edit_permissions_by_unauthenticated_user(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', edit_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', edit_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', edit_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', edit_permission='public').save()

        for i in range(1, 5):
            data = {'title': f'UPDATED POST {i}'}

            response = self.client.put(reverse('posts-update', kwargs={'pk': i}), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_9_update_posts_editable_for_authenticated_admin_if_some_posts_were_deleted(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', is_active=False).save()

        for i in range(1, 5):
            data = {'title': f'UPDATED POST {i}'}

            response = self.client.put(reverse('posts-update', kwargs={'pk': i}), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {'title': f'UPDATED POST {i}', 'content': '', 'read_permission': 'owner', 'edit_permission': 'owner'})
    
    def test_10_update_posts_editable_for_authenticated_blogger_if_he_or_she_is_author_of_all_posts_and_some_posts_were_deleted(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', is_active=False).save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', is_active=False).save()

        for i in range(1, 5):
            data = {'title': f'UPDATED POST {i}'}

            if i == 1 or i == 3:
                response = self.client.put(reverse('posts-update', kwargs={'pk': i}), data, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data, {'title': f'UPDATED POST {i}', 'content': '', 'read_permission': 'owner', 'edit_permission': 'owner'})
            else:
                response = self.client.put(reverse('posts-update', kwargs={'pk': i}), data, format='json')
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_11_posts_permissions_update_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', content='Lorem Ipsum', read_permission='owner', edit_permission='owner').save()

        data = {'read_permission': 'public', 'edit_permission': 'public'}

        response = self.client.put(reverse('posts-update', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': 'Post 1', 'content': 'Lorem Ipsum', 'read_permission': 'public', 'edit_permission': 'public'})
    
    def test_12_posts_title_and_content_update_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', content='Lorem Ipsum').save()

        data = {'title': 'UPDATED POST 1', 'content': 'UPDATED CONTENT'}

        response = self.client.put(reverse('posts-update', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': 'UPDATED POST 1', 'content': 'UPDATED CONTENT', 'read_permission': 'owner', 'edit_permission': 'owner'})
    
    def test_13_posts_title_update_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', content='Lorem Ipsum').save()

        data = {'title': 'UPDATED POST 1'}

        response = self.client.put(reverse('posts-update', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': 'UPDATED POST 1', 'content': 'Lorem Ipsum', 'read_permission': 'owner', 'edit_permission': 'owner'})
    
    def test_14_posts_content_update_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', content='Lorem Ipsum').save()

        data = {'content': 'UPDATED CONTENT'}

        response = self.client.put(reverse('posts-update', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': 'Post 1', 'content': 'UPDATED CONTENT', 'read_permission': 'owner', 'edit_permission': 'owner'})
    
    def test_15_post_update_without_data_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', content='Lorem Ipsum').save()

        data = {}

        response = self.client.put(reverse('posts-update', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': 'Post 1', 'content': 'Lorem Ipsum', 'read_permission': 'owner', 'edit_permission': 'owner'})
    
    def test_16_non_existent_post_update_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', content='Lorem Ipsum').save()

        data = {'title': 'UPDATED POST 1', 'content': 'UPDATED CONTENT'}

        response = self.client.put(reverse('posts-update', kwargs={'pk': 2}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_17_non_existent_post_update_by_authenticated_blogger(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', content='Lorem Ipsum').save()

        data = {'title': 'UPDATED POST 1', 'content': 'UPDATED CONTENT'}

        response = self.client.put(reverse('posts-update', kwargs={'pk': 2}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
        

class PostsDelete(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('posts-delete', kwargs={'pk': 1})
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
    
    def test_3_forbidden_access_to_browsable_api_by_unauthenticated_users(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_4_delete_posts_with_different_edit_permissions_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', edit_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', edit_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', edit_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', edit_permission='public').save()

        for i in range(1, 5):
            response = self.client.delete(reverse('posts-delete', kwargs={'pk': i}), format='json')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(response.data, None)
            self.assertFalse(Posts.objects.get(pk=i).is_active)
    
    def test_5_delete_posts_with_different_edit_permissions_by_authenticated_blogger_if_posts_were_posted_by_blogger_from_same_team(self):
        self.user.role = 'blogger'
        self.user.team = 'team 1'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 1').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', edit_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', edit_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', edit_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', edit_permission='public').save()

        for i in range(1, 5):
            if i == 1:
                response = self.client.delete(reverse('posts-delete', kwargs={'pk': i}), format='json')
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
                self.assertTrue(Posts.objects.get(pk=i).is_active)
            else:
                response = self.client.delete(reverse('posts-delete', kwargs={'pk': i}), format='json')
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                self.assertEqual(response.data, None)
                self.assertFalse(Posts.objects.get(pk=i).is_active)
    
    def test_6_delete_posts_with_different_edit_permissions_by_authenticated_blogger_if_posts_were_posted_by_blogger_from_different_team(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com', team='team 2').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 1', edit_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 2', edit_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 3', edit_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=2), title='Post 4', edit_permission='public').save()

        for i in range(1, 5):
            if i == 1 or i == 2:
                response = self.client.delete(reverse('posts-delete', kwargs={'pk': i}), format='json')
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(response.data['detail'], 'Not found.')
                self.assertTrue(Posts.objects.get(pk=i).is_active)
            else:
                response = self.client.delete(reverse('posts-delete', kwargs={'pk': i}), format='json')
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                self.assertEqual(response.data, None)
                self.assertFalse(Posts.objects.get(pk=i).is_active)
    
    def test_7_delete_posts_with_different_edit_permissions_by_authenticated_blogger_if_posts_were_posted_by_him_or_herself(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', edit_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', edit_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', edit_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', edit_permission='public').save()

        for i in range(1, 5):
            response = self.client.delete(reverse('posts-delete', kwargs={'pk': i}), format='json')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(response.data, None)
            self.assertFalse(Posts.objects.get(pk=i).is_active)
    
    def test_8_forbidden_posts_deletion_with_different_edit_permissions_by_unauthenticated_user(self):
        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 1', edit_permission='owner').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 2', edit_permission='team').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 3', edit_permission='authenticated').save()
        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), title='Post 4', edit_permission='public').save()

        for i in range(1, 5):
            response = self.client.delete(reverse('posts-delete', kwargs={'pk': i}), format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
            self.assertTrue(Posts.objects.get(pk=i).is_active)
    
    def test_9_delete_post_already_deleted_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), is_active=False).save()

        response = self.client.delete(reverse('posts-delete', kwargs={'pk': 1}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
        self.assertFalse(Posts.objects.get(pk=1).is_active)
    
    def test_10_delete_post_with_public_edit_permission_and_already_deleted_by_authenticated_blogger(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_2@example.com').save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1), edit_permission='public', is_active=False).save()

        response = self.client.delete(reverse('posts-delete', kwargs={'pk': 1}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertFalse(Posts.objects.get(pk=1).is_active)
    
    def test_11_non_existent_post_deletion_by_authenticated_admin(self):
        self.user.role = 'admin'
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1)).save()

        response = self.client.delete(reverse('posts-delete', kwargs={'pk': 2}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_12_non_existent_post_deletion_by_authenticated_blogger(self):
        self.user.role = 'blogger'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        factories.PostsFactory(author=CustomUsers.objects.get(pk=1)).save()

        response = self.client.delete(reverse('posts-delete', kwargs={'pk': 2}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
