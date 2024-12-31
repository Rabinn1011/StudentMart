from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.views.defaults import permission_denied
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User



from .forms import ProductForm,SignupForm, SellerForm
from .models import Product, Seller_Details
from django.contrib.auth.decorators import login_required,permission_required

seller_group,created = Group.objects.get_or_create(name='Sellers')
content_type = ContentType.objects.get_for_model(Product)
permissions = Permission.objects.filter(content_type=content_type, codename__in=[
    'add_product','change_product','delete_product'
])
seller_group.permissions.set(permissions)
seller_group.save()

def home(request):
    products =Product.objects.all()
    return render(request,'main.html', {'products':products} )

def contact(request):
    return render(request, 'contact.html')
def about(request):
    return render(request, 'about.html')


@login_required
@permission_required('store.add_product', raise_exception=True)
def add_product(request):
    try:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)  # Handle both form data and uploaded files
            if form.is_valid():
                product = form.save(commit=False)
                product.seller = request.user  # Set the current user as the seller
                product.save()
                return redirect('home')  # Redirect to a product list or another page
        else:
            form = ProductForm()
        return render(request, template_name='add_product.html', context={'form': form})

    except PermissionDenied:

        messages.error(request, "You need to log in or register to add a product.")
        return redirect('register')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def login_user(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
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
    return redirect('home')

def seller_info(request):
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)  # Handle both form data and uploaded files
        if form.is_valid():
            seller_detail = form.save(commit=False)
            seller_detail.user = request.user  # Set the current user as the seller
            seller_detail.save()
            return redirect('home')  # Redirect to a product list or another page
    else:
        form =SellerForm()
    return render(request, 'seller_details.html', {'form': form})

@login_required
def seller_profile(request):
    if request.user.groups.filter(name='Sellers').exists():
        seller=Seller_Details.objects.get(user=request.user)
        return render(request,'seller_profile.html',{'seller':seller})
    else:
        return redirect('home')