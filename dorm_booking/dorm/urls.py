from django.urls import path
from .views import register_view, login_view, logout_view, maintenance_request_view, maintenance_success_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('maintenance/', maintenance_request_view, name='maintenance_request'),
    path('maintenance/success/', maintenance_success_view, name='maintenance_success'),
]
