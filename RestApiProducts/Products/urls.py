from django.urls import path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductsViewSet)
router.register(r'recipes', RecipesViewSet)

urlpatterns = []

urlpatterns += router.urls
