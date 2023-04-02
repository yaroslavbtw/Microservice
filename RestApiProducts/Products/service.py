import decimal
from collections import OrderedDict


def formDataToProductModal(instance):
    weight_to_calc, product = instance.weight, instance.product
    data = {}
    relation = product.weight / weight_to_calc
    data['calories'] = round(product.calories * relation, 2)
    data['proteins'] = round(float(product.proteins * decimal.Decimal(relation)), 2)
    data['fats'] = round(float(product.fats * decimal.Decimal(relation)), 2)
    data['carbohydrates'] = round(float(product.carbohydrates * decimal.Decimal(relation)), 2)
    return OrderedDict(data)


def formDataToRecipe(instance):
    res_dict = OrderedDict([('calories', 0), ('proteins', 0), ('fats', 0), ('carbohydrates', 0), ('weight', 0)])
    for pm in instance.composition.all():
        dict_var = formDataToProductModal(pm)
        for key in dict_var.keys():
            res_dict[key] += dict_var[key]
        res_dict['weight'] += pm.weight
    return res_dict
