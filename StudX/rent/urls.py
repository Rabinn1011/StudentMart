from django.urls import path , include
from . import views


urlpatterns = [
    path('room/',views.room,name='room'),
    path('add_room/',views.add_Room,name='add_room'),

]