#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/11
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', context={})