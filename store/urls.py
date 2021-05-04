from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.loginview, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'), 
]    
