#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/11

from django.contrib import admin
from django.urls import path,include
import problems.views
from . import views
app_name = 'problem'
urlpatterns = [
    path('', views.problems),
    path('<slug:slug>/', views.problem_detail, name='problem_detail'),
]