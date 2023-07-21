# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from  core .models import Amenity, RoomType, RoomImage, Payment, Booking, User, Customer
from django.db import transaction

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

        # Set the is_customer field to be True by default
        self.fields['is_customer'].initial = True




class CustomrRegistrationCreationForm(UserCreationForm):
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

        # Set the is_customer field to be True by default
        self.fields['is_customer'].initial = True



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



# ---------------------------------------------------------------------------------------------------------------------------

class customerRegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=100)

    model = User
    fields = ('username', 'email', 'phone_number', 'password1', 'password2', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    
                    'form-control'
                )
            })


            """
            Using @transaction.atomic ensures that all the code inside the decorated block
             is executed as a single atomic transaction. If any exception occurs during the execution
              of the block, then the transaction is rolled back.. This helps in maintaining data
             consistency and integrity.
            """
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            address = self.cleaned_data.get('address')

            Customer.objects.create(
                user=user,
                address=address
            )


        return user

