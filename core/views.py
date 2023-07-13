from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'pages/index.html')


def about(request):
    return render(request, 'pages/about.html')


def contact_us(request):
    return render(request, 'pages/contact.html')


def rooms(request):
    return render(request, 'pages/accomodation.html')


def gallery(request):
    return render(request, 'pages/gallery.html')


def privacy_policy(request):
    return render(request, 'pages/index.html')


def terms(request):
    return render(request, 'pages/index.html')
