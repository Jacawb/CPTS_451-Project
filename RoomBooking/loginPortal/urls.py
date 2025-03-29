from django.urls import path
from . import views

urlpatterns=[
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
]


