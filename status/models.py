from django.db import models
from problems.models import Problem
from django.contrib.auth.models import User
# Create your models here.

# 提交后的状态


class Status(models.Model):
    # source = models.CharField(max_length=200, blank=True, verbose_name='题目来源')
    result = models.CharField(max_length=200, blank=False, verbose_name='结果')
    time = models.IntegerField(verbose_name='时间')
    memory = models.IntegerField(verbose_name='内存')
    code_length = models.IntegerField(verbose_name='代码长度')
    lang = models.CharField(max_length=200, verbose_name='语言')
    submit_time = models.TimeField(auto_created=True, verbose_name='提交时间')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problem_status')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_status')
