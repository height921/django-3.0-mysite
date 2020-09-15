#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/14
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from captcha.fields import CaptchaField
import re


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50)
    email = forms.EmailField(label='邮箱')
    password1 = forms.CharField(label='密码',
                                required=True,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='请再次输入密码',
                                required=True,
                                widget=forms.PasswordInput)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username)>50:
            raise forms.ValidationError('用户名太长了')
        else:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('用户名已经存在')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('此邮箱已经注册')
        else:
            raise forms.ValidationError('请输入正确的邮箱')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError('密码太短了')
        elif len(password1) > 16:
            raise forms.ValidationError('密码太长了')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('两次输入不一样，请重新输入')
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               required=True,
                               max_length=50,
                               widget=forms.TextInput(attrs={
                                   'placeholder': '请输入用户名',
                               }))
    password = forms.CharField(label='密码',
                               required=True,
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': '请输入密码',
                               }))
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class ForgetPasswordForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50)
    email = forms.EmailField(label='邮箱')
    captcha = CaptchaField(label='验证码', error_messages={'invalid': '验证码错误'})

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if not User.objects.filter(email=email, username=username).exists():
            raise forms.ValidationError('用户名或邮箱错误')

        return self.cleaned_data


class ResetPassword(forms.Form):
    password1 = forms.CharField(required=True,
                                label='密码',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(required=True,
                                label='请再次输入密码密码',
                                widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError('密码太短了')
        elif len(password1) > 16:
            raise forms.ValidationError('密码太长了')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('两次输入不一样，请重新输入')
        return password2