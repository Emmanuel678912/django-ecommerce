from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth import authenticate, login, logout
from .models import Customer, Product, Category, Order, OrderItem
import json

from django.http import JsonResponse

# Create your views here.
def store(request):
    products = Product.objects.all()

    categories = Category.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']

    context = {'products' : products, 'categories' : categories, 'cartItems' : cartItems}
    
    return render(request, 'store.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']

    context = {'cartItems' : cartItems}
    return render(request, 'checkout.html', context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except: 
            cart ={}
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']

        for i in cart:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items']+= cart[i]['quantity']

            item = {}
        

    context = {'items' : items, 'order' : order}
    return render(request, 'cart.html', context)

def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']
    return render(request, 'contact.html', {})

def loginview(request):
    context = {}

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        try:
            user = User.objects.get(email=email)
            if user is not None:
                login(request, user)

                return redirect('/')
            else:
                return redirect('register')
        except User.DoesNotExist:
            pass
            
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']

    return render(request, 'login.html', context)

def register(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']
    
    # adds new user when they submit a form
    if request.method == 'POST':
        firstname = request.POST['name']
        lastname = request.POST['last']
        email = request.POST['email']
        password = request.POST['password']

        # creates new user
        user, created = User.objects.get_or_create(
        is_superuser=False, 
        email=email, 
        password=password,
        username=email, 
        first_name=firstname,
        last_name=lastname)

        try:
            customer = Customer.objects.get(first_name=firstname)
        except Customer.DoesNotExist:
            customer = Customer(first_name=firstname)

        customer.user = user
        customer.last_name = lastname
        customer.email = email
        customer.password = password
        customer.save()

        # saves user data
        user.save()

        return redirect('login')

    context = {}
    return render(request, 'register.html', context)

def logout_view(request):
    # check if user is logged in when logout button is pressed
    if request.POST.get('logout'):
        print("user has logged out")
        logout(request)
        return redirect('/')
    
    return render(request, 'logout.html', {})

def product(request, slug, id):
    item = Product.objects.get(id=id)

    products = Product.objects.filter(id=id)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']

    context = {'products' : products, 'item' : item}

    return render(request, 'product.html', context)


def category_page(request, slug, id):
    category = Category.objects.get(id=id)

    products = Product.objects.filter(category=category)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']

    context = {'category' : category, 'products': products}
    return render(request, 'category-page.html', context)


def update_item(request):
    
    print(request.body)

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ', action)
    print('Product: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)