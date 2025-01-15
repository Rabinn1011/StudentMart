from django.shortcuts import render

from rent.models import Room


# Create your views here.
def room(request):
    rooms = Room.objects.all()