from django.db import models
from products.models import Product
from ingredients.models import Ingredient, Unit

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  

    class Meta:
        db_table = 'recipe'

class RecipeDetail(models.Model):
    recipedetail_id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)  
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)  
    quantity = models.IntegerField()  
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)  

    class Meta:
        db_table = 'recipedetail'
        unique_together = ('recipe', 'ingredient')


