from django import template
from django.core.signing import Signer

register = template.Library()
signer = Signer()

@register.filter
def sign_username(username):
    """Signs the username securely."""
    return signer.sign(username)
