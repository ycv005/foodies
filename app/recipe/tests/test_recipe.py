from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import Recipe, Tag, Ingredient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse('recipe:recipe-list')
TEST_CREDENTIAL = {
    "email": "test@gmail.com",
    "name": "test",
    "password": "testpassword"
}
SAMPLE_RECIPE = {
    "name": "Sample Recipe",
    "time_took_min": 10,
    "price": 5.00
}


def recipe_detail_url(id):
    """Return a recipe detail url"""
    return reverse('recipe:recipe-detail', args=[id])


def sample_tag(user, name):
    """Create & return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name):
    """Create & return a sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


def sample_user(**params):
    """Create & return a user"""
    data = TEST_CREDENTIAL
    data.update(params)
    return get_user_model().objects.create_user(
        **data
    )


def sample_recipe(user, **params):
    """sample recipe that we can use repeatedly"""
    data = SAMPLE_RECIPE.copy()
    data.update(params)
    return Recipe.objects.create(user=user, **data)


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

    def test_recipe_detail(self):
        """Test to get a recipe detail"""
        recipe = sample_recipe(self.user)
        tag = sample_tag(self.user, "food")
        tag1 = sample_tag(self.user, "fast food")
        ingredient = sample_ingredient(self.user, "oil")
        recipe.tags.add(tag)
        recipe.tags.add(tag1)
        recipe.ingredients.add(ingredient)

        res = self.client.get(recipe_detail_url(recipe.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(str(recipe), recipe.name)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating recipe"""
        res = self.client.post(RECIPE_URL, SAMPLE_RECIPE)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in SAMPLE_RECIPE.keys():
            self.assertEqual(SAMPLE_RECIPE[key], getattr(recipe, key))

    def test_create_recipe_tags(self):
        """Test creating a recipe with tags"""
        tag = sample_tag(user=self.user, name="food")
        tag1 = sample_tag(user=self.user, name="north indian")
        data = SAMPLE_RECIPE.copy()
        data['tags'] = [tag.id, tag1.id]

        res = self.client.post(RECIPE_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(2, len(tags))
        self.assertIn(tag, tags)
        self.assertIn(tag1, tags)

    def test_create_recipe_ingredients(self):
        """Test createing a recipe with ingredients"""
        ingredient = sample_ingredient(self.user, name="soya")
        ingredient1 = sample_ingredient(self.user, name="mustards")
        data = SAMPLE_RECIPE.copy()
        data['ingredients'] = [ingredient.id, ingredient1.id]
        res = self.client.post(RECIPE_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertIn(ingredient, ingredients)
        self.assertIn(ingredient1, ingredients)
