from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['longitude','latitude', 'detailsBy']
