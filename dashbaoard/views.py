from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccommodationForm, AccommodationEditForm
from .models import Accommodation
from django.contrib import messages
from .models import Service, Accommodation


# Create your views here.

def dashboard(request):
    return render(request, "pages/dashboard.html")



def accommodation_create(request):
    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES, request=request)  # Pass the request object to the form
        if form.is_valid():
            accommodation = form.save(commit=False)
            accommodation.created_by = request.user  # Set the 'created_by' field to the current user
            accommodation.save()
            form.save_m2m()  # Save the many-to-many relationships
            messages.success(request, 'Accommodation created successfully.')
            return redirect('accommodation_create')
    else:
        form = AccommodationForm(request=request)  
    return render(request, 'pages/accommodation_create.html', {'form': form})



def accommodation_details(request):
    accomodations = Accommodation.objects.all()  
    return render(request, "pages/accommodation_details.html", {"accomodations":accomodations})


# def accomodation_edit(request):
#     return render(request, "pages/accomodation_edit.html")

def accommodation_edit(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    
    form = AccommodationEditForm(request.POST or None, request.FILES or None, instance=accommodation)
    if form.is_valid():
        form.save()
        return redirect('accommodation_details')  
    
    context = {
        'form': form,
        'accommodation': accommodation,
    }
    return render(request, "pages/accomodation_edit.html", context)




def accommodation_delete(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    
    if request.method == 'POST':
        accommodation.delete()
        return redirect('accommodation_details') 
    
    return render(request, 'pages/accomodation_delete.html', {'accommodation': accommodation})


