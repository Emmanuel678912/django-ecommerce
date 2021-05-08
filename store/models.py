from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=80)
    image = models.ImageField(null=True, blank=True, upload_to='media/category-images')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    desc = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    slug = models.CharField(max_length=80)
    image = models.ImageField(null=True, blank=True, upload_to='media/product-images')

    def __str__(self):
        return self.name

    @property # allows access to function as attribute instead of method
    def imageURL(self): # tests if url exists if not returns an empty string
        try:
            url = self.image.url 
        except:
            url = ''    
        return url 

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.customer.name

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address