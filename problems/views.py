import re

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Problem, Category
from .utils.submit_code import HDUSubmit, main_function
from status.models import Status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from uuslug import slugify


# Create your views here.


def problems(request):
    '''
    题目列表,这里的tag就是model中的category，status指的该用户是否AC
    :param request:
    :return:
    '''
    problem_list = Problem.objects.all()
    if request.session.get('not_first', False):
        difficulty = request.session.get('difficulty', '')
        difficulty = request.GET.get('difficulty', difficulty)
        difficulty_num = re.sub("\D", "", difficulty)
        tag = request.session.get('tag', '')
        tag = request.GET.get('tag', tag)
        status = request.session.get('status', '')
        status = request.GET.get('status', status)
    else:
        difficulty = '难度'
        tag = '标签'
        status = '状态'
        request.session['not_first'] = True
        request.session['difficulty'] = difficulty
        request.session['tag'] = tag
        request.session['status'] = status
    print('status', status)
    if status != '状态':
        if status == '已通过':
            status_list = Status.objects.filter(user=request.user)
            status_list = status_list.filter(result='Accepted')
            problem_list = [item.problem for item in status_list]
        if status == '未通过':
            status_list = Status.objects.filter(user=request.user)
            status_list = status_list.filter(~Q(result='Accepted'))
            problem_list = [item.problem for item in status_list]
        if status == '未做':
            problem_has_done = Status.objects.filter(user=request.user).values('problem')[0]
            print('problem_has_done', problem_has_done)
            # 还没写完呢
            pass
    if difficulty != '难度':
        problem_list = Problem.objects.filter(difficulty=difficulty_num)
    if tag != '标签':
        if tag == '未分类':
            problem_list = problem_list.filter(category=None)
        else:
            category = Category.objects.get(title=tag)
            problem_list = problem_list.filter(category=category)

    context = {
        'problem_list': problem_list,
        'difficulty': difficulty,
        'all_tag': Category.objects.values('title'),
        'tag': tag,
        'status': status,
    }
    return render(request, 'problems.html', context=context)


def problem_detail(request, slug):
    print("进入detail")
    '''
    题目的详细内容,
    post请求是返回答题结果
    :param request:
    :param slug:
    :return:
    '''
    if request.method == 'GET':
        problem = get_object_or_404(Problem, slug=slug)
        context = {
            'problem': problem,
        }
        return render(request, 'problem_detail.html', context=context)
    else:
        print("进入了post")
        source = request.POST.get('source', '')
        code = request.POST.get('code', '')
        language = request.POST.get('language', '')
        problem_id = request.POST.get('problem_id', '')
        print(source, code)
        problem = get_object_or_404(Problem, slug=slug)
        # status=Status.objects.create(result='waiting',
        #                              time=0,
        #                              memory=0,
        #                              code_length=0,
        #                              lang=language,
        #                              user=request.user,
        #                              problem=problem)
        # status.save()
        result = main_function(source, code, language, problem_id)
        print("result")
        print(result)
        if isinstance(result, str):
            return JsonResponse({"status": "submit failed"})
        else:
            if result.get('result') == "Accepted":
                problem.accepted += 1
                if Status.objects.filter(user=request.user).exists():
                    is_first = False
                else:
                    is_first = True
                if Status.objects.filter(result='Accepted', user=request.user, problem=problem).exists():
                    is_first_ac = False
                else:
                    is_first_ac = True
            status = Status.objects.create(result=result.get('result'),
                                           time=result.get('time', 0) if result.get('time', 0) != '' else 0,
                                           memory=result.get('memory', 0) if result.get('memory', 0) != '' else 0,
                                           code_length=result.get('code_length'),
                                           lang=result.get('lang'),
                                           # submit_time=result.get('submit_time'),
                                           user=request.user,
                                           problem=problem,
                                           is_first_ac=is_first_ac,
                                           is_first_submit=is_first,
                                           )
            status.save()
            problem.submitted += 1
            problem.pass_rate = problem.accepted / problem.submitted * 100
            problem.save()
            data = {
                "status": "success",
                "result": status.result,
            }
            return JsonResponse(data=data)


def modify_category_difficulty(request):
    print("进入modify")
    pk = request.GET.get("pk")
    problem = Problem.objects.filter(pk=pk).first()
    if problem:
        category_list = request.GET.getlist("category")
        difficulty = int(request.GET.get("difficulty"))
        categories = problem.category.all()

        for category_vote in category_list:
            for category in categories:
                if category_vote == category.title:
                    category.vote_number += 1
                    category.save()
                    break

        num = problem.participants
        problem.difficulty = (num * problem.difficulty + difficulty) // (num + 1)
        problem.save()
        data = {
            "status": "success",
        }
        return JsonResponse(data=data)
    return JsonResponse(data={"status": "error"})


def problem_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    problem_list = Problem.objects.filter(category=category)
    context = {
        'problem_list': problem_list,
        'category': category,
    }
    return render(request, 'problem_category.html', context=context)


def problem_all_category(request):
    category_list = Category.objects.all()
    context = {
        'category_list': category_list,
    }
    return render(request, 'problem_all_category.html', context=context)


def problem_recommend(request):
    return render(request, 'problem_recommend.html')
