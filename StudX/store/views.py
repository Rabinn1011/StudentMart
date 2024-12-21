from django.shortcuts import render,redirect
from .forms import ProductForm
from .models import Product
from django.contrib.auth.decorators import login_required

def home(request):
    products =Product.objects.all()
    return render(request,'main.html', {'products':products} )

@login_required
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
