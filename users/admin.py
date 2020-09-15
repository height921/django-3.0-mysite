from django.contrib import admin
from .models import EmailVerifyRecord
# Register your models here.


class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)