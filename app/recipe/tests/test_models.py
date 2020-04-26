from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import Tag, Ingredient, Recipe
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


class IngredientModelTest(TestCase):
    """Class to test Ingredient model"""
    @classmethod
    def setUpTestData(self):
        """Test data for each test method"""
        self.user = get_user_model().objects.create_user(
            email="test@gmaill.com",
            name="test",
            password="testpassword"
        )

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = Ingredient.objects.create(
            user=self.user,
            name="Cucumber"
        )
        self.assertEqual(str(ingredient), ingredient.name)


class RecipeModelTest(TestCase):
    """Class to test Recipe model"""
    @classmethod
    def setUpTestData(cls):
        """Test data for each test method defined below"""
        cls.user = get_user_model().objects.create_user(
            email="test@gmaill.com",
            name="test",
            password="testpassword"
        )

    def test_recipe_success(self):
        """Test the recipe string representation"""
        recipe = Recipe.objects.create(
            user=self.user,
            name="Paneer button",
            time_took_min="5",
            price=50.00
        )

        self.assertEqual(recipe.name, str(recipe))
