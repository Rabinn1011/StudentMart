

from .models import Seller_Details

def seller_details(request):
    """
    Adds `seller_details` to every template context.
    It's the Seller_Details instance if the user is authenticated and has one,
    otherwise None.
    """
    user = request.user
    seller = None
    if user.is_authenticated:
        try:
            seller = Seller_Details.objects.get(user=user)
        except Seller_Details.DoesNotExist:
            seller = None
    return { 'seller_details': seller }

