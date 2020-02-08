from django.contrib import admin

from .models import Topping, MenuItem, Category, Extra

# Register your models here.
admin.site.register(Topping)
admin.site.register(Extra)
admin.site.register(Category)
admin.site.register(MenuItem)
