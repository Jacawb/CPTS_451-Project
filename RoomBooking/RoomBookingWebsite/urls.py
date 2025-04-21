from django.urls import path, include
from . import views

urlpatterns=[
    path('', views.start, name="application-start"),
    path('page1/', views.pg1, name="application-pg1"),
    path('page2/', views.pg2, name="application-pg2"),
    path('page3/', views.pg3, name="application-pg3"),
    path('confirm/', views.confirmation, name="application-confirmation"),
    path('rooms/', views.room_browsing, name='room_browsing'),
    path("signup/", views.authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
]