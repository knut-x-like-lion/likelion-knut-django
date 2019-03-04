from django import forms
from .models import AdvancedUser


class BlogPost(forms.ModelForm):
    class Meta:
        # model = Blog
        fields = ['title', 'body']


class BlogPost2(forms.Form):
    email = forms.EmailField()
    max_number = forms.ChoiceField(choices=[('1', 'one'), ('2', 'two')])


class EditProfile(forms.ModelForm):
    class Meta:
        model = AdvancedUser
        fields = ['nickname', 'message', 'picture', 'link1', 'link2', 'link3']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "닉네임"}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "상태 메시지"}),
            # 'picture': forms.ImageField(attrs={'class': 'form-control'}),
            # 'link1': forms.URLField(attrs={'placeholder': "상태 메시지"}),
            # 'link2': forms.URLField(attrs={'placeholder': "상태 메시지"}),
            # 'link3': forms.URLField(attrs={'placeholder': "상태 메시지"}),
        }
        labels = {
            'nickname': '',
            'message': '',
            'picture': '프로필 사진',
            'link1': 'URL1',
            'link2': 'URL2',
            'link3': 'URL3',
        }
