from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    owner_name = models.CharField(max_length=100)
    coordintate= models.CharField(max_length=100)
    owner_phone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='uploads/rooms/', null=True, blank=True)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    noOfRooms = models.IntegerField()
    detailsBy = models.ForeignKey(User, on_delete=models.CASCADE)
    moreDetails = models.TextField()

    def __str__(self):
        return self.owner_name