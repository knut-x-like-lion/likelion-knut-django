from django.shortcuts import render
from .models import *


# Create your views here.


def index(request):
    maxim = Maxim.objects
    return render(request, 'www/index.html', {'maxim': maxim})


def notice(request):
    return render(request, 'www/notice.html')
