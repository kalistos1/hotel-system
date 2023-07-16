from django.shortcuts import render
import uuid
from .models import Room, Booking, Payment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Room, Booking, Payment,RoomType,RoomImage
from django.conf import settings
from django.contrib import messages
#import paystack
from django.urls import reverse
from paystackapi.transaction import Transaction as PaystackTransaction
import uuid


# Create your views here.


def index(request):
    room_types = RoomType.objects.all()
    first_room_type = room_types.first()
    first_room_images = None

    if first_room_type:
        first_room_images = RoomImage.objects.filter(room__room_type=first_room_type)[:3]

    form = BookingForm()

    context = {
                'room_types':room_types,
                'form':form,
                'first_room_images': first_room_images,
               }
    return render(request, 'pages/index.html',context)


def about(request):
    return render(request, 'pages/about.html')


def contact_us(request):
    return render(request, 'pages/contact.html')


def rooms(request):
    rooms = Room.objects.all()
    context = {
                'rooms':rooms,
               }
    return render(request, 'pages/all-accomodations.html',context)



def room_available_list_view(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)
    available_rooms = Room.objects.filter(room_type=room_type, is_available=True)

    room_images = {}
    for room in available_rooms:
        room_images[room.id] = RoomImage.objects.filter(room=room)[:3]
    return render(request, 'pages/accomodation.html', {'room_type': room_type, 'available_rooms': available_rooms,'room_images':room_images})



def room_book(request, room_id=None):
   
    room = None
    room_type = None
  
    if room_id:
        # Logic for booking with specific room selection
        room = get_object_or_404(Room, id=room_id)

        if not room.is_available:
            return render(request, 'room_not_available.html', {'room': room})

        if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.room = room
                booking.customer = request.user.customer
                booking.save()

                # Check payment option
                payment_option = form.cleaned_data['payment_option']
                if payment_option == 'card':
                    return initiate_payment(request, booking)
                elif payment_option == 'cash':
                    booking.is_paid = True
                    booking.save()
                    return redirect('booking_success', booking_id=booking.id)

        else:
            form = BookingForm()

    else:
        # Logic for booking with room type selection
        if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                room_type = form.cleaned_data['room_type']
                room = room_type.room_set.filter(is_available=True).first()

                if room is not None:
                    booking = form.save(commit=False)
                    booking.room = room
                    booking.customer = request.user.customer
                    booking.save()

                    # Check payment option
                    payment_option = form.cleaned_data['payment_option']
                    if payment_option == 'card':
                        return initiate_payment(request, booking)
                    elif payment_option == 'cash':
                        booking.is_paid = True
                        booking.save()
                        return redirect('booking_success', booking_id=booking.id)
                else:
                    messages.error(request, 'No available rooms for selected room type.')
                    return redirect('room_list')  # Redirect to a page with available room types or other suitable URL

        else:
            form = BookingForm()

    return redirect('hotel:index')


def initiate_payment(request, booking):
    total_amount = booking.calculate_total_cost()

    # Generate a unique transaction reference
    transaction_ref = str(uuid.uuid4()).replace("-", "").upper()

    # Create the payment object
    payment = Payment.objects.create(
        booking=booking,
        amount=total_amount,
        payment_method='card',
        transaction_ref=transaction_ref,
        email=booking.customer.user.email
    )

    # Redirect to the Paystack payment page
    return redirect(f'/paystack_payment/{payment.id}/')


@login_required
def process_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    booking = payment.booking

    if request.method == 'POST':
        reference = request.POST.get('reference')

        # Verify the Paystack payment
        paystack_transaction = PaystackTransaction.verify(reference=reference)
        if paystack_transaction['status']:
            # Mark the booking as paid
            booking.is_paid = True
            booking.save()

            # Update the payment details
            payment.transaction_id = paystack_transaction['transaction_id']
            payment.verified = True
            payment.save()

            return redirect('booking_success', booking_id=booking.id)
        else:
            # Handle payment failure
            return redirect('payment_failed', booking_id=booking.id)

    return render(request, 'paystack_payment.html', {'booking': booking, 'payment': payment})


@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.is_paid or booking.status == 'confirmed':
        booking.status = 'canceled'
        booking.save()

        # Perform any additional cancellation logic if needed

        return redirect('booking_cancel_success')

    return render(request, 'booking_cancel.html', {'booking': booking})



def gallery(request):
    return render(request, 'pages/gallery.html')


def privacy_policy(request):
    return render(request, 'pages/index.html')


def terms(request):
    return render(request, 'pages/index.html')


# views.py
from django.http import JsonResponse

def get_available_rooms(request):
    if request.method == 'GET' and request.is_ajax():
        room_type_id = request.GET.get('room_type_id')
        rooms = Room.objects.filter(room_type_id=room_type_id, is_available=True)
        room_data = [{'id': room.id, 'room_number': room.room_number} for room in rooms]
        return JsonResponse({'rooms': room_data})
    else:
        return JsonResponse({'error': 'Invalid request'})
