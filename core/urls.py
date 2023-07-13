from django.urls import path
from .import views


app_name = "hotel"

urlpatterns =[
    path('',views.index, name ='index'),
    path('about-us/',views.about, name ='about'),
    path('contact-us/',views.contact_us, name ='contact'),
    path('rooms/',views.rooms, name ='rooms'),
    path('gallery/',views.gallery, name ='gallery'),
]