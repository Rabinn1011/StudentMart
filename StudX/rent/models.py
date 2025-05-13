from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import os
# Create your models here.
import os
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


def room_image_upload_path(instance, filename):
    """Consistent upload path for both Room and RoomImage models"""
    folder_name = slugify(instance.owner_name if hasattr(instance, 'owner_name') else instance.room.owner_name)
    return os.path.join('rooms', folder_name, filename)


class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('apartment', 'Apartment'),
        ('hostel', 'Hostel Bed'),
    ]

    owner_name = models.CharField(max_length=100)
    owner_phone = models.CharField(max_length=20)
    type = models.CharField(max_length=100, choices=ROOM_TYPES)
    noOfRooms = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255, blank=True)  # New field
    detailsBy = models.ForeignKey(User, on_delete=models.CASCADE)
    moreDetails = models.TextField()
    main_image = models.ImageField(
        upload_to=room_image_upload_path,
        null=True,
        blank=True,
        verbose_name="Main Room Image"
    )

    def __str__(self):
        return f"{self.owner_name}'s {self.get_type_display()}"

class RoomImage(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='additional_images'
    )
    image = models.ImageField(
        upload_to=room_image_upload_path,
        verbose_name="Additional Image"
    )

    def __str__(self):
        return f"Image #{self.id} for {self.room.owner_name}"

    class Meta:
        verbose_name = "Room Additional Image"
        verbose_name_plural = "Room Additional Images"

class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.room.name}"
