from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_to_shopping_cart", views.add_to_shopping_cart, name="add_to_shopping_cart"),
    path("remove_from_shopping_cart", views.remove_from_shopping_cart, name="remove_from_shopping_cart"),
    path("get_shopping_cart_items", views.get_shopping_cart_items, name="get_shopping_cart_items")
]
