from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Room(models.Model):
        owner_name = models.CharField(max_length=100)
        latitude = models.FloatField()
        longitude = models.FloatField()
        owner_phone = models.CharField(max_length=20)
        photo = models.ImageField(upload_to='uploads/rooms/', null=True, blank=True)
        type = models.CharField(max_length=100)
        noOfRooms = models.IntegerField()
        detailsBy = models.ForeignKey(User, on_delete=models.CASCADE)
        moreDetails = models.TextField()

        def __str__(self):
            return self.owner_name

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
