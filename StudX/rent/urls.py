from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('room/', views.room, name='room'),
    path('add_room/', views.add_Room, name='add_room'),
    path('room_detail/<int:room_id>', views.room_detail, name='room_details'),
    path('room/<int:room_id>/add-review/', add_review, name='add_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),

]
