from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
import uuid
class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15)
    # Add other fields as per your requirements

    def __str__(self):
        return self.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    address = models.CharField(max_length=100)
    # Add other fields as per your requirements

    def __str__(self):
        return self.user.username

class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='receptionist')
    # Add additional fields specific to receptionists
    # Add other fields as per your requirements

    def __str__(self):
        return self.user.username

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager')
    # Add additional fields specific to managers
    # Add other fields as per your requirements

    def __str__(self):
        return self.user.username

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='room_images/')
    # Add other fields as per your requirements

    def __str__(self):
        return self.name

class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    total_rooms = models.PositiveIntegerField()
    booked_rooms = models.PositiveIntegerField(default=0)
    # Add other fields as per your requirements

    @property
    def available_rooms(self):
        return self.total_rooms - self.booked_rooms

    def __str__(self):
        return self.name

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    floor = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.ManyToManyField(Amenity)
    # Add other fields as per your requirements

    def __str__(self):
        return self.room_number


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='room_images/')
    image2 = models.ImageField(upload_to='room_images/')
    image3 = models.ImageField(upload_to='room_images/')


class Payment(models.Model):
    PAYMENT_OPTIONS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]

    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name="payment_booking")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_OPTIONS)
    transaction_id = models.CharField(max_length=100)
    transaction_ref = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_ref:
            self.transaction_ref = str(uuid.uuid4()).replace("-", "").upper()
        super().save(*args, **kwargs)

    def amount_value(self):
        return int(self.amount * 100)

    def __str__(self):
        return f"Payment for Booking {self.booking}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    guests = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    cancellation_terms = models.TextField(blank=True)
    reservation_number = models.CharField(max_length=100, unique=True)
    notes = models.TextField(blank=True)
    payment_option = models.CharField(max_length=20, choices=Payment.PAYMENT_OPTIONS)
    payment = models.OneToOneField(Payment, null=True, blank=True, on_delete=models.CASCADE, related_name="booking_payment")
    # Add other fields as per your requirements

    def __str__(self):
        return f"{self.room} - {self.customer}"
    

    def calculate_total_cost(self):
        # Implement your logic to calculate the total cost here
        # Example calculation based on room price and number of guests
        room_price = self.room.price
        num_guests = self.guests
        total_cost = room_price * Decimal(num_guests)

        return total_cost
