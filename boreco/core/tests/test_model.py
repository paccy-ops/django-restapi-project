from django.contrib.auth import get_user_model
from django.test import TestCase


def sample_user(email="test@gmail.com", password="test1234"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelClass(TestCase):

    def test_create_user_email_successful(self):
        """Test for creating a new user with email successful"""
        email = "boreco@gmail.com"
        password = "boreco123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email for new User is normalized"""
        email = "boreco@GMAIL.COM"
        password = "12345"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating wih no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', '12345pa')

    def test_create_new_super_user(self):
        """Testing creating a new superuser"""
        email = "paco@gmail.com"
        password = "po1233"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
