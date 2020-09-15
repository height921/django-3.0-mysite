from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile')


class EmailVerifyRecord(models.Model):
    """邮箱激活码"""
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(verbose_name='验证码类型', choices=(('register', '注册'), ('forget', '忘记密码')),
                                 max_length=20)
    send_time = models.DateTimeField(verbose_name='发送时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)
