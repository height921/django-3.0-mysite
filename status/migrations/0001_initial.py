# Generated by Django 3.0.8 on 2020-09-20 03:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problems', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=200, verbose_name='结果')),
                ('time', models.IntegerField(verbose_name='时间')),
                ('memory', models.IntegerField(verbose_name='内存')),
                ('code_length', models.IntegerField(verbose_name='代码长度')),
                ('lang', models.CharField(max_length=200, verbose_name='语言')),
                ('submit_time', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problem_status', to='problems.Problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_status', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
