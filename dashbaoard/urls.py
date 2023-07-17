from django.urls import path
from .import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create/", views.accommodation_create, name="accommodation_create"),
    path("details/", views.accommodation_details, name="accommodation_details"),
    path('edit/<int:pk>/', views.accommodation_edit, name='accommodation_edit'),
    path('delete/<int:pk>/', views.accommodation_delete, name='accommodation_delete'),
]