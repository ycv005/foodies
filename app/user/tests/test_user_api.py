from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


class PublicUserApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credential = {
            'email': "ycv005@gmail.com",
            'name': "yash",
            'password': "@P1q2w3e4r"
        }

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test user creation on api view"""
        res = self.client.post(CREATE_USER_URL, self.credential)
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        user = get_user_model().objects.filter(**res.data)
        self.assertTrue(user.exists())
        self.assertNotIn('password', res.data)

    def test_create_duplicate_user(self):
        """Test, duplicate user creation"""
        get_user_model().objects.create_user(**self.credential)
        res = self.client.post(CREATE_USER_URL, self.credential)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_password_too_short(self):
        """Test, password should be 5 char long"""
        self.credential['password'] = "abcd"
        res = self.client.post(CREATE_USER_URL, self.credential)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=self.credential['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_user(self):
        """Test that token is created for the user"""
        get_user_model().objects.create_user(**self.credential)
        res = self.client.post(TOKEN_URL, self.credential)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not access on invalid credential"""
        get_user_model().objects.create_user(**self.credential)
        self.credential['password'] = "abcde"
        res = self.client.post(TOKEN_URL, self.credential)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_user(self):
        """Test that token is not created for non-user"""
        res = self.client.post(TOKEN_URL, self.credential)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_missing_field(self):
        """Test to not create token when a field is missing"""
        self.credential['password'] = ''
        res = self.client.post(TOKEN_URL, self.credential)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
