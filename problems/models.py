from django.db import models
from datetime import datetime
from uuslug import slugify
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='类型')
    slug = models.SlugField(editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Problem(models.Model):
    slug = models.SlugField(editable=False)
    problem_id = models.CharField(max_length=20, primary_key=True, verbose_name='题目编号')
    time_limit_C = models.IntegerField(default=1000, verbose_name='时间限制')
    time_limit_other = models.IntegerField(default=1000, verbose_name='其他语言时间限制')
    memory_limit_C = models.IntegerField(default=65536, verbose_name='内存限制')
    memory_limit_other = models.IntegerField(default=65536, verbose_name='其他语言内存限制')
    title = models.CharField(max_length=1000, verbose_name='题目标题', blank=True)
    description = models.TextField(verbose_name='题目描述', blank=True)
    input_description = models.TextField(verbose_name='输入描述', blank=True)
    output_description = models.TextField(verbose_name='输出描述', blank=True)
    sample_input = models.TextField(verbose_name='样例输入', blank=True)
    sample_output = models.TextField(verbose_name='样例输出', blank=True)
    hint = models.TextField(blank=True, verbose_name='题目提示')
    source = models.CharField(max_length=200, blank=True, verbose_name='题目来源')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='题目添加时间')
    accepted = models.IntegerField(default=0, verbose_name='通过人数')
    submitted = models.IntegerField(default=0, verbose_name='提交人数')
    category = models.ManyToManyField(to=Category, verbose_name='类型',
                                      related_name='problem_category', null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.source)+str(self.problem_id))
        super(Problem, self).save(*args, **kwargs)

