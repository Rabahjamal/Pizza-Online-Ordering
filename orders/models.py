from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

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

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    time = models.DateTimeField(default=timezone.now)
    delivery_address = models.CharField(max_length=256)
    #shopping_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id} placed by user {self.user.username}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"shopping cart of user {self.user.username}"

class CartItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    topping = models.ManyToManyField(Topping, blank=True)
    extra = models.ManyToManyField(Extra, blank=True)
    size = models.CharField(max_length=5)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.size} {self.item.name}"
