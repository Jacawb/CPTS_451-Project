from django.urls import path
from . import views

urlpatterns=[
    path("", views.home, name="home"),
    path('rooms/', views.room_browsing, name='room_browsing'),
    path('', views.start, name="application-start"),
    path('page1/', views.pg1, name="application-pg1"),
    path('page2/', views.pg2, name="application-pg2"),
    path('confirm/', views.confirmation, name="application-confirmation"),
    path("signup/", authView, name="authView"),
 path("accounts/", include("django.contrib.auth.urls")),
]