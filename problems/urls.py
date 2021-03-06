#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/11

from django.urls import path
from . import views
app_name = 'problem'
urlpatterns = [
    path('', views.problems, name='problem_list'),
    path('<slug:slug>/', views.problem_detail, name='problem_detail'),
    path('category',views.problem_all_category, name='problem_all_category'),
    path('category/<slug:slug>', views.problem_category, name='problem_category'),
    path('modify_category_difficulty', views.modify_category_difficulty, name='modify_category_difficulty'),
    path('recommend', views.problem_recommend, name='problem_recommend'),
    path('problem_add', views.problems_add, name='problem_add'),
]