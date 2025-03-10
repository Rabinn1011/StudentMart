from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from unicodedata import category

from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image', 'is_sale', 'sale_price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
                'style': 'margin: 10px 0; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%; border-radius: 5px;',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'style': 'margin: 10px 0; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%; border-radius: 5px; resize: vertical; height: 120px;',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product price',
                'style': 'margin: 10px 0; border: 1px solid #ccc; padding: 10px; font-size: 14px; border-radius: 5px;',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'margin: 10px 0; padding: 10px; font-size: 14px;',
            }),
            'is_sale': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'display:flex;margin: 10px; transform: scale(1.2);',
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sale price (if applicable)',
                'style': 'margin: 10px 0; border: 1px solid #ccc; padding: 10px; font-size: 14px; border-radius: 5px;',
            }),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']



class SellerProfileEditForm(forms.ModelForm):
    class Meta:
        model = Seller_Details
        fields = ['seller_name', 'photo', 'address', 'phone_number', 'citizenship_number', 'chitizenship_photo', 'dob']
        widgets = {
            'seller_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name',
                'style': 'display:flex; margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
                'style': 'display:flex; margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'style': 'display:flex; margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
            }),
            'citizenship_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your citizenship number',
                'style': 'display:flex; margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
            }),
            'dob': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your date of birth',
                'style': 'display:flex; margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px;',
                'type': 'date',
            }),
        }


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller_Details
        fields = ['seller_name', 'address', 'phone_number', 'photo', 'citizenship_number', 'chitizenship_photo', 'dob']
        widgets = {
            'seller_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name',
                'style': 'display:flex; margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
                'style': 'display:flex; margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'style': 'display:flex; margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
            }),

            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': ' margin-bottom:10px;  padding: 10px; font-size: 14px;',
            }),
            'citizenship_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your citizenship number',
                'style': 'display:flex; margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
            }),
            'chitizenship_photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': ' margin-bottom:10px;  padding: 10px; font-size: 14px;',
            }),
            'dob': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your date of birth',
                'style': 'display:flex; margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px;',
                'type': 'date',
            }),
        }


class SignupForm(UserCreationForm):
    # Define fields with custom widgets
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'style': 'margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',

        }),
        required=True
    )
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'User Name',
            'style': 'margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
        })
    )
    first_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'style': 'margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
        })
    )
    last_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'style': 'margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'style': 'margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'style': 'margin-top:10px; margin-bottom:10px; border: 1px solid #ccc; padding: 10px; font-size: 14px; width: 100%;',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', '' 'email', 'password1', 'password2']

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


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image', 'is_sale', 'sale_price']
