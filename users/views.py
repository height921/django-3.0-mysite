import time
from datetime import timedelta, datetime

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth import authenticate
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from random import Random

from django.utils.timezone import now

from problems.models import Category
from .forms import LoginForm, RegistrationForm, ForgetPasswordForm, ResetPassword
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from .utils.email_send import send_email
from .models import EmailVerifyRecord
from django.contrib.auth.hashers import make_password
from status.models import Status
# Create your views here.


def user_info(request):
    '''
    查看用户信息
    '''
    if request.user.is_authenticated:
        # 提交总数和ac总数
        submission_num = Status.objects.filter(user=request.user).count()
        ac_num = Status.objects.filter(user=request.user).values('problem__slug').distinct().count()

        # 各个分类对应的做题数和ac数
        category_x_list = []
        category_y_submit_list = []
        category_y_ac_list = []
        category_list = Category.objects.all()
        for category in category_list:
            category_x_list.append(category.title)
            category_y_submit_list.append(Status.objects.filter(user=request.user,problem__category=category).count())
            category_y_ac_list.append(Status.objects.filter(user=request.user,
                                                            problem__category=category, is_first_ac=True).count())
        # 判断是返回一个月的数据还是从第一次提交开始算起
        nowadays = datetime.now()
        a_month = datetime.now() - timedelta(days=30)

        if Status.objects.filter(user=request.user,is_first_submit=True).exists():
            first_submit_time = Status.objects.get(user=request.user,is_first_submit=True).submit_time
            if first_submit_time>a_month:
                a_month=first_submit_time

        # 最近一个月的题目或者从第一次提交到现在的题目
        select = {'day': 'date(submit_time)'}
        count_data = Status.objects. \
            filter(submit_time__range=(a_month, nowadays),user=request.user). \
            extra(select=select).\
            values('day').order_by("day").annotate(number=Count('submit_time'))
        submit_x_list = []
        submit_y_list = []
        ac_y_list = []
        ac_x_list = []
        for i in count_data:
            print(type(i['day']))
            submit_x_list.append(str(i['day']))
            submit_y_list.append(i['number'])
        count_data = Status.objects. \
            filter(submit_time__range=(a_month, nowadays), user=request.user,is_first_ac=True). \
            extra(select=select).values('day').order_by("day").annotate(number=Count('submit_time'))
        for i in count_data:
            ac_x_list.append(str(i['day']))
            ac_y_list.append(i['number'])
        submit_index=0
        ac_index=0
        submit_x=[]
        submit_y=[]
        ac_y=[]
        for i in range((nowadays - a_month).days + 1):
            day = (a_month + timedelta(days=i)).strftime("%Y-%m-%d")
            submit_x.append(day)
            if day in submit_x_list:
                submit_y.append(submit_y_list[submit_index])
                submit_index+=1
            else:
                submit_y.append(0)
            if day in ac_x_list:
                ac_y.append(ac_y_list[ac_index])
                ac_index+=1
            else:
                ac_y.append(0)

        context = {
            'submission_num': submission_num,
            'AC_num': ac_num,
            'submit_x_list': submit_x,
            'submit_y_list': submit_y,
            'AC_y_list': ac_y,
            'category_x': category_x_list,
            'category_y_submit': category_y_submit_list,
            'category_y_AC': category_y_ac_list,
        }
        return render(request, 'user_info.html', context)
    else:
        return render(request, 'home.html', {})


def forget_password(request):
    if request.method == 'GET':
        form = ForgetPasswordForm()
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_email(email, 'forget')
            return render(request, 'send_success.html')
    return render(request, 'forget_password.html', {'form': form})


def reset_password(request, active_code):
    if request.method == 'GET':
        record = EmailVerifyRecord.objects.filter(code=active_code)
        if record:
            for item in record:
                email = item.email
                demo = User.objects.filter(email=email)
                if demo:
                    context = {
                        'email': email,
                        'form': ResetPassword(),
                        'code': active_code,
                    }
                    return render(request, 'reset_password.html', context=context)
        return redirect('home')
    else:
        form = ResetPassword(request.POST)
        print(333)
        if form.is_valid():
            print(1222)
            password2 = form.cleaned_data['password2']
            email = request.POST.get('email')
            print(email)
            user = User.objects.get(email=email)
            user.password = make_password(password=password2)
            user.save()
            print(155)
            return redirect('home')
        else:
            return redirect('home')


def login(request):
    if request.is_ajax():
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            auth.login(request, user)
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error"})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return redirect(request.GET.get('from', reverse('home')))

    return render(request, 'login.html', {})


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def register(request):
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        print('进入post')
        if register_form.is_valid():
            print('进入form')
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password1']
            email = register_form.cleaned_data['email']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    key = CaptchaStore.generate_key()
    image_url = captcha_image_url(key)
    context = {
        'key': key,
        'image_url': image_url,
    }
    return render(request, 'register.html', context)


def terms(request):
    '''
    服务条款
    :param request:
    :return:
    '''
    return render(request, 'terms.html', {})


def check_user(request):
    res = {}
    username = request.GET.get('username')
    print(username)
    if username:
        if User.objects.filter(username=username).exists():
            print('用户名存在')
            res = {"code": 100, "msg": "用户名存在，请重新输入"}
        else:
            res = {"code": 101}
    else:
        res = {"code": 102, "msg": "请输入用户名"}

    return JsonResponse(res)


def check_captcha(request):
    print('检查验证码')
    res = {}
    captcha_0 = request.GET.get('captcha_0')
    captcha_1 = request.GET.get('captcha_1')
    if captcha_1:
        if CaptchaStore.objects.filter(response=captcha_1, hashkey=captcha_0):
            print('验证码正确')
            res = {"code": 101}
        else:
            res = {"code": 100, "msg": "验证码错误，请重新输入"}
    else:
        res = {"code": 102, "msg": "请输入验证码"}

    return JsonResponse(res)


def check_email(request):
    res = {}
    email = request.GET.get('email')
    if email:
        if User.objects.filter(email=email).exists():
            res = {"code": 100, "msg": "该邮箱已经注册，请重新输入"}
        else:
            res = {"code": 101}
    else:
        res = {"code": 102, "msg": "请输入邮箱"}

    return JsonResponse(res)


def questionnaire(request):
    return render(request, 'questionnaire.html')


def reset_pwd2(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            password = request.POST['new_password1']
            if password == '':
                render(request, 'reset_password2.html')
            request.user.set_password(password)
            request.user.save()
            auth.authenticate(username=request.user.username, password=password)
            auth.login(request, request.user)
            return redirect(request.GET.get('from', reverse('home')))
        return render(request, 'reset_password2.html')
    else:
        return render(request,'home.html',{})