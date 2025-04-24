from django.urls import path, include
from .views import authView, home,LoginPage


urlpatterns=[
    path('', LoginPage, name="login"),
    path('home/', home, name='home'),
    path("signup/", authView, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
]


