# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm, CustomUserChangeForm,CustomrRegistrationCreationForm
from  core .models import User, Amenity,RoomType, Room, Customer
from .forms import RoomTypeForm
from .forms import AmenityForm
from django.contrib import messages 

# Create your views here.

def dashboard(request):
    users = User.objects.count()
    amenities = Amenity.objects.count()
    rooms = Room.objects.count()
    customers = Customer.objects.count()
    print("kkkkkk", users)

    context = {
        "users":users,
        "amenities":amenities,
        "rooms":rooms,
        "customers":customers

    }
    return render(request, "pages/dashboard.html", context)


#@user_passes_test(lambda u: u.is_manager)
def user_create_view(request):
    if request.method == 'POST':
        form = CustomrRegistrationCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomrRegistrationCreationForm()
    return render(request, "pages/customer_register.html", {'form': form})



#@user_passes_test(lambda u: u.is_manager)
def user_update_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'pages/edit_user.html', {'form': form, 'user': user})




#@user_passes_test(lambda u: u.is_manager)
def user_list(request):
    users = User.objects.all()
    context ={
        'users':users,
    }
    return render(request, 'pages/all_users.html',context)



@user_passes_test(lambda u: u.is_manager)
def user_delete_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_delete.html', {'user': user})



#================================================================================================================


@user_passes_test(lambda u: u.is_manager)
def admin_book_user(request):
    pass


# @user_passes_test(lambda u: u.is_manager)
def amenity_create_view(request):
    if request.method == 'POST':
        form = AmenityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:amenity_list')
    else:
        form = AmenityForm()
    return render(request, 'pages/amenity_create.html', {'form': form})



# @user_passes_test(lambda u: u.is_manager)
def amenity_list_view(request):
    amenities = Amenity.objects.all()
    return render(request, 'pages/amenity_list.html', {'amenities': amenities})



# @user_passes_test(lambda u: u.is_manager)
def amenity_update_view(request, amenity_id):
    amenity = get_object_or_404(Amenity, id=amenity_id)
    if request.method == 'POST':
        form = AmenityForm(request.POST, instance=amenity)
        if form.is_valid():
            form.save()
            return redirect('dashboard:amenity_list')
    else:
        form = AmenityForm(instance=amenity)
    return render(request, 'pages/amenity_update.html', {'form': form, 'amenity': amenity})



# @user_passes_test(lambda u: u.is_manager)
def amenity_delete_view(request, amenity_id):
    amenity = get_object_or_404(Amenity, id=amenity_id)
    if request.method == 'POST':
        amenity.delete()
        return redirect('dashboard:amenity_list')
    return render(request, 'pages/amenity_delete.html', {'amenity': amenity})




# @user_passes_test(lambda u: u.is_manager)
def room_type_create_view(request):
    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:room_type_list')
    else:
        form = RoomTypeForm()
    return render(request, 'pages/room_type_create.html', {'form': form})



# @user_passes_test(lambda u: u.is_manager)
def room_type_list_view(request):
    room_types = RoomType.objects.all()
    return render(request, 'pages/room_type_list.html', {'room_types': room_types})



# @user_passes_test(lambda u: u.is_manager)
def room_type_update_view(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)
    if request.method == 'POST':
        form = RoomTypeForm(request.POST, instance=room_type)
        if form.is_valid():
            form.save()
            return redirect('dashboard:room_type_list')
    else:
        form = RoomTypeForm(instance=room_type)
    return render(request, 'pages/room_type_upate.html', {"form":form})



# -------------------------------------------------------------------------------------------------------

# def customer_register(request):
#     return render(request, "pages/customer_register.html" )