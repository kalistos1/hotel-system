from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests', 'payment_option']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-in Date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Check-out Date'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Guests'}),
            'payment_option': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise forms.ValidationError('Check-out date must be after check-in date')

        payment_option = cleaned_data.get('payment_option')

        if payment_option == 'cash':
            booking = Booking(**cleaned_data)
            if not booking.is_same_type_available():
                raise forms.ValidationError('No rooms of the same type are available')

        return cleaned_data