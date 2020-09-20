#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/11
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', context={})


def about(request):
    return render(request, 'about.html', context={})


def contact_us(request):
    return render(request, 'contact_us.html', context={})