from django.urls import path
from .import views


app_name ="dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("user_create/", views.user_list, name="all_users"),
    path("all_users/", views.user_create_view, name="user_create"),
    path('user_edit/<int:pk>/', views.user_update_view, name='accommodation_edit'),
    
]