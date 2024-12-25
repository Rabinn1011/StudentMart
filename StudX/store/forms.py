from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Product, Seller_Details


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image','is_sale','sale_price']

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller_Details
        fields = ['seller_name','address','phone_number','photo','citizenship_number','dob']

class SignupForm(UserCreationForm):

        # Define fields with custom widgets
        email = forms.EmailField(
            label="",
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            required=True
        )






        class Meta:
            model = User

            fields = ['username', 'email', 'password1', 'password2']

        # Add dynamic attributes in the constructor
        def __init__(self, *args, **kwargs):
            super(SignupForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'User Name'
            self.fields['username'].label = ""
            self.fields[
                'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'
            self.fields['password1'].label = ""
            self.fields[
                'password1'].help_text = '<span class="form-text text-muted"><small>Your password must contain at least 8 characters.</small></span>'

            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
            self.fields['password2'].label = ""
            self.fields['password2'].help_text = ""
