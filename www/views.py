from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

import threading
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
        return _auth_controls(request, typewrite_result)
    else:
        if request.user.is_authenticated:
            edit_password_form = EditPassword()
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            return render(request, 'www/index.html',
                          {'maxim': Maxim.objects, 'typewrite': typewrite_result, 'profile_form': profile_form, 'edit_password_form': edit_password_form})
        return render(request, 'www/index.html', {'maxim': Maxim.objects, 'typewrite': typewrite_result, 'reset_password_form': ResetPassword()})


def posts(request):
    return render(request, 'www/posts.html', {'posts': Post.objects.order_by('-date_created')})


def post(request, post_url):
    content = Post.objects.get(title=post_url)
    return render(request, 'www/post.html', {'post': content})


def team(request):
    operators = User.objects.filter(is_staff=True, is_superuser=False).select_related('advanceduser')
    User.objects.get(is_staff=True)
    members = User.objects.filter(is_staff=False)
    return render(request, 'www/team.html', {'operators': operators, 'members': members})


def portfolio(request):
    return render(request, 'www/portfolio.html')


def error404(request):
    return render(request, 'www/404.html')


def _auth_controls(request, typewrite_result):
    if request.POST['submit_type'] == "login":
        user = auth.authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'www/index.html', {'maxim': Maxim.objects, 'typewrite': typewrite_result, 'flash_data': 'failedLogin'})
    elif request.POST['submit_type'] == "signup":
        if request.POST['password'] == request.POST['password-verify']:
            try:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
                advanced_user = AdvancedUser(user_id=user.id)
                advanced_user.save()
                auth.login(request, user)
            except IntegrityError:
                flash_data = 'failedSignup'
            else:
                flash_data = 'successSignup'
        else:
            flash_data = 'notMatchPassword'
        return render(request, 'www/index.html', {'maxim': Maxim.objects, 'typewrite': typewrite_result, 'flash_data': flash_data})
    elif request.POST['submit_type'] == "logout":
        auth.logout(request)
        return HttpResponseRedirect('/')
    elif request.POST['submit_type'] == "edit_profile":
        try:
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
    elif request.POST['submit_type'] == "edit_password":
        if check_password(request.POST['current_password'], request.user.password):
            if request.POST['password'] == request.POST['password_verify']:
                request.user.set_password(request.POST['password'])
                request.user.save()
                return HttpResponseRedirect('/')
    elif request.POST['submit_type'] == "reset_password":
        try:
            user = User.objects.get(email=request.POST['email'])
            password = User.objects.make_random_password(length=20)
            user.set_password(password)
            user.save()
            mailing = EmailThread('비밀번호 변경', '', 'likelionknut@gmail.com', ['cr3ux53c@gmail.com'], False, '<h1>' + password + '</h1>')
            mailing.start()
        except User.DoesNotExist:
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, 'text/html')
        msg.send(self.fail_silently)


def send_email(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()
