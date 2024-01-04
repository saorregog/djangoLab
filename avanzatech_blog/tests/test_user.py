# DJANGO IMPORTS
from django.urls import reverse

# DJANGO REST FRAMEWORK IMPORTS
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# MODELS
from user.models import CustomUsers

# FACTORIES
from . import factories


class UsersList(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('users-list')
        self.user = factories.CustomUsersFactory()
    
    def test_1_access_to_browsable_api_by_authenticated_superusers(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
    
    def test_2_forbidden_access_to_browsable_api_by_authenticated_users(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')
    
    def test_3_forbidden_access_to_browsable_api_by_unauthenticated_users(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_4_list_all_users_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com').save()
        factories.CustomUsersFactory(email='test_2@example.com').save()
        factories.CustomUsersFactory(email='test_3@example.com').save()

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


class UsersCreate(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('users-create')
        self.user = factories.CustomUsersFactory()
    
    def test_1_access_to_browsable_api_by_authenticated_superusers(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], 'Method \"GET\" not allowed.')
    
    def test_2_forbidden_access_to_browsable_api_by_authenticated_users(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')
    
    def test_3_forbidden_access_to_browsable_api_by_unauthenticated_users(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_4_new_user_creation_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        data = {'email': 'test@example.com', 'password': '123456789', 'team': 'team 1'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 1, 'email': 'test@example.com', 'first_name': None, 'role': 'blogger', 'team': 'team 1', 'is_active': True})
    
    def test_5_forbidden_new_user_creation_by_authenticated_user(self):
        self.client.force_authenticate(user=self.user)

        data = {'email': 'test@example.com', 'password': '123456789', 'team': 'team 1'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')
    
    def test_6_forbidden_new_user_creation_by_unauthenticated_user(self):
        data = {'email': 'test@example.com', 'password': '123456789', 'team': 'team 1'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_7_new_admin_user_creation_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        data = {'email': 'test@example.com', 'password': '123456789', 'role': 'admin'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 1, 'email': 'test@example.com', 'first_name': None, 'role': 'admin', 'team': '', 'is_active': True})
    
    def test_8_new_blogger_user_creation_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        data = {'email': 'test@example.com', 'password': '123456789', 'role': 'blogger', 'team': 'team 1'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 1, 'email': 'test@example.com', 'first_name': None, 'role': 'blogger', 'team': 'team 1', 'is_active': True})
    
    def test_9_new_user_creation_with_existing_email_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.user.email = 'test@example.com'
        self.user.save()
        self.client.force_authenticate(user=self.user)

        data = {'email': 'test@example.com', 'password': '123456789', 'role': 'blogger', 'team': 'team 1'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'], ['custom users with this email address already exists.'])
    
    def test_10_new_admin_user_creation_without_email_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        data = {'password': '123456789', 'role': 'admin'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], ['Email address field may not be blank.'])
    
    def test_11_new_admin_user_creation_without_password_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        data = {'email': 'test@example.com', 'role': 'admin'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], ['Password field may not be blank.'])
    
    def test_12_new_admin_user_creation_without_email_and_password_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        data = {'role': 'admin'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], ['Email address field may not be blank.', 'Password field may not be blank.'])
    
    def test_13_new_blogger_user_creation_without_team_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        data = {'email': 'test@example.com', 'password': '123456789', 'role': 'blogger'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], ['Bloggers must belong to one team.'])
    
    def test_14_new_blogger_user_creation_without_email_password_and_team_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        data = {'role': 'blogger'}

        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], ['Email address field may not be blank.', 'Password field may not be blank.', 'Bloggers must belong to one team.'])
    

class UsersUpdate(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('users-update', kwargs={'pk': 1})
        self.user = factories.CustomUsersFactory()
    
    def test_1_access_to_browsable_api_by_authenticated_superusers(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], 'Method \"GET\" not allowed.')
    
    def test_2_forbidden_access_to_browsable_api_by_authenticated_users(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')
    
    def test_3_forbidden_access_to_browsable_api_by_unauthenticated_users(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_4_admin_user_update_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com', role='admin').save()

        data = {'first_name': 'test_user_1'}

        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'email': 'test_1@example.com', 'first_name': 'test_user_1', 'role': 'admin', 'team': '', 'is_active': True})
    
    def test_5_blogger_user_update_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com', role='blogger', team='team 1').save()

        data = {'first_name': 'test_user_1'}

        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'email': 'test_1@example.com', 'first_name': 'test_user_1', 'role': 'blogger', 'team': 'team 1', 'is_active': True})
    
    def test_6_role_update_for_admin_user_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com', role='admin').save()

        data = {'role': 'blogger', 'team': 'team 1'}

        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'email': 'test_1@example.com', 'first_name': None, 'role': 'blogger', 'team': 'team 1', 'is_active': True})
    
    def test_7_role_update_for_admin_user_without_team_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com', role='admin').save()

        data = {'role': 'blogger'}

        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], ['Bloggers must belong to one team.'])
    
    def test_8_role_update_for_blogger_user_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com', role='blogger', team='team 1').save()

        data = {'role': 'admin', 'team': 'admin team'}

        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'email': 'test_1@example.com', 'first_name': None, 'role': 'admin', 'team': 'admin team', 'is_active': True})
    
    def test_9_role_update_for_blogger_user_with_blank_team_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com', role='blogger', team='team 1').save()

        data = {'role': 'admin', 'team': ''}

        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'email': 'test_1@example.com', 'first_name': None, 'role': 'admin', 'team': '', 'is_active': True})
    
    def test_10_role_update_for_blogger_user_without_team_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com', role='blogger', team='team 1').save()

        data = {'role': 'admin'}

        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'email': 'test_1@example.com', 'first_name': None, 'role': 'admin', 'team': '', 'is_active': True})
    
    def test_11_admin_user_update_with_same_role_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com', role='admin').save()

        data = {'role': 'admin'}

        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'email': 'test_1@example.com', 'first_name': None, 'role': 'admin', 'team': '', 'is_active': True})
    
    def test_12_blogger_user_update_with_same_role_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com', role='blogger', team='team 1').save()

        data = {'role': 'blogger'}

        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'email': 'test_1@example.com', 'first_name': None, 'role': 'blogger', 'team': 'team 1', 'is_active': True})
    
    def test_13_admin_user_update_without_data_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com', role='admin').save()

        data = {}

        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'email': 'test_1@example.com', 'first_name': None, 'role': 'admin', 'team': '', 'is_active': True})
    
    def test_14_blogger_user_update_without_data_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory(email='test_1@example.com', role='blogger', team='team 1').save()

        data = {}

        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'email': 'test_1@example.com', 'first_name': None, 'role': 'blogger', 'team': 'team 1', 'is_active': True})
    
    def test_15_non_existent_user_update_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        data = {'first_name': 'test_user_1'}

        response = self.client.put(reverse('users-update', kwargs={'pk': 2}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')


class UsersDelete(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.endpoint = reverse('users-delete', kwargs={'pk': 1})
        self.user = factories.CustomUsersFactory()
    
    def test_1_access_to_browsable_api_by_authenticated_superusers(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], 'Method \"GET\" not allowed.')
    
    def test_2_forbidden_access_to_browsable_api_by_authenticated_users(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')
    
    def test_3_forbidden_access_to_browsable_api_by_unauthenticated_users(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_4_user_deletion_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
        self.assertFalse(CustomUsers.objects.get(pk=1).is_active)
    
    def test_5_non_existent_user_deletion_by_authenticated_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        factories.CustomUsersFactory().save()

        response = self.client.delete(reverse('users-delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')
