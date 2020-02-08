from django.db import models

# Create your models here.
class Topping(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"

class Extra(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}"

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    has_toppings = models.BooleanField()
    has_extra = models.BooleanField()

    def __str__(self):
        return f"{self.name}"

class MenuItem(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    small_price = models.FloatField(blank=True, null=True)
    large_price = models.FloatField(blank=True, null=True)
    number_of_topping = models.IntegerField(blank=True, null=True)
    number_of_extra_items = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} from {self.category}"
