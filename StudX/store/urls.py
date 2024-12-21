
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_product/', views.add_product, name='add_product'),
    path('product/<int:pk>', views.product, name='product'),
]