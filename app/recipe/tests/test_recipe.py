from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import Recipe, Tag, Ingredient, recipe_image_file_path
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
import tempfile
import os
from PIL import Image
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


def image_upload_url(id):
    """Return url for image upload"""
    return reverse('recipe:recipe-upload-image', args=[id])


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

    def test_partially_update_recipe(self):
        """Test updating a recipe with patch"""
        recipe = sample_recipe(self.user)
        recipe.tags.add(sample_tag(self.user, "south indian"))
        new_tag = sample_tag(self.user, "american")
        data = {'name': 'Butter chicken', 'tags': [new_tag.id]}

        self.client.patch(recipe_detail_url(recipe.id), data)
        recipe.refresh_from_db()
        self.assertEqual(recipe.name, data['name'])
        self.assertIn(new_tag, recipe.tags.all())
        self.assertEqual(1, len(recipe.tags.all()))

    def test_update_recipe(self):
        """Test updating a recipe with put"""
        recipe = sample_recipe(self.user)
        recipe.tags.add(sample_tag(self.user, "south indian"))
        data = SAMPLE_RECIPE.copy()
        data['title'] = 'Chicken punjabi'
        data['price'] = 180
        self.client.put(recipe_detail_url(recipe.id), data)
        recipe.refresh_from_db()
        self.assertEqual(data['price'], recipe.price)
        self.assertEqual(data['name'], recipe.name)
        #  all tags would be removed since not provided
        self.assertEqual(len(recipe.tags.all()), 0)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image saved in right location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = recipe_image_file_path(None, 'myimage.jpeg')

        exp_path = f'uploads/recipe/{uuid}.jpeg'
        self.assertEqual(file_path, exp_path)


class RecipeImageUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)
        self.recipe = sample_recipe(self.user)

    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image_recipe(self):
        """Test a image is uploaded successfully to recipe"""
        url = image_upload_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', [10, 10])
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_invalid_image(self):
        """Test uploading invalid image to recipe"""
        url = image_upload_url(self.recipe.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
