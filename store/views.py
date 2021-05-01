from django.shortcuts import render

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
    return render(request, 'login.html', context)

def register(request):
    context = {}
    return render(request, 'register.html', context)