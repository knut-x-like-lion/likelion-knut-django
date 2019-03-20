from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

import threading
from .models import *
from .form import *


# Create your views here.
# todo ajax로 로그인/가입 비밀번호 불일치 처리


class FaqView(View):
    def get(self, request):
        if request.user.is_authenticated:
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            return render(request, 'www/faq.html', {'profile_form': profile_form, 'edit_password_form': EditPassword(), 'faq_1': Faq.objects.filter(tag_id=1), 'faq_2': Faq.objects.filter(tag_id=2)})
        return render(request, 'www/faq.html', {'reset_password_form': ResetPassword(), 'faq_1': Faq.objects.filter(tag_id=1), 'faq_2': Faq.objects.filter(tag_id=2)})


class Auth(View):
    pass


class IndexView(View):

    def post(self, request):
        typewrite_result = ""
        for i in TypeWrite.objects.all():
            typewrite_result += "\""
            typewrite_result += i.__str__()
            typewrite_result += "\","
        typewrite_result = typewrite_result[:typewrite_result.__len__() - 1]
        return auth_controls(request, typewrite_result)

    def get(self, request):
        typewrite_result = ""
        for i in TypeWrite.objects.all():
            typewrite_result += "\""
            typewrite_result += i.__str__()
            typewrite_result += "\","
        typewrite_result = typewrite_result[:typewrite_result.__len__() - 1]
        if request.user.is_authenticated:
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            return render(request, 'www/index.html', {'profile_form': profile_form, 'edit_password_form': EditPassword(), 'maxim': Maxim.objects, 'typewrite': typewrite_result})
        return render(request, 'www/index.html', {'reset_password_form': ResetPassword(), 'maxim': Maxim.objects, 'typewrite': typewrite_result})


class TeamView(View):
    def post(self, request):
        return auth_controls(request, '')

    def get(self, request):
        operators = User.objects.filter(is_staff=True, is_superuser=False).select_related('advanceduser').order_by('-date_joined')
        # todo  쿼리 최적화
        members = User.objects.filter(is_staff=False, is_superuser=False).select_related('advanceduser').order_by('-date_joined')
        members = members.raw('SELECT * FROM auth_user JOIN www_member ON auth_user.email = www_member.email')

        if request.user.is_authenticated:
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            return render(request, 'www/team.html', {'profile_form': profile_form, 'edit_password_form': EditPassword(), 'operators': operators, 'members': members})
        return render(request, 'www/team.html', {'reset_password_form': ResetPassword(), 'operators': operators, 'members': members})


class NoticeContentView(View):
    def get(self, request, title):
        if request.user.is_authenticated:
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            return render(request, 'www/notice.html',
                          {'profile_form': profile_form, 'edit_password_form': EditPassword(), 'posts': Notice.objects.order_by('-date_created'), 'notice': Notice.objects.get(title=title)})
        return render(request, 'www/notice.html', {'reset_password_form': ResetPassword(), 'posts': Notice.objects.order_by('-date_created'), 'notice': Notice.objects.get(title=title)})


class NoticeListView(View):
    def post(self, request):
        return auth_controls(request, '')

    def get(self, request):
        if request.user.is_authenticated:
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            return render(request, 'www/notice_list.html', {'profile_form': profile_form, 'edit_password_form': EditPassword(), 'notice': Notice.objects.order_by('-date_created')})
        return render(request, 'www/notice_list.html', {'reset_password_form': ResetPassword(), 'notice': Notice.objects.order_by('-date_created')})


class NoticeNewView(View):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                form_data = NewPortfolio(request.POST, request.FILES)
                # form_data.author = auth.get_user(request).username
                if form_data.is_valid():
                    form_data.save()
                    # obj = form_data.save(commit=False)
                    # obj.user = request.user
                    # obj.save()
                    return HttpResponseRedirect('/assignment')
                else:
                    raise Exception
            except Exception:
                return HttpResponseRedirect('/assignment', {'flash_data': '제출 과정에서 오류가 발생했습니다.'})

    def get(self, request):
        if request.user.is_authenticated:
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            return render(request, 'www/portfolio_new.html', {'profile_form': profile_form, 'edit_password_form': EditPassword(), 'notice_form': NewPortfolio()})
        return HttpResponseRedirect('/notice')


#
# def post(request, post_url):
#     content = Post.objects.get(title=post_url)
#     return render(request, 'www/post.html', {'post': content})


class PortfolioView(View):
    def get(self, request):
        if request.user.is_authenticated:
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            return render(request, 'www/portfolio.html', {'profile_form': profile_form, 'edit_password_form': EditPassword(), 'assignments': Portfolio.objects.order_by('-datetime_created')})
        return render(request, 'www/portfolio.html', {'reset_password_form': ResetPassword(), 'posts': Portfolio.objects.order_by('-datetime_created')})


class AssignmentGetView(View):

    def get(self, request, assignment_url):
        if request.user.is_authenticated:
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            return render(request, 'www/assignment.html', {'profile_form': profile_form, 'edit_password_form': EditPassword(), 'assignment': Portfolio.objects.get(id=assignment_url)})
        return render(request, 'www/assignment.html', {'reset_password_form': ResetPassword(), 'posts': Portfolio.objects.order_by('-date_created')})


class AssignmentEditView(View):

    def post(self, request, assignment_url):
        if request.user.is_authenticated:
            try:
                form_data = NewPortfolio(request.POST, request.FILES)
                # form_data.author = auth.get_user(request).username
                if form_data.is_valid():
                    assignment = Portfolio.objects.get(id=assignment_url)
                    assignment.title = request.POST['title']
                    assignment.content = request.POST['content']
                    assignment.file = request.POST['file']
                    assignment.save()
                    return HttpResponseRedirect('/assignment')
                else:
                    raise Exception
            except Exception:
                return HttpResponseRedirect('/assignment', {'flash_data': '제출 과정에서 오류가 발생했습니다.'})

    def get(self, request, assignment_url):
        if request.user.is_authenticated:
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            assignment_form = NewPortfolio(instance=Portfolio.objects.get(id=assignment_url))
            return render(request, 'www/assignment_new.html', {'profile_form': profile_form, 'edit_password_form': EditPassword(), 'assignment_form': assignment_form})
        return render(request, 'www/assignment_new.html', {'reset_password_form': ResetPassword(), 'posts': Portfolio.objects.order_by('-date_created')})


class AssignmentNewView(View):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                form_data = NewPortfolio(request.POST, request.FILES)
                # form_data.author = auth.get_user(request).username
                if form_data.is_valid():
                    form_data.save()
                    # obj = form_data.save(commit=False)
                    # obj.user = request.user
                    # obj.save()
                    return HttpResponseRedirect('/assignment')
                else:
                    raise Exception
            except Exception:
                return HttpResponseRedirect('/assignment', {'flash_data': '제출 과정에서 오류가 발생했습니다.'})

    def get(self, request):
        if request.user.is_authenticated:
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            return render(request, 'www/assignment_new.html', {'profile_form': profile_form, 'edit_password_form': EditPassword(), 'assignment_form': NewAssignment()})
        return HttpResponseRedirect('/assignment')


def portfolio(request):
    return render(request, 'www/portfolio.html')


def error404(request):
    return render(request, 'www/404.html')


def auth_controls(request, typewrite_result):
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
                if not User.objects.filter(email=request.POST['email']):
                    user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
                    advanced_user = AdvancedUser(user_id=user.id)
                    advanced_user.save()
                    auth.login(request, user)
                else:
                    raise Exception
            except IntegrityError:
                flash_data = 'failedSignup'
            except Exception:
                flash_data = 'failedSignup'
            else:
                flash_data = 'successSignup'
        else:
            flash_data = 'notMatchPassword'

        if request.user.is_authenticated:
            profile_form = EditProfile(instance=AdvancedUser.objects.get(user_id=auth.get_user(request).id))
            return render(request, 'www/index.html',
                          {'profile_form': profile_form, 'edit_password_form': EditPassword(), 'maxim': Maxim.objects, 'typewrite': typewrite_result, 'flash_data': flash_data})
        return render(request, 'www/index.html', {'reset_password_form': ResetPassword(), 'maxim': Maxim.objects, 'typewrite': typewrite_result, 'flash_data': flash_data})

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
            password = User.objects.make_random_password(length=12)
            user.set_password(password)
            user.save()
            mailing = EmailThread('KNUT X LIKE LION 임시 비밀번호 발급', '', 'KNUT X LIKE LION', [request.POST['email']], False,
                                  '<div dir="ltr"><p>KNUT X LIKE LION으로부터 임시 비밀번호가 발급되었습니다. 로그인 후 비밀번호를 변경하시기 바랍니다.</p><p>임시 비밀번호 : ' + password + '</p><div dir="ltr" class="gmail_signature" data-smartmail="gmail_signature"><div dir="ltr"><div><div dir="ltr"><div dir="ltr"><div dir="ltr"><div><b><br></b></div><div><b>HACK YOUR LIFE</b></div><div>멋쟁이 사자처럼 at 한국교통대학교 <b>KNUT X LIKE LION</b></div><div><a href="http://knut.likelion.org" target="_blank">http://knut.likelion.org</a></div><div><a href="https://facebook.com/likelionKNUT" target="_blank">https://facebook.com/likelionKNUT</a></div><div><a href="https://likelion.net" target="_blank">https://likelion.net</a></div></div></div></div></div></div></div></div>')
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
