from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import os , uuid


class CartProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Seller_Details(models.Model):
    seller_name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='uploads/profile_photos/', null=True, blank=True)
    chitizenship_photo = models.ImageField(upload_to='uploads/chitizenship/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    citizenship_number = models.CharField(max_length=250)
    dob = models.DateField()

    def __str__(self):
        return self.seller_name

def product_image_upload_path(instance, filename):
    folder_name = slugify(instance.name)
    return os.path.join('uploads/products', folder_name, filename)

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Books', 'Books'),
        ('Academic Tools', 'Academic Tools'),
        ('Academic Coats', 'Academic Coats'),
        ('Electronics', 'Electronics'),
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
    is_sold = models.BooleanField(default=False)

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



class Comment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="comments")  # Assuming you have a Product model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique Order ID
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Buyer
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product Ordered
    amount = models.PositiveIntegerField()  # Amount in paisa (NPR x100)
    khalti_pidx = models.CharField(max_length=100, blank=True, null=True, unique=True)  # Khalti Transaction ID
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Payment Status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Order {self.order_id} - {self.product.name} - {self.status}"