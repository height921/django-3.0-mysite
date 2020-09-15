from django.shortcuts import render
from .models import Problem
# Create your views here.


def problems(request):
    '''
    题目列表
    :param request:
    :return:
    '''
    problem_list = Problem.objects.all()
    context = {
        'problems': problem_list,
    }
    return render(request, 'problems.html', context=context)


def problem_detail(request, slug):
    '''
    题目的详细内容
    :param request:
    :param slug:
    :return:
    '''
    problem = Problem.objects.get(slug=slug)
    context = {
        'problem': problem,
    }
    return render(request, 'problem_detail.html', context=context)


def submit_code(request):
    source = request.POST.get('source')
    code = request.POST.get('code')
    language = request.POST.get('language')
    problem_id = request.POST.get('problem_id')
    result = ''
    return result
