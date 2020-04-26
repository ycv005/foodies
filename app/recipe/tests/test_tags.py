from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import Tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import TagSerializer


class PublicTagApiTest(TestCase):
    """Test case for the publicily available tag api"""
    @classmethod
    def setUpTestData(cls):
        cls.TAG_URL = reverse('recipe:tag-list')

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is req for retrieving tags"""
        res = self.client.get(self.TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):
    """Tesst the authorized user tags"""
    @classmethod
    def setUpTestData(self):
        self.crenditial = {
            "email": "test@gmail.com",
            "name": "test",
            "password": "testpassword"
        }
        self.user = get_user_model().objects.create_user(**self.crenditial)
        self.TAG_URL = reverse('recipe:tag-list')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test that an authorized user get all its own tags"""
        Tag.objects.create(user=self.user, name="taghere")
        Tag.objects.create(user=self.user, name="sometags")

        res = self.client.get(self.TAG_URL)
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are specific to user"""
        user2 = get_user_model().objects.create_user(
            email="test2@gmail.com",
            name="test2",
            password="test2password"
        )
        Tag.objects.create(user=user2, name="fruity")
        tag = Tag.objects.create(user=self.user, name="Foodie")

        res = self.client.get(self.TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successfully(self):
        """Test that a tag is created successfully"""
        data = {"name": "sometag"}
        self.client.post(
            self.TAG_URL,
            data
        )
        tag_exist = Tag.objects.filter(
            user=self.user,
            name=data['name']
        ).exists()
        self.assertTrue(tag_exist)

    def test_create_tag_invalid(self):
        """Test create new invalid tag"""
        res = self.client.post(
            self.TAG_URL,
            {"name": ""}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
