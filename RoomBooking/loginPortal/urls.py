from django.urls import path, include
from .views import RegistrationPage, home,LoginPage


urlpatterns=[
    path('', LoginPage, name="login"),
    path("register/", RegistrationPage, name="register"),
    #path("accounts/", include("django.contrib.auth.urls")),
]


