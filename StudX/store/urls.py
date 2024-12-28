
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_product/', views.add_product, name='add_product'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:pk>', views.product, name='product'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('seller_detail', views.seller_info, name='seller_info'),
    path('seller_profile/', views.seller_profile, name='seller_profile'),


]