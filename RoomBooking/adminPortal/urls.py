from django.urls import path
from . import views

urlpatterns = [
    # Example view
    path("", views.admin_home, name="admin_home"),
]