from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from rent.forms import *
from rent.models import Room

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Review




import logging
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Room, Review  # Ensure these are correct based on your app structure
from .forms import ReviewForm

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
    room = get_object_or_404(Room, id=room_id)
    reviews = room.reviews.all().order_by('-created_at')  # Fetch room-specific reviews

    form = ReviewForm()  # No need to handle POST requests here

    return render(request, 'roomdetails.html', {
        'room': room,
        'reviews': reviews,  # Pass reviews to the template
        'form': form,  # Pass review form to the template
    })


def add_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.room = room
            review.user = request.user
            review.save()

            # Send review data and whether the review belongs to the user
            review_data = {
                'username': review.user.username,
                'comment': review.comment,
                'rating': review.rating,
                'created_at': review.created_at.strftime('%b %d, %Y'),  # Format date
            }

            return JsonResponse({
                'success': True,
                'review_data': review_data,
                'is_user_review': request.user == review.user,  # Flag for delete button
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors,
            })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request method.',
        })

logger = logging.getLogger(__name__)


@login_required
@require_POST
def delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        # Check if the current user is the author of the review
        if request.user == review.user:
            review.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'You are not authorized to delete this review.'})
    except Review.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Review not found.'})
