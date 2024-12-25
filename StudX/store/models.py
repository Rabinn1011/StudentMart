from django.db import models
from django.contrib.auth.models import User





class Seller_Details(models.Model):
    seller_name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='uploads/profile_photos/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    citizenship_number = models.CharField(max_length=250)
    dob = models.DateField()

    def __str__(self):
        return self.seller_name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0 ,decimal_places=2,max_digits=6)
    description = models.CharField(max_length=250,default='',blank=True,null=True)
    image = models.ImageField(upload_to='uploads/products/', null=True, blank=True)
    is_sale = models.BooleanField(default=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_price = models.DecimalField(default=0 ,decimal_places=2,max_digits=6)

    def __str__(self):
        return self.name

    class Meta:
        permissions = []


