#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/11

from django.urls import path, re_path
from . import views
app_name = 'problem'
urlpatterns = [
    path('', views.problems, name='problem_list'),
    path('<slug:slug>/', views.problem_detail, name='problem_detail'),
    # path('submit_code/', views.submit_code, name='submit_code'),
    path('category/<slug:slug>', views.problem_category, name='problem_category'),
    # re_path(r'(?P<difficulty>\d+)/(?P<category>)/(?P<status>)/', views.problems)
    path('modify_category_difficulty', views.modify_category_difficulty, name='modify_category_difficulty'),
]