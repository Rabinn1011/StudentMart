from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from .views import login_required_redirect
from .views import search_products

urlpatterns = [
    path('', views.home, name='home'),
    path('add_product/', views.add_product, name='add_product'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:pk>', views.product, name='product'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('seller_detail/', views.seller_info, name='seller_info'),
    path('search/', search_products, name='search'),
    path('seller_profile/<str:encoded_username>', views.seller_profile, name='seller_profile'),
    path('edit_profile/', views.edit_seller_profile, name='edit_seller_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('edit_product/<int:pk>/', views.edit_product_form, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product_form, name='delete_product'),
    path('user_profile/<str:encoded_username>', views.user_profile, name='user_profile'),
path("seller-login-required/", login_required_redirect, name="seller-login-required"),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html',
        success_url='/contact/',  # Redirect to user profile after successful password change
    ), name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_rest_form.html'),name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password_rest_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

]
