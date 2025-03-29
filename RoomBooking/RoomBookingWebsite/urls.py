from django.urls import path
from . import views

urlpatterns=[
    path("", views.home, name="home"),
    path('rooms/', views.room_browsing, name='room_browsing'),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
]