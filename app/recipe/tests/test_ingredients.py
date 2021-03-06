from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import Ingredient, Recipe
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')

TEST_CREDENTIAL = {
    "email": "test@gmail.com",
    "name": "test",
    "password": "testpassword"
}


class PublicIngredientApiTest(TestCase):
    """Test the publicly available ingredient API"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access to endpoint"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """Test the private ingredient API"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**TEST_CREDENTIAL)
        self.client.force_authenticate(self.user)

    def test_get_ingredient_list(self):
        """Test to get a list of ingredient && limited to user"""
        Ingredient.objects.create(user=self.user, name="oil")
        Ingredient.objects.create(user=self.user, name="nuts")
        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_ingredient_limited_to_user(self):
        """Test that the ingredient is available to its owner"""
        user2 = get_user_model().objects.create_user(
            email="test2@gmail.com",
            name="test2",
            password="testpassword"
        )
        Ingredient.objects.create(user=user2, name="tumeric")
        Ingredient.objects.create(user=self.user, name="salad")

        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.filter(
            user=self.user,
        )
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_ingredients(self):
        """Test that ingredients are created successfully"""
        data = {
            "name": "soap",
            "user": self.user
        }
        self.client.post(INGREDIENT_URL, data)

        ingredient_exists = Ingredient.objects.filter(
            user=self.user,
            name=data['name']
        ).exists()
        self.assertTrue(ingredient_exists)

    def test_invalid_ingredient(self):
        data = {
            "name": "",
            "user": self.user
        }
        res = self.client.post(INGREDIENT_URL, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_ingredients_assigned_to_recipes(self):
        """Test filtering ingredients by those assigned to recipes"""
        ingredient1 = Ingredient.objects.create(
            user=self.user, name='Apples'
        )
        ingredient2 = Ingredient.objects.create(
            user=self.user, name='Turkey'
        )
        recipe = Recipe.objects.create(
            name='Apple crumble',
            time_took_min=5,
            price=10,
            user=self.user
        )
        recipe.ingredients.add(ingredient1)

        res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})

        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_ingredients_assigned_unique(self):
        """Test filtering ingredients by assigned returns unique items"""
        ingredient = Ingredient.objects.create(user=self.user, name='Eggs')
        Ingredient.objects.create(user=self.user, name='Cheese')
        recipe1 = Recipe.objects.create(
            name='Eggs benedict',
            time_took_min=30,
            price=12.00,
            user=self.user
        )
        recipe1.ingredients.add(ingredient)
        recipe2 = Recipe.objects.create(
            name='Coriander eggs on toast',
            time_took_min=20,
            price=5.00,
            user=self.user
        )
        recipe2.ingredients.add(ingredient)

        res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
