# Generated by Django 3.0.8 on 2020-09-17 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='类型')),
                ('content', models.TextField(default='', verbose_name='介绍')),
                ('slug', models.SlugField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('slug', models.SlugField(editable=False)),
                ('problem_id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='题目编号')),
                ('time_limit', models.IntegerField(default=1000, verbose_name='时间限制')),
                ('memory_limit', models.IntegerField(default=65536, verbose_name='内存限制')),
                ('title', models.CharField(blank=True, max_length=1000, verbose_name='题目标题')),
                ('description', models.TextField(blank=True, verbose_name='题目描述')),
                ('input_description', models.TextField(blank=True, verbose_name='输入描述')),
                ('output_description', models.TextField(blank=True, verbose_name='输出描述')),
                ('sample_input', models.TextField(blank=True, verbose_name='样例输入')),
                ('sample_output', models.TextField(blank=True, verbose_name='样例输出')),
                ('hint', models.TextField(blank=True, verbose_name='题目提示')),
                ('source', models.CharField(blank=True, max_length=200, verbose_name='题目来源')),
                ('accepted', models.IntegerField(default=0, verbose_name='通过人数')),
                ('submitted', models.IntegerField(default=0, verbose_name='提交人数')),
                ('category', models.ManyToManyField(blank=True, related_name='problem_category', to='problems.Category', verbose_name='类型')),
            ],
        ),
    ]
