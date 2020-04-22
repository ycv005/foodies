from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "ycv005@gmail.com"
        cls.password = "@P1q2w3e4r"
        cls.name = "Yash"

    def test_user_create_with_email(self):
        """Testing a user is created with email"""
        user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password,
            name=self.name
        )
        self.assertEqual(self.email, user.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.admin)
        self.assertFalse(user.staff)

    def test_new_user_invalid_email(self):
        """Test user with invalid email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None, self.password, self.name
            )

    def test_new_super_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email=self.email,
            password=self.password,
            name=self.name
        )
        self.assertTrue(user.admin)
        self.assertTrue(user.staff)

    def test_new_staff_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_staffuser(
            email=self.email,
            password=self.password,
            name=self.name
        )
        self.assertFalse(user.admin)
        self.assertTrue(user.staff)
