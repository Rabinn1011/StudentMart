from django.shortcuts import render, redirect

from rent.forms import RoomForm
from rent.models import Room


# Create your views here.
def room(request):
    rooms = Room.objects.all()

def add_Room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)  # Handle form data and uploaded files
        if form.is_valid():
            room = form.save(commit=False)
            room.detailsBy = request.user  # Set the current user as the seller
            room.save()
            return redirect('home')  # Redirect to home or another page
    else:
        form = RoomForm()
    return render(request, 'add_room.html', {'form': form})