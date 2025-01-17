from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import os


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

def product_image_upload_path(instance, filename):
    """
    Define the upload path for images.
    Create a folder for each product using the product's name or ID.
    """
    folder_name = slugify(instance.name)  # Use the product name slugified as the folder name
    return os.path.join('uploads/products', folder_name, filename)

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Books', 'Books'),
        ('Academic Tools', 'Academic Tools'),
        ('Academic Coats', 'Academic Coats'),
        ('Student Tools', 'Student Tools'),
        ('Table', 'Table'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0 ,decimal_places=2,max_digits=6)
    description = models.CharField(max_length=250,default='',blank=True,null=True)
    image = models.ImageField(upload_to=product_image_upload_path, null=True, blank=True)
    is_sale = models.BooleanField(default=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_price = models.DecimalField(default=0 ,decimal_places=2,max_digits=6)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES,default='Other')


    def __str__(self):
        return self.name

    class Meta:
        permissions = []


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')

    def product_image_upload_path(instance, filename):
        folder_name = slugify(instance.product.name)  # Use the product's name
        return os.path.join('uploads/products', folder_name, filename)

    image = models.ImageField(upload_to=product_image_upload_path)

    def __str__(self):
        return f"Image for {self.product.name}"
