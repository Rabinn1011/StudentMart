from django.contrib import admin
from .models import Product, Seller_Details, ProductImage, CartProfile, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Seller_Details)
admin.site.register(CartProfile)
admin.site.register(Order)

