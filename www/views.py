from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import *
from .form import *


# Create your views here.


def index(request):
    queryset = TypeWrite.objects
    typewrite_result = ""
    for i in queryset.all():
        typewrite_result += "\""
        typewrite_result += i.__str__()
        typewrite_result += "\","
    typewrite_result = typewrite_result[:typewrite_result.__len__() - 1]
    # todo  return render에 flash_data만 인수로 하고 중복 제거
    # todo ajax로 로그인/가입 비밀번호 불일치 처리
    if request.method == "POST":
        if request.POST['submit_type'] == "login":
            user = auth.authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'www/index.html', {'maxim': Maxim.objects, 'typewrite': typewrite_result, 'flash_data': 'failedLogin'})
        elif request.POST['submit_type'] == "signup":
            if request.POST['password'] == request.POST['password-verify']:
                try:
                    User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
                except IntegrityError:
                    return render(request, 'www/index.html', {'maxim': Maxim.objects, 'typewrite': typewrite_result, 'flash_data': 'failedSignup'})
                except ArithmeticError:
                    pass
                else:
                    return render(request, 'www/index.html', {'maxim': Maxim.objects, 'typewrite': typewrite_result, 'flash_data': 'successSignup'})
            else:
                return render(request, 'www/index.html', {'maxim': Maxim.objects, 'typewrite': typewrite_result, 'flash_data': 'notMatchPassword'})
        elif request.POST['submit_type'] == "logout":
            auth.logout(request)
            return HttpResponseRedirect('/')
        elif request.POST['submit_type'] == "edit_profile":
            try:
                request.POST['picture']

                instance_user = AdvancedUser.objects.get(user_id=auth.get_user(request).id)
                form_data = EditProfile(request.POST, request.FILES, instance=instance_user)
                if form_data.is_valid():
                    obj = form_data.save(commit=False)
                    obj.user = request.user
                    obj.save()
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/')
            except AdvancedUser.DoesNotExist:
                form_data = EditProfile(request.POST)
                if form_data.is_valid():
                    obj = form_data.save(commit=False)
                    obj.user = request.user
                    obj.save()
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/')
        else:
            # todo 알수 없는 오류(오류코드 1)
            return HttpResponseRedirect('/')
    else:
        if request.user.is_authenticated:
            #     old_data = AdvancedUser.objects.get(user_id=auth.get_user(request).id)
            #     form_data = EditProfile(instance=old_data)
            return render(request, 'www/index.html', {'maxim': Maxim.objects, 'typewrite': typewrite_result, 'profile': EditProfile()})
        return render(request, 'www/index.html', {'maxim': Maxim.objects, 'typewrite': typewrite_result})


def notice(request):
    return render(request, 'www/notice.html')
