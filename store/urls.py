from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.loginview, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'), 
    path('product/<str:slug>/<int:id>/', views.product, name='product'), 
    path('category/<str:slug>/<int:id>/', views.category_page, name='category-page'), 
]    

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)