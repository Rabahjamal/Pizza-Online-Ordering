from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/index.html", {"message": None})
    # get all categories from the database
    categories = Category.objects.all()
    toppings = Topping.objects.all()

    # extract the menu items from the database in a dictionary where
    # is the key is the category name and the value is a list of items
    menu = dict()
    for category in categories:
        menu[category.name] = MenuItem.objects.filter(category=category)

    context = {
      "user": request.user,
      "menu": menu,
      "toppings": toppings
    }
    return render(request, "orders/home.html", context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials."})
    else:
        if not request.user.is_authenticated:
            return render(request, "orders/login.html", {"message": None})
        return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if not request.user.is_authenticated:
            return render(request, "orders/register.html", {"message": None})
        return HttpResponseRedirect(reverse("index"))
