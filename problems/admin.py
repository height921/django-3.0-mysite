from django.contrib import admin
from .models import Category, Problem,SubmitAccount
# Register your models here.


admin.site.register(Category)
admin.site.register(Problem)
admin.site.register(SubmitAccount)