# Generated by Django 3.0.8 on 2020-09-12 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_auto_20200912_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='123', editable=False),
        ),
        migrations.AddField(
            model_name='problem',
            name='slug',
            field=models.SlugField(default='234', editable=False),
        ),
    ]