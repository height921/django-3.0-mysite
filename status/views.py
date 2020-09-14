from django.shortcuts import render
from .models import Status
# Create your views here.


def status(request):
    status_list = Status.objects.all().order_by('submit_time')
    context = {
        'status_list': status_list,
    }
    return render(request, 'status.html', context=context)