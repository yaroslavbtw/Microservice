# Generated by Django 4.1.7 on 2023-03-18 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0003_recipes_rename_id_products_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='recipe',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='Products.recipes'),
        ),
    ]
