from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProductSerializer, RecipeSerializer
from .models import Products, Recipes
from rest_framework import permissions


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Products.objects.all()
    lookup_field = 'uuid'

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Recipes.objects.prefetch_related('composition')
    lookup_field = 'uuid'

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
