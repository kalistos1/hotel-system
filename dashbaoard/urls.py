from django.urls import path
from .import views


app_name ="dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("user_create/", views.user_list, name="all_users"),
    path("amenity_create/", views.amenity_create_view, name="amenity_create"),
    path("amenity_list/", views.amenity_list_view, name="amenity_list"),
    path("amenity_update/<int:amenity_id>/", views.amenity_update_view, name="amenity_update"),
    path("amenity_delete/<int:amenity_id>/", views.amenity_delete_view, name="amenity_delete"),
    path("room_create/", views.room_type_create_view, name="room_type_create"),
    path("room_list/", views.room_type_list_view, name="room_type_list"),
    path("room_update/<int:room_type_id>/", views.room_type_update_view, name="room_type_update"),
    path("register/", views.user_create_view, name="user_create"),
    path('user_edit/<int:pk>/', views.user_update_view, name='accommodation_edit'),

    # ----------------------------------------------------------------------------------------------------

    # path("register", views.customer_register, name="customer_register")
    
]