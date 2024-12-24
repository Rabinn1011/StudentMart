from django.db import models
from django.contrib.auth.models import User



class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0 ,decimal_places=2,max_digits=6)
    description = models.CharField(max_length=250,default='',blank=True,null=True)
    image = models.ImageField(upload_to='uploads/products/', null=True, blank=True)
    is_sale = models.BooleanField(default=False)
    seller = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    sale_price = models.DecimalField(default=0 ,decimal_places=2,max_digits=6)

    def __str__(self):
        return self.name

    class Meta:
        permissions = []



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    dob = models.DateField(verbose_name="Date of Birth")
    citizenship_number = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='uploads/profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username
