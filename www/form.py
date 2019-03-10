from django import forms
from .models import AdvancedUser


class BlogPost(forms.ModelForm):
    class Meta:
        # model = Blog
        fields = ['title', 'body']


class EditPassword(forms.Form):
    current_password = forms.CharField(required=True)
    password = forms.CharField(required=True)
    password_verify = forms.CharField(required=True)
    widgets = {
        'current_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "현재 비밀번호"}),
        'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "비밀번호 변경"}),
        'password_verify': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "비밀번호 확인"}, ),
    }
    labels = {
        'current_password': '',
        'password': '',
        'password_verify': '',
    }


class EditProfile(forms.ModelForm):
    class Meta:
        model = AdvancedUser
        fields = ['nickname', 'message', 'picture', 'background', 'link1', 'link2', 'link3']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "닉네임"}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "상태 메시지"}),
            'picture': forms.FileInput(),
            'background': forms.FileInput(),
            'link1': forms.URLInput(attrs={'class': 'form-control', 'placeholder': "블로그 링크"}),
            'link2': forms.URLInput(attrs={'class': 'form-control', 'placeholder': "Facebook 링크"}),
            'link3': forms.URLInput(attrs={'class': 'form-control', 'placeholder': "GitHub 링크"}),
        }
        labels = {
            'nickname': '',
            'message': '',
            'picture': '프로필 사진',
            'background': '배경 사진',
            'link1': '',
            'link2': '',
            'link3': '',
        }


class ResetPassword(forms.Form):
    email = forms.CharField(required=True)
    widgets = {
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "메일 주소"}),
    }
    labels = {
        'email': '',
    }
