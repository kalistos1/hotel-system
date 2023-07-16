from django import forms
from django.core.exceptions import ValidationError
from .models import Booking, RoomType, Room
from django.db.models import F
class BookingForm(forms.ModelForm):
    room_type = forms.ModelChoiceField(
        queryset=RoomType.objects.filter(booked_rooms__lt=F('total_rooms')),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_room_type'})
    )

    class Meta:
        model = Booking
        fields = ['room_type', 'check_in_date', 'check_out_date', 'guests', 'payment_option']
        widgets = {
            'check_in_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Check-in Date', 'type': 'date'}
            ),
            'check_out_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Check-out Date', 'type': 'date'}
            ),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Guests'}),
            'payment_option': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        room_type = cleaned_data.get('room_type')
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise forms.ValidationError('Check-out date must be after check-in date')

        if room_type:
            available_rooms = room_type.available_rooms
            if available_rooms <= 0:
                raise forms.ValidationError(f'No rooms are available for the selected room type: {room_type}')

        return cleaned_data

