from django.http import Http404
from django.shortcuts import render, redirect
from pyexpat.errors import messages

from rent.forms import RoomForm
from rent.models import Room


def room(request):
    rooms = Room.objects.all()

def add_Room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)  # Handle form data and uploaded files
        latitude =request.POST.get('latitude')
        longitude =request.POST.get('longitude')
        if form.is_valid():
            room = form.save(commit=False)
            room.detailsBy = request.user  # Set the current user as the seller
            room.latitude = latitude
            room.longitude = longitude
            room.save()
            messages.success(request, 'Room Added')
            return redirect('home')  # Redirect to home or another page
        messages.error(request, 'Room Not Added')
    else:
        form = RoomForm()
    return render(request, 'add_room.html', {'form': form})

def room_detail(request, room_id):
    try:
        room = Room.objects.get(id=room_id)

    except Room.DoesNotExist:
        raise Http404("Room not found")

    return render(request, 'roomdetails.html', {'room': room})
