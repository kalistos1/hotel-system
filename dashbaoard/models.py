from django.db import models
# from django.contrib.auth.models import User
from core.models import User
# Create your models here.

class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_files/')
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=50)
    capacity = models.IntegerField()
    services = models.ManyToManyField('Service')

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.IntegerField()
    
    
    def __str__(self):
        return self.name


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    arrival_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    

   