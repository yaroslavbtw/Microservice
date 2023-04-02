from collections import OrderedDict
from itertools import chain
from rest_framework import serializers
from .models import Products, Recipes, ProductModal
from .service import formDataToProductModal, formDataToRecipe


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class ProductModalSerializer(serializers.ModelSerializer):
    product = serializers.UUIDField()

    class Meta:
        model = ProductModal
        fields = ['product', 'weight']

    def to_representation(self, instance):
        res = formDataToProductModal(instance)
        data = super().to_representation(instance)
        return OrderedDict(chain(data.items(), res.items()))


class RecipeSerializer(serializers.ModelSerializer):
    composition = ProductModalSerializer(many=True)

    class Meta:
        model = Recipes
        fields = '__all__'

    def create(self, validated_data):
        composition_data = validated_data.pop('composition')
        recipe = Recipes.objects.create(**validated_data)
        for comp_data in composition_data:
            product_uuid = comp_data.pop('product')
            product = Products.objects.get(uuid=product_uuid)
            pm = ProductModal.objects.create(product=product, **comp_data)
            pm.recipes_set.add(recipe)
        return recipe

    def to_representation(self, instance):
        res = formDataToRecipe(instance)
        data = super().to_representation(instance)
        return OrderedDict(chain(data.items(), res.items()))
