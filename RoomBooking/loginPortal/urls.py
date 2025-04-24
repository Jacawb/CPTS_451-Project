from django.urls import path, include
from .views import authView, home,LoginPage


urlpatterns=[
    path('home/', home, name='home'),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", LoginPage, name="LoginPage"),
]


