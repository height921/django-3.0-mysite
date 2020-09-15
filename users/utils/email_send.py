#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/14
from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER


def random_str(random_length=8):
    '''
    获得一个随机字符串
    :param random_length:需要返回随机字符串的长度
    :return:随机的字符串
    '''
    string = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        string += chars[random.randint(0, length)]
    return string


def send_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'ACM题集与分析网站注册激活链接'
        email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(
            code)

        send_status = send_mail(
            email_title,
            email_body,
            EMAIL_HOST_USER,
            [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = 'ACM题集与分析网站密码重置链接'
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1:8000/user/resetpassword/{0}'.format(
            code)

        send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, [email])
        if send_status:
            pass
