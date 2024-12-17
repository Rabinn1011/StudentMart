from django.db import models

class Seller(models.Model):
    # user = models.OneToOneField( 'User',on_delete=models.CASCADE)
    store_name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0 ,decimal_places=2,max_digits=6)
    description = models.CharField(max_length=250,default='',blank=True,null=True)
    image = models.ImageField(upload_to='uploads/products/', null=True, blank=True)
    is_sale = models.BooleanField(default=False)
    seller = models.ForeignKey('auth.User',on_delete=models.CASCADE,default=1)
    sale_price = models.DecimalField(default=0 ,decimal_places=2,max_digits=6)

    def __str__(self):
        return self.name