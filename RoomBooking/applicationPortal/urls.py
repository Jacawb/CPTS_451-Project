from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('', views.start, name="application-start"),
    path('page1/', views.pg1, name="application-pg1"),
    path('page2/', views.pg2, name="application-pg2"),
    path('page3/', views.pg3, name="application-pg3"),
    path('confirm/', views.confirmation, name="application-confirmation"),
    path('logout/', LogoutView.as_view(next_page='application-start'), name='logout'),
    path('userinfo/', views.userinfo, name='view_info'),
]