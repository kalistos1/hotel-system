from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['check_in_date'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Check-in Date'})
        self.fields['check_out_date'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Check-out Date'})
        self.fields['guests'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Guests'})

    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests']
