from django.contrib.admin.options import get_content_type_for_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render,redirect
from .forms import ProductForm,SignupForm
from .models import Product, UserProfile
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
@permission_required('store.add_product')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Handle both form data and uploaded files
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Set the current user as the seller
            product.save()
            return redirect('home')  # Redirect to a product list or another page
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save User model
            profile = UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data.get('full_name'),

                phone_number=form.cleaned_data.get('phone_number'),
                address=form.cleaned_data.get('address'),
                dob=form.cleaned_data.get('dob'),
                citizenship_number=form.cleaned_data.get('citizenship_number'),
                photo=form.cleaned_data.get('photo'),
            )
            #messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})