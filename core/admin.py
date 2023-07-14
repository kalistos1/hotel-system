from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Receptionist)
admin.site.register(Manager)
admin.site.register(Amenity)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Payment)
admin.site.register(RoomPrice)
admin.site.register(Booking)
admin.site.register(RoomImage)