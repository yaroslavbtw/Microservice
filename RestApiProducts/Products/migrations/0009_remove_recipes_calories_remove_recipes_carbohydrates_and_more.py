# Generated by Django 4.1.7 on 2023-03-18 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0008_productmodal_alter_recipes_composition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipes',
            name='calories',
        ),
        migrations.RemoveField(
            model_name='recipes',
            name='carbohydrates',
        ),
        migrations.RemoveField(
            model_name='recipes',
            name='fats',
        ),
        migrations.RemoveField(
            model_name='recipes',
            name='proteins',
        ),
        migrations.RemoveField(
            model_name='recipes',
            name='weight',
        ),
        migrations.RemoveField(
            model_name='productmodal',
            name='product_uuid',
        ),
        migrations.AddField(
            model_name='productmodal',
            name='product_uuid',
            field=models.ManyToManyField(to='Products.products'),
        ),
    ]
