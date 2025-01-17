from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.forms.models import modelformset_factory
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.signing import Signer, BadSignature
from django.http import Http404
from django.urls import reverse
from .forms import ProductForm, SignupForm, SellerForm, SellerProfileEditForm, ProductImageForm
from .models import Product, Seller_Details, ProductImage
from django.contrib.auth.decorators import login_required,permission_required
from rent.models import Room

seller_group,created = Group.objects.get_or_create(name='Sellers')
content_type = ContentType.objects.get_for_model(Product)
permissions = Permission.objects.filter(content_type=content_type, codename__in=[
    'add_product','change_product','delete_product'
])
seller_group.permissions.set(permissions)
seller_group.save()

def home(request):
    user_in_seller_group = request.user.groups.filter(name='Seller').exists()
    products =Product.objects.all()
    rooms= Room.objects.all()
    if request.user.is_authenticated:
       seller_details = Seller_Details.objects.filter(user=request.user).first()
       return render(request, 'main.html', {'products': products, 'seller_details': seller_details})
    return render(request,'main.html', {'products':products,'rooms':rooms, 'user_in_seller_group':user_in_seller_group} )

def contact(request):
    return render(request, 'contact.html')
def about(request):
    return render(request, 'about.html')


# @login_required
# @permission_required('store.add_product', raise_exception=True)
# def add_product(request):
#     try:
#         if request.method == 'POST':
#             form = ProductForm(request.POST, request.FILES)  # Handle both form data and uploaded files
#             if form.is_valid():
#                 product = form.save(commit=False)
#                 product.seller = request.user  # Set the current user as the seller
#                 product.save()
#                 return redirect('home')  # Redirect to a product list or another page
#         else:
#             form = ProductForm()
#         return render(request, template_name='add_product.html', context={'form': form})
#
#     except PermissionDenied:
#         messages.error(request, "You need to log in or register to add a product.")
#         return redirect('register')

def add_product(request):
    if not request.user.is_authenticated:  # Check if user is logged in
        messages.error(request, "You are not logged in. Please log in to add a product.")
        return redirect(f"/login/?next=/add_product")  # Redirect to login with `next` parameter

    if not request.user.is_superuser:
        if not request.user.groups.filter(name='Sellers').exists():
           messages.error(request, "You do not have permission to add products. Please register as a Seller.")
           return redirect('seller_info')

        seller_details = Seller_Details.objects.filter(user=request.user).first()
        if not seller_details.is_verified:
           messages.error(request, "You are not a verified seller. Please update your profile or wait for admin response.")
           return redirect('seller_profile',username=request.user.username)

    try:
        ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3)
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES)
            formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
            if product_form.is_valid() and formset.is_valid():
                product = product_form.save(commit=False)
                product.seller = request.user  # Set the current user as the seller
                product.save()
                for form in formset.cleaned_data:
                    if form:
                        image =form['image']
                        ProductImage.objects.create(product=product, image=image)
                return redirect('home')  # Redirect to home or another page
        else:
            product_form = ProductForm()
            formset = ImageFormSet(queryset=ProductImage.objects.none())
        return render(request, 'add_product.html', {'product_form': product_form, 'formset': formset})

    except PermissionDenied:
        messages.error(request, "You do not have permission to add a product.")
        return redirect('register')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def login_user(request):
    next_url = request.GET.get('next')
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username}! You have successfully logged in.")
            return redirect(next_url or 'home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})



def register(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered. Please use a different email.")
                return render(request, 'register.html', {'form': form})

            # Save User model
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f"Welcome {username}! Your account has been successfully created.")
                return redirect('login')  # Redirect to login or any desired page

        else:
            messages.error(request, "There was an error in your registration form. Please try again.")

    return render(request, 'register.html', {'form': form})

def logout_user(request):

    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')

def seller_info(request):
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)  # Handle both form data and uploaded files
        if form.is_valid():
            seller_detail = form.save(commit=False)
            seller_detail.user = request.user  # Set the current user as the seller
            seller_detail.save()
            seller_group1, created = Group.objects.get_or_create(name="Sellers")
            request.user.groups.add(seller_group1)
            return redirect('home')  # Redirect to a product list or another page
    else:
        form =SellerForm()
    return render(request, 'seller_details.html', {'form': form})


# def seller_profile(request,username):
#     if not request.user.is_authenticated:  # Check if user is logged in
#         messages.error(request, "You are not logged in. Please log in to add a product.")
#         return redirect(f"/login/?next=/seller_info")
#     if request.user.groups.filter(name='Sellers').exists():
#         seller = request.user
#         products = Product.objects.filter(seller=seller)
#         seller1 = get_object_or_404(Seller_Details,user__username=username)
#         seller=Seller_Details.objects.get(user=request.user)
#         return render(request,'seller_profile.html',{'seller':seller , 'products':products,'seller1':seller1})
#     else:
#         return redirect('home')

signer = Signer()
def user_profile(request, encoded_username):
    try:
        username = None
        user_objects = User.objects.values_list('username', flat=True)
        for user_object in user_objects:
            signed_value = f"{user_object}:{encoded_username}"
            try:
                username = signer.unsign(signed_value)
                break
            except BadSignature:
                continue
        if username is None:
            raise Http404("Invalid or tampered username")

    except BadSignature:
        raise Http404("Invalid or tampered username")


    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in. Please log in.")
        return redirect('login')
    if request.user.is_authenticated:
     user_profile1 = get_object_or_404(User, username=username)
    # Pass relevant user data to the template
    context = {
        'username': user_profile1.username,
        'first_name': user_profile1.first_name,
        'last_name': user_profile1.last_name,
        'email': user_profile1.email,
        'change_password_url': reverse('password_change'),  # Change Password URL

    }
    return render(request, 'user_profile.html', {'user_profile1': user_profile1})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keeps the user logged in after changing the password
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully updated.')

            return redirect('main.html')  # Redirect to user profile after success
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'password_change.html', {'form': form})

def seller_profile(request, encoded_username):

    try:
        seller_users = Seller_Details.objects.values_list('user__username', flat=True)
        seller_users = list(seller_users)
        username = None
        for seller_user in seller_users:
            signed_value = f"{seller_user}:{encoded_username}"
            try:
                username = signer.unsign(signed_value)
                break
            except BadSignature:
                continue
    except BadSignature:
        raise Http404("Invalid or tampered username")

    if not request.user.is_authenticated:  # Check if user is logged in
        messages.error(request, "You are not logged in. Please log in.")
        return redirect('contact')

    if request.user.is_authenticated:
        # Get the profile of the seller based on the passed username
        seller1 = get_object_or_404(Seller_Details, user__username=username)

        # Get all products for the logged-in user (seller)
        products1 = Product.objects.filter(seller=seller1.user)

        # Render the seller's profile page with the correct context
        return render(request, 'seller_profile.html', {'seller': seller1, 'products1': products1})
    else:
        return redirect('home')

def edit_seller_profile(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name='Sellers').exists():
        messages.error(request, "You need to be logged in as a seller to edit your profile.")
        return redirect('login')

        # Get the seller's details
    seller = get_object_or_404(Seller_Details, user=request.user)

    if request.method == 'POST':
        form = SellerProfileEditForm(request.POST, request.FILES, instance=seller)
        if form.is_valid():
            if not form.cleaned_data['photo']:
                seller.photo = None
            form.save()
            encoded_username = signer.sign(request.user.username)
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('seller_profile', encoded_username=encoded_username.split(":")[1])
    else:
        form = SellerProfileEditForm(instance=seller)

    return render(request, 'edit_user.html', {'form': form})

def delete_profile(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name='Sellers').exists():
        messages.error(request, "You need to be logged in as a seller to edit your profile.")
        return redirect('login')
    request.user.delete()
    messages.success(request, "Your profile has been deleted successfully.")
    return redirect('home')



def edit_product_form(request, pk):
    product1 = get_object_or_404(Product, id=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product1)
        if form.is_valid():
            form.save()
            messages.success(request, "Your product has been updated successfully.")
            return redirect('product',pk=form.cleaned_data['pk'])
    else:
         form = ProductForm(instance=product1)

    return render(request, 'edit_product.html', {'form': form})

def delete_product_form(request, pk):
    product1 = get_object_or_404(Product, id=pk, seller=request.user)
    product1.delete()
    messages.success(request, "Product has been deleted successfully.")

    return redirect('home')