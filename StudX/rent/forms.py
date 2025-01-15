from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields=['owner_name','coordintate','owner_phone','photo','location','noOfRooms','moreDetails']