from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name="application-start"),
    path('page1/', views.pg1, name="application-pg1"),
    path('page2/', views.pg2, name="application-pg2"),
    path('confirm/', views.confirmation, name="application-confirmation"),
]