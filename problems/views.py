from django.shortcuts import render
from .models import Problem
# Create your views here.


def problems(request):
    problem_list = Problem.objects.all()
    context = {
        'problems': problem_list,
    }
    return render(request, 'problems.html', context=context)


def problem_detail(request, slug):
    problem = Problem.objects.get(slug=slug)
    context = {
        'problem': problem,
    }
    return render(request, 'problem_detail.html', context=context)
