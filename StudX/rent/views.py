from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from rent.forms import *
from rent.models import Room
from django.shortcuts import render, get_object_or_404
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden

from .forms import RoomForm, RoomImageForm
from .models import Room, RoomImage

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


from store.models import Seller_Details


def add_Room(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to add a room.")
        return redirect('login')

    try:
        seller = Seller_Details.objects.get(user=request.user)
        if not seller.is_verified:
            messages.error(request, "Only verified sellers can add a room.")
            return redirect('home')
    except Seller_Details.DoesNotExist:
        messages.error(request, "You must register as a seller first.")
        return redirect('seller_info')

    RoomImageFormSet = modelformset_factory(RoomImage, form=RoomImageForm, extra=3)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        formset = RoomImageFormSet(request.POST, request.FILES, queryset=RoomImage.objects.none())

        if form.is_valid() and formset.is_valid():
            room = form.save(commit=False)
            room.detailsBy = request.user
            room.save()

            for form in formset:
                if form.cleaned_data and form.cleaned_data.get('image'):
                    RoomImage.objects.create(room=room, image=form.cleaned_data['image'])

            messages.success(request, 'Room Added Successfully')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = RoomForm()
        formset = RoomImageFormSet(queryset=RoomImage.objects.none())

    return render(request, 'add_room.html', {
        'form': form,
        'formset': formset,
    })


def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # Check if the logged-in user is the one who added the room
    if request.user != room.detailsBy:
        return HttpResponseForbidden("You are not allowed to edit this room.")

    RoomImageFormSet = modelformset_factory(RoomImage, form=RoomImageForm, extra=0)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        formset = RoomImageFormSet(request.POST, request.FILES, queryset=RoomImage.objects.filter(room=room))

        if form.is_valid() and formset.is_valid():
            form.save()

            # Handle the image formset
            for form in formset:
                if form.cleaned_data.get('image'):
                    room_image = form.save(commit=False)
                    room_image.room = room
                    room_image.save()

            messages.success(request, 'Room updated successfully.')
            return redirect('home')

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = RoomForm(instance=room)
        formset = RoomImageFormSet(queryset=RoomImage.objects.filter(room=room))

    return render(request, 'edit_room.html', {
        'form': form,
        'formset': formset,
        'room': room,
    })


from django.http import JsonResponse


def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.user != room.detailsBy:
        messages.error(request, "You are not authorized to delete this room.")
        return JsonResponse({'success': False})

    if request.method == "POST":
        room.delete()
        messages.success(request, "Room deleted successfully.")
        return JsonResponse({'success': True})

    messages.error(request, "Invalid request method.")
    return JsonResponse({'success': False})


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
