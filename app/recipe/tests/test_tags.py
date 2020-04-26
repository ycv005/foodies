from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import Tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import TagSerializer


class TagModelTest(TestCase):
    """Test case for the tag model"""
    @classmethod
    def setUpTestData(cls):
        """Test data for each test method defined below"""
        cls.user = get_user_model().objects.create_user(
            email="test@gmaill.com",
            name="test",
            password="testpassword"
        )

    def test_tag_create_successfull(self):
        """Test that tag are created successfully"""
        tag = Tag.objects.create(
            name="taghere",
            user=self.user
        )
        self.assertEqual(str(tag), tag.name)
        self.assertEqual(self.user.id, tag.user.id)


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
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            name="test",
            password="testpassword"
        )
        self.TAG_URL = reverse('recipe:tag-list')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test that an authorized user get all its own tags"""
        Tag.objects.create(user=self.user, name="taghere")
        Tag.objects.create(user=self.user, name="sometags")

        res = self.client.get(self.TAG_URL)
        tags = Tag.objects.all().order_by('-name')
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
