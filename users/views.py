from django.shortcuts import render
from random import Random
# Create your views here.


def random_str(random_length=8):
    string = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(random_length):
        string += chars[random.randint(0, length)]
    return string


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    return render()


def logout(request):
    return render()


def register(request):
    return render()


def find_password(request):
    return render()
