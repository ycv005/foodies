from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagListViewSet


router = DefaultRouter()
router.register('tags', TagListViewSet)
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
