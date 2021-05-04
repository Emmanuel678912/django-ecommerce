from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth import authenticate, login, logout
from .models import Customer

# Create your views here.
def store(request):
    context = {}
    return render(request, 'store.html', context)

def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)

def cart(request):
    context = {}
    return render(request, 'cart.html', context)

def contact(request):
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
            


    return render(request, 'login.html', context)

def register(request):
    
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
        # adds new user to customer group
        #customers.user_set.add(user)

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