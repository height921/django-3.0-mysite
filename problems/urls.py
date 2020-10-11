#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/11

from django.urls import path
from . import views
app_name = 'problem'
urlpatterns = [
    path('', views.problems, name='problem_list'),
    path('<slug:slug>/', views.problem_detail, name='problem_detail'),
    path('category/<slug:slug>', views.problem_category, name='problem_category'),
    path('modify_category_difficulty', views.modify_category_difficulty, name='modify_category_difficulty'),
]