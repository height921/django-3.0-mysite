#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/10/11

from django import template
from django.contrib.contenttypes.models import ContentType
from status.models import Status
register = template.Library()


@register.simple_tag(takes_context=True)
def get_status(context, obj):
    user = context['user']
    content_type = ContentType.objects.get_for_model(obj)
    if not user.is_authenticated:
        return ''
    results = Status.objects.filter(problem=obj, user=user)
    if results:
        if results.filter(result="Accepted"):
            return 'fa-check fa-check-color'
        return 'fa-question fa-question-color'
    return ''
