from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import JsonResponse
from django.shortcuts import render, redirect
from random import Random
from .forms import LoginForm, RegistrationForm, ForgetPasswordForm, ResetPassword
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from .utils.email_send import send_email
from .models import EmailVerifyRecord
from django.contrib.auth.hashers import make_password
# Create your views here.


def user_info(request):
    '''
    查看用户信息
    '''
    context = {

    }
    return render(request,'user_info.html', context)


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
            user.password=make_password(password=password2)
            user.save()
            print(155)
            return redirect('home')
        else:
            return redirect('home')


def login(request):
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
    return render(request, 'terms.html',{})


def check_user(request):
    res = {}
    username = request.GET.get('username')
    if username:
        if User.objects.filter(username=username).exist():
            res = {"code": 100, "msg": "用户名存在，请重新输入"}
        else:
            res = {"code": 101}
    else:
        res = {"code": 102, "msg": "请输入用户名"}

    return JsonResponse(res)


def check_email(request):
    res = {}
    email = request.GET.get('email')
    if email:
        if User.objects.filter(email=email).exist():
            res = {"code": 100, "msg": "邮箱以注册，请重新输入"}
        else:
            res = {"code": 101}
    else:
        res = {"code": 102, "msg": "请输入邮箱"}

    return JsonResponse(res)