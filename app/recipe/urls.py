from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagListViewSet, IngredientViewSet, RecipeViewSet


router = DefaultRouter()
router.register('tags', TagListViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
