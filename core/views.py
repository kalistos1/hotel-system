from django.shortcuts import render
import uuid
from .models import Room, Booking, Payment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Room, Booking, Payment
from django.conf import settings
#import paystack
from django.urls import reverse
from paystackapi.transaction import Transaction as PaystackTransaction
import uuid


# Create your views here.


def index(request):
    rooms = Room.objects.all()
    context = {
                'rooms':rooms,
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
    return render(request, 'pages/accomodation.html',context)



@login_required
def room_book(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if not room.is_available:
        return render(request, 'room_not_available.html', {'room': room})

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            guests = form.cleaned_data['guests']
            payment_option = form.cleaned_data['payment_option']

            if payment_option == 'card':
                booking = Booking.objects.create(
                    room=room,
                    customer=request.user.customer,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    guests=guests,
                    payment_option=payment_option
                )
                return initiate_payment(request, booking)

            elif payment_option == 'cash':
                room_type = room.room_type

                # Check if any other rooms of the same type are available
                if room_type.available_rooms > 0:
                    booking = Booking.objects.create(
                        room=room,
                        customer=request.user.customer,
                        check_in_date=check_in_date,
                        check_out_date=check_out_date,
                        guests=guests,
                        payment_option=payment_option
                    )
                    booking.is_paid = True
                    booking.save()
                    return redirect('booking_success', booking_id=booking.id)
                else:
                    return render(request, 'room_not_available.html', {'room': room})

    else:
        form = BookingForm()

    return render(request, 'book_room.html', {'room': room, 'form': form})


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
