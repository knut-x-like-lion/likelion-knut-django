from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.


def index(request):
    queryset = TypeWrite.objects
    typewrite_result = ""
    for i in queryset.all():
        typewrite_result += "\""
        typewrite_result += i.__str__()
        typewrite_result += "\","
    typewrite_result = typewrite_result[:typewrite_result.__len__() - 1]

    return render(request, 'www/index.html', {'maxim': Maxim.objects, 'typewrite': typewrite_result})


def notice(request):
    return render(request, 'www/notice.html')
