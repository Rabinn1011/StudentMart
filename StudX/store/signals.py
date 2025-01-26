import json
from django.db.models.signals import post_delete
from django.dispatch import receiver
from store.models import Product, CartProfile

@receiver(post_delete, sender=Product)
def update_cart_profiles(sender, instance, **kwargs):
    product_id = str(instance.id)

    for profile in CartProfile.objects.all():
        if profile.old_cart:
            cart_data = json.loads(profile.old_cart)  # Convert string to dict
            if product_id in cart_data:
                del cart_data[product_id]  # Remove the deleted product
                profile.old_cart = json.dumps(cart_data)  # Convert back to string
                profile.save()

@receiver(post_delete, sender=Product)
def clean_up_cart(sender, instance, **kwargs):
    # Get all CartProfiles
    for cart_profile in CartProfile.objects.all():
        if cart_profile.old_cart:
            # Convert old_cart back to dictionary
            cart_dict = json.loads(cart_profile.old_cart)
            product_id = str(instance.id)

            # Remove the product if it exists
            if product_id in cart_dict:
                del cart_dict[product_id]

            # If the cart is empty after deletion, set old_cart to None
            if not cart_dict:
                cart_profile.old_cart = None  # or ''
            else:
                cart_profile.old_cart = json.dumps(cart_dict)

            cart_profile.save()