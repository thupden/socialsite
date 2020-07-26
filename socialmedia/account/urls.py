from django.urls import path
from django.contrib import admin
from . import views

urlpatterns =[
    path('',views.home,name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('change_password/', views.Change_Password.as_view(), name="changePassword"),
]