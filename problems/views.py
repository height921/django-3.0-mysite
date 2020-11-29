import math
import re

import requests
from bs4 import BeautifulSoup
from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Problem, Category, SimpleCategory
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
    # 搜索实现
    search = request.GET.get('search', '')
    if search != '':
        problem_list = problem_list.filter(
            Q(title__contains=search) | Q(problem_id__contains=search))
    # 分页实现
    num = request.GET.get('num', 1)
    if num == '' or num == '0':
        num = 1
    paginator = Paginator(problem_list, 10)
    num = int(num)
    has_next = True
    if num > paginator.num_pages:
        num = paginator.num_pages
        has_next=False
    problem_list = paginator.page(num)
    begin = num - int(math.ceil(10.0 / 2))
    if begin < 1:
        begin = 1
    end = begin + 9
    if end > paginator.num_pages:
        end = paginator.num_pages
    if end <= 10:
        begin = 1
    else:
        begin = end - 9
    page_list = range(begin, end + 1)

    context = {
        'problem_list': problem_list,
        'difficulty': difficulty,
        'all_tag': Category.objects.values('title'),
        'tag': tag,
        'status': status,
        'num': num,
        'lnum': num - 1,
        'rnum': num + 1,
        'page_list': page_list,
        'search': search,
        'has_next': has_next,
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
            'category_list':Category.objects.all(),
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
        # 题目分类修改
        '''
        这里修改思路是，获取用户提交的类别，然后对题目的SimpleCategory投票数加1或者新建，
        然后选择投票数最高的两位添加到题目上
        '''
        simple_categories = SimpleCategory.objects.filter(problem=problem)
        for category_vote in category_list:
            is_in = False
            for simple_category in simple_categories:
                if category_vote == simple_category.title:
                    simple_category.vote_number += 1
                    simple_category.save()
                    is_in = True
                    break
            if not is_in:
                SimpleCategory.objects.create(title=category_vote, vote_number=1, problem=problem).save()
        categories_vote_max = SimpleCategory.objects.filter(problem=problem).order_by('-vote_number')[:2]
        problem.category.clear()
        for item in categories_vote_max:
            category = get_object_or_404(Category, title=item.title)
            print(category)
            problem.category.add(category)
        # 题目难度修改
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


def function_add_problem(search):

    url = 'http://acm.hdu.edu.cn/showproblem.php?pid=' + search
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "lxml")
    i = 0
    a = soup.find_all('div', class_='panel_content')
    b = soup.find_all('span')[0].text
    b = re.split(r" |    ", b)

    title = soup.find(name='h1').string
    description = a[0].text
    input_description = a[1].text
    output_description = a[2].text
    sample_input = a[3].text
    sample_output = a[4].text
    tlimit = int(re.findall(r"\d+", b[2])[1])
    mlimit = int(re.findall(r"\d+", b[7])[1])

    low = 0.02549062736759782
    high = 0.7068466730954677
    parameter = (high - low) / 9
    rat = int(b[14]) / int(b[11])
    p = Problem(
        problem_id=search,
        time_limit=tlimit,
        memory_limit=mlimit,
        title=title,
        description=description,
        input_description=input_description,
        output_description=output_description,
        sample_input=sample_input,
        sample_output=sample_output,
        source='HDU',
        difficulty=int(math.ceil((high - rat) / parameter)),
    )
    p.save()
    return p


def problems_add(request):

    category_list = Category.objects.all()
    context = {
        'category_list': category_list,
    }
    if request.method == 'GET':

        return render(request, 'problem_add.html', context=context)
    else:
        search = request.POST.get('search')
        categories = requests.post.get('categories')
        problem = function_add_problem(search)  # 添加单个题目
        for i in categories:
            category = Category.objects.get(id=i)
            problem.category.add(category)
    return render(request, 'problem_add.html', context=context)
