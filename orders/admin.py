from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Topping)
admin.site.register(Extra)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
