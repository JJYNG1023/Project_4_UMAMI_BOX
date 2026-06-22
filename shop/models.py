from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description=models.TextField(max_length=500)

    def __str__(self):
        return self.friendly_name or self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=254)
    friendly_name=models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.friendly_name or self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    tag = models.ManyToManyField(Tag,null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField()
    cooking_time = models.PositiveIntegerField(null=True, blank=True)
    servings = models.PositiveIntegerField(null=True, blank=True)
    spice_level = models.CharField(max_length=50,null=True, blank=True)
    ingredients = models.TextField(null=True, blank=True)
    allergens = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name