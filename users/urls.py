#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/13

from django.contrib import admin
from django.urls import path,include
import problems.views
from . import views
app_name = 'user'
urlpatterns = [
    path('', views.problems),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('findpassword/', views.find_password(), name='findpassword'),
]