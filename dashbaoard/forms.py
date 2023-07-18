from django import forms
from .models import Accommodation

class AccommodationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Retrieve the 'request' argument if present
        super(AccommodationForm, self).__init__(*args, **kwargs)
    
        # Add 'form-control' class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            
        # Add placeholders
        self.fields['name'].widget.attrs['placeholder'] = 'Enter the name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter the description'
        self.fields['price_per_night'].widget.attrs['placeholder'] = 'Enter the price per night'
        self.fields['room_type'].widget.attrs['placeholder'] = 'Enter the room type'
        self.fields['capacity'].widget.attrs['placeholder'] = 'Enter the capacity'
        self.fields['services'].widget.attrs['placeholder'] = 'Enter the services'
        self.fields['image'].widget.attrs['placeholder'] = 'Select an image'
        self.fields['image'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Accommodation
        fields = ['name', 'description', 'price_per_night', 'room_type', 'capacity', 'services', 'image']

    def clean(self):
        cleaned_data = super().clean()
        user = self.request.user  
        if not user.is_superuser:
            raise forms.ValidationError("Only superusers can create accommodations.")

        return cleaned_data



class AccommodationEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccommodationEditForm, self).__init__(*args, **kwargs)
        
        # Add 'form-control' class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Add placeholders
        self.fields['name'].widget.attrs['placeholder'] = 'Enter the name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter the description'
        self.fields['price_per_night'].widget.attrs['placeholder'] = 'Enter the price per night'
        self.fields['room_type'].widget.attrs['placeholder'] = 'Enter the room type'
        self.fields['capacity'].widget.attrs['placeholder'] = 'Enter the capacity'
        self.fields['services'].widget.attrs['placeholder'] = 'Enter the services'
        self.fields['image'].widget.attrs['placeholder'] = 'Select an image'
        self.fields['image'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Accommodation
        fields = ['name', 'description', 'price_per_night', 'room_type', 'capacity', 'services', 'image']

