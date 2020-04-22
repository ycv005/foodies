from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Setup data for test, which will be common for all method"""
        cls.email = "ycv005@gmail.com"
        cls.email1 = "yash005@gmail.com"
        cls.password = "@P1q2w3e4r"
        cls.name = "Yash"

    def setUp(self):
        """Setup for admin, it setup for each class method"""
        self.admin_user = get_user_model().objects.create_superuser(
            email=self.email,
            password=self.password,
            name=self.name
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email=self.email1,
            password=self.password,
            name=self.name
        )

    def test_user_list(self):
        """Test that users are listed on user app"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

        self.assertContains(res, self.admin_user.name)
        self.assertContains(res, self.admin_user.email)

    def test_user_change_page(self):
        """Test that checkout the user change page in admin"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
