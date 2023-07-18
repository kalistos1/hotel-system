# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from  core .models import Amenity, RoomType, RoomImage, Payment, Booking, User

class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomUserCreationForm(UserCreationForm):
    is_manager = forms.BooleanField(label='Is Manager', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_customer = forms.BooleanField(label='Is Customer', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_receptionist = forms.BooleanField(label='Is Receptionist', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2','is_manager','is_receptionist', 'is_customer')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class AmenityForm(BootstrapModelForm):
    class Meta:
        model = Amenity
        fields = ('name', 'description', 'image')

class RoomTypeForm(BootstrapModelForm):
    class Meta:
        model = RoomType
        fields = ('name', 'description', 'total_rooms', 'booked_rooms')

class RoomImageForm(BootstrapModelForm):
    class Meta:
        model = RoomImage
        fields = ('room', 'image1', 'image2', 'image3')

class PaymentForm(BootstrapModelForm):
    class Meta:
        model = Payment
        fields = ('booking', 'amount', 'payment_method', 'transaction_id', 'transaction_ref', 'email', 'verified')
