#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/11

from django.urls import path
from . import views
app_name = 'problem'
urlpatterns = [
    path('', views.problems, name='problem_list'),
    path('<slug:slug>/', views.problem_detail, name='problem_detail'),
    # path('submit_code/', views.submit_code, name='submit_code'),
    path('category/<slug:slug>', views.problem_category, name='problem_category'),
]