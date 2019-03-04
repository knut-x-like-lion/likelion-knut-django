from django import forms


class BlogPost(forms.ModelForm):
    class Meta:
        # model = Blog
        fields = ['title', 'body']


class BlogPost2(forms.Form):
    email = forms.EmailField()
    max_number = forms.ChoiceField(choices=[('1', 'one'), ('2', 'two')])


# class Signup(forms.Form):
#     name = forms.TextInput()
#     email = forms.EmailField(label='Email')
#     password = forms.PasswordInput()
#     passwordVerify = forms.PasswordInput()
#     signCode = forms.PasswordInput()
