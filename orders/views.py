from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import serializers
import json
from .models import *

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    # get all categories from the database
    categories = Category.objects.all()
    toppings = Topping.objects.all()
    extra_items = Extra.objects.all()

    # extract the menu items from the database in a dictionary where
    # is the key is the category name and the value is a list of items
    menu = dict()
    for category in categories:
        menu[category.name] = MenuItem.objects.filter(category=category)

    serialized_menu = dict()
    for category in menu:
        serialized_menu[category] = serializers.serialize('json', menu[category])

    context = {
      "user": request.user,
      "menu": menu,
      "toppings": toppings,
      "extra_items": extra_items,
      "serialized_menu": serialized_menu
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

        #create a shopping_cart for this user
        cart = Cart(user=user)
        cart.save()

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if not request.user.is_authenticated:
            return render(request, "orders/register.html", {"message": None})
        return HttpResponseRedirect(reverse("index"))

def add_to_shopping_cart(request):
    print(request.body.decode("utf-8"))
    req = json.loads(request.body.decode("utf-8"))
    #req = json.loads(request.POST.get('data', ''))
    print(req)
    item_id = req["item_id"]
    size = req["size"]
    quantity = req["quantity"]
    price = req["price"]
    toppings = req['toppings']
    extras = req['extra']

    item = MenuItem.objects.filter(id=item_id)
    cart = Cart.objects.filter(user=request.user)
    total_price = price * quantity

    cart_item = CartItem(item=item[0], size=size, quantity=quantity, total_price=total_price, cart=cart[0])
    cart_item.save()

    for topping in toppings:
        cart_item.topping.add(Topping.objects.filter(name=topping)[0])

    for extra in extras:
        cart_item.extra.add(Extra.objects.filter(name=extra)[0])

    return JsonResponse({"success": True})


def remove_from_shopping_cart(request):
    pass

#def is(user_orders, cart_item):

#    for order in user_orders:
#        for item in order.shopping_cart.cartitem_set.all():
#            if item.id == cart_item.id:
#                return True
#    return False

def get_shopping_cart_items(request):
    cart = Cart.objects.filter(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart[0])

    #user_orders = Order.objects.filter(user=request.user)

    items = []
    for item in cart_items:
        #if not is(user_orders, cart_item):
        dic = dict()
        dic['name'] = item.item.name
        dic['size'] = item.size
        dic['quantity'] = item.quantity
        dic['price'] = item.total_price
        dic['toppings'] = []
        for topping in item.topping.all():
            dic['toppings'].append(topping.name)
        dic['extra'] = []
        for extra in item.extra.all():
            dic['extra'].append(extra.name)
        items.append(dic)

    json_obj = json.dumps(items)
    return JsonResponse(json_obj, safe=False)

def place_order(request):
    if request.method == 'POST':
        city = request.POST["City"]
        district = request.POST["District"]
        street_number = request.POST["StreetNumber"]
        building_number = request.POST["BuildingNumber"]

        address = city + "-" + district + "-" + street_number + "-" + building_number
        order = Order(user=request.user, delivery_address=address)
        order.save()

        user_shopping_cart = Cart.objects.filter(user=request.user)
        user_shopping_cart_items = CartItem.objects.filter(cart=user_shopping_cart[0])

        # associate the items in the shopping cart with the created order and remove them from the shopping cart
        for item in user_shopping_cart_items:
            item.order = order
            item.cart = None
            item.save()

        print("the order was placed sucessfully")
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return render(request, "orders/create_order.html")
        return HttpResponseRedirect(reverse("index"))
