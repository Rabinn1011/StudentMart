from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from rent.forms import RoomForm
from rent.models import Room


def room(request):
    rooms = Room.objects.all()


from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Seller_Details


def add_Room(request):
    # Check if the user is logged in
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to add a room.")
        return redirect('login')  # Redirect to login page

    try:
        seller = Seller_Details.objects.get(user=request.user)
        if not seller.is_verified:
            messages.error(request, "Only verified sellers can add a room.")
            return redirect('home')  # Redirect unverified users to home
    except Seller_Details.DoesNotExist:
        messages.error(request, "You must register as a seller first.")
        return redirect('seller_info')  # Redirect to seller registration page

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)  # Handle form data and uploaded files
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

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
