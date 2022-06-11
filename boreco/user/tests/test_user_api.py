from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:register')
ME_URL = reverse('user:me')
LOGIN_URL = reverse('user:login')

user_data = {
    "email": "paci@gmail.com",
    "password": "paco126"
}


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_superuser(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test users api public"""

    def setUp(self):
        self.client = APIClient()
        self.superuser = create_superuser(**user_data)

    def create_valid_user_success(self):
        payload = {
            'email': 'pacifique@gmail.com',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_unauthorized(self):
        """Test creating user that already exist fails"""
        payload = {
            'email': 'pacifique@gmail.com',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_user_success(self):
    #     """Test creating user that already exist fails"""
    #     payload = {
    #         'email': 'pacifique@gmail.com',
    #     }
    #     self.client.force_authenticate(user=self.superuser)
    #     create_user(**payload)
    #     res = self.client.post(CREATE_USER_URL, payload)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #
    # def test_password_too_short(self):
    #     """Test that password must be more than 5 characters"""
    #     payload = {
    #         'email': 'pacifique@gmail.com',
    #         'password': 'pw',
    #     }
    #     res = self.client.post(CREATE_USER_URL, payload)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     user_exists = get_user_model().objects.filter(
    #         email=payload['email']
    #     ).exists()
    #     self.assertFalse(user_exists)

# def test_generate_token_for_user(self):
#     """test generating token for a user"""
#     payload = {
#         'email': 'boreco@gmail.com',
#         'password': 'boreco1234'
#     }
#     create_user(**payload)
#     res = self.client.post(LOGIN_URL, payload)
#     self.assertIn('token', res.data)
#     self.assertEqual(res.status_code, status.HTTP_200_OK)
#
# def test_create_token_invalid_credentials(self):
#     """Test that token is not created , user is unauthorized if invalid credentials given"""
#     create_user(email="paco@gmail.com", password='test1234')
#     payload = {
#         'email': 'paco@gmail.com',
#         'password': 'wro1'
#     }
#     res = self.client.post(LOGIN_URL, payload)
#     self.assertNotIn('token', res.data)
#     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
# def test_create_token_no_user(self):
#     """Test that token is not created if user does not exist"""
#     payload = {'email': 'paco@gmail.com', 'password': 'test1234'}
#     res = self.client.post(LOGIN_URL, payload)
#     self.assertNotIn('token', res.data)
#     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
# def test_create_token_missing_fields(self):
#     """Test that email and password are required"""
#     res = self.client.post(LOGIN_URL, {'email': '', 'password': ''})
#     self.assertNotIn('token', res.data)
#     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
# def test_retrieve_user_unauthorized(self):
#     """Test that authentication is required"""
#     res = self.client.get(ME_URL)
#     self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


# class PrivateUserApiTest(TestCase):
#     """Test Api request that require authentication"""
#
#     def setUp(self):
#         self.adminUser = create_superuser(
#             email='paco@gmail.com',
#             password='test123865')
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.adminUser)

# def test_retrieve_profile_success(self):
#     """Test retrieving profile for logged in user"""
#     res = self.client.get(ME_URL)
#     self.assertEqual(res.status_code, status.HTTP_200_OK)
#     self.assertEqual(res.data, {
#         'email': self.adminUser.email,
#         'is_active': self.adminUser.is_active,
#         'is_staff': self.adminUser.is_staff,
#         'is_superuser': self.adminUser.is_superuser})

# def test_post_me_not_allowed(self):
#     """Test that POST not allowed on the ME_URL"""
#     res = self.client.post(ME_URL, {})
#     self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
# def test_update_user_profile(self):
#     """Test updating the user profile for authenticated user"""
#     payload = {'password': 'password123'}
#     res = self.client.patch(ME_URL, payload)
#     self.adminUser.refresh_from_db()
#     self.assertTrue(self.adminUser.check_password(payload['password']))
#     self.assertEqual(res.status_code, status.HTTP_200_OK)
