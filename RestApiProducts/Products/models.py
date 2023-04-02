from django.db import models
import uuid


class Recipes(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt_create = models.DateTimeField(auto_now_add=True)
    dt_update = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    composition = models.ManyToManyField(to='ProductModal')

    def __str__(self):
        return str(self.title)


class Products(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt_create = models.DateTimeField(auto_now_add=True)
    dt_update = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    weight = models.IntegerField()
    calories = models.IntegerField()
    proteins = models.DecimalField(max_digits=10, decimal_places=2)
    fats = models.DecimalField(max_digits=10, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.title)


class ProductModal(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    weight = models.IntegerField()
