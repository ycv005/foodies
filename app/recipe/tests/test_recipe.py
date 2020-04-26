from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import Recipe
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse('recipe:recipe-list')
TEST_CREDENTIAL = {
    "email": "test@gmail.com",
    "name": "test",
    "password": "testpassword"
}


def sample_user(**params):
    data = TEST_CREDENTIAL
    data.update(params)
    return get_user_model().objects.create_user(
        **data
    )


def sample_recipe(user, **params):
    """sample recipe that we can use repeatedly"""
    data = {
        'user': user,
        'name': "Sample Recipe",
        "time_took_min": 10,
        "price": 15.00
    }
    data.update(params)
    return Recipe.objects.create(**data)


class PublicRecipeApiTest(TestCase):
    """Test all possible unauthenticated recipe API accesss"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that auth is req. for recipe api access"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test unauthenticated recipe api access to get, create"""
    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_get_recipes(self):
        """Test to retrieve all recipes"""
        sample_recipe(self.user)
        sample_recipe(self.user, name="some new recipe")
        sample_recipe(self.user, name="New Recipe tastes good")

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_limited_user(self):
        """Test that recipe limited to its owner"""
        sample_recipe(self.user)
        sample_recipe(self.user, name="Maggi recipe")
        user = sample_user(email="test2@gmail.com")
        sample_recipe(user, name="Yipee recipe")

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(
            user=self.user
        )
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)
