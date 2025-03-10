from django import forms
from .models import Room
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Review  # Ensure Review is correctly imported from your app


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['longitude', 'latitude', 'detailsBy']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        rating = forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'type': 'range',  # range input for star selection
                'min': 1,
                'max': 5,
                'step': 1,
            }),
            validators=[MinValueValidator(1), MaxValueValidator(5)]
        )
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3,  # Reduce the number of visible rows
                'cols': 50,  # Optional, controls width

                'placeholder': 'Write your review here...',
            })
        }
