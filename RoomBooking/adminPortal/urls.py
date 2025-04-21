from django.urls import path
from . import views

app_name = 'adminPortal'

urlpatterns = [
    # Example view
    path('manage_rooms/', views.manage_rooms, name='manage_rooms'),
    path('manage_bookings/', views.manage_bookings, name='manage_bookings'),
    path('approve_application/<int:application_id>/', views.approve_application, name='approve_application'),
    path('cancel_application/<int:application_id>/', views.cancel_application, name='cancel_application'),
    path('reassign_room/<int:room_id>/', views.reassign_room, name='reassign_room'),
]