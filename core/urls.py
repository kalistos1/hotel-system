from django.urls import path
from .import views


app_name = "hotel"

urlpatterns =[
    path('',views.index, name ='index'),
    path('about-us/',views.about, name ='about'),
    path('contact-us/',views.contact_us, name ='contact'),
    path('rooms/',views.rooms, name ='rooms'),
    path('gallery/',views.gallery, name ='gallery'),
    # URL pattern for booking with room type selection
    path('room_book/', views.room_book, name='room_book_by_room_type'),
    
    # URL pattern for booking with specific room selection
    path('room_book/room/<int:room_id>/', views.room_book, name='room_book_by_room_id'),

    path('get-available-rooms/', views.get_available_rooms, name='getrooms'),
    path('available-rooms/<int:room_type_id>/', views.room_available_list_view, name='room_available_list'),
    path('paystack_payment/',views.initiate_payment)

]