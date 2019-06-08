from django import forms
from .models import AdvancedUser, Portfolio, Notice
from django_summernote import fields as summer_fields


class EditPassword(forms.Form):
    current_password = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "현재 비밀번호"}))
    password = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "새 비밀번호"}))
    password_verify = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "새 비밀번호 확인"}))


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
            'picture': '프로필 사진 (1:1 비율)',
            'background': '배경 사진',
            'link1': '',
            'link2': '',
            'link3': '',
        }


class NoticeForm(forms.ModelForm):
    content = summer_fields.SummernoteTextFormField(error_messages={'required': '데이터를 입력해주세요', })

    class Meta:
        model = Notice
        fields = ['title', 'summary', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "제목"}),
            'summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "요약"}),
            # 'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "내용"}),
            # 'content': SummernoteInplaceWidget(attrs={'class': 'form-control', 'placeholder': "내용"}),
            # 'file': forms.FileInput(),
        }
        labels = {
            'title': '',
            'summary': '',
            'content': '',
            'file': '',
        }


class NewPortfolio(forms.ModelForm):
    content = summer_fields.SummernoteTextFormField(error_messages={'required': (u'데이터를 입력해주세요'), })

    class Meta:
        model = Portfolio
        fields = ['title', 'summary', 'content', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "제목"}),
            'summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "요약"}),
            # 'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "내용"}),
            # 'content': SummernoteInplaceWidget(attrs={'class': 'form-control', 'placeholder': "내용"}),
            'file': forms.FileInput(),
        }
        labels = {
            'title': '',
            'summary': '',
            'content': '',
            'file': '',
        }


class ResetPassword(forms.Form):
    email = forms.CharField(required=True)
    widgets = {
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "메일 주소"}),
    }
    labels = {
        'email': '',
    }
