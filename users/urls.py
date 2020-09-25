#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/13

from django.contrib import admin
from django.urls import path,include
import problems.views
from . import views
app_name = 'user'
urlpatterns = [
    path('', views.user_info, name='user_info'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forgetpassword/', views.forget_password, name='forgetpassword'),
    path('resetpassword/<str:active_code>', views.reset_password, name='resetpassword'),
    path('terms/', views.terms, name='terms'),
    path('register/check_email/', views.check_email, name='check_email'),
    path('register/check_user/', views.check_user, name='check_user'),
    path('register/check_captcha/', views.check_captcha, name='check_captcha'),
    path('logout/', views.logout, name='logout'),
]