from django import forms
# from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, \
    PasswordChangeForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Почта', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text='')
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='Каптча')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus')
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'captcha']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserAuthForms(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}),
                               help_text='')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               help_text='')

    def __init__(self, *args, **kwargs):
        super(UserAuthForms, self).__init__(*args, **kwargs)


class RecoverPasswordForm(PasswordResetForm):
    email = forms.CharField(label='Почта', max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Такая почта не зарегестрирована.'.format(email))
        return email


class RecoverSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Повторите пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# class RecoverUserProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name')
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#
#     def save(self, commit=True):
#         user = super(RecoverUserProfileForm, self).save(commit=True)
#         user.username = self.cleaned_data['username']
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         if commit:
#             user.save()
#         return user


class RecoverUserProfileForm(forms.Form):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Почта', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        if commit:
            self.user.save()
        return self.user

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.initial['username'] == username:
            return username
        try:
            account = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Логин "{}" уже используется.'.format(username))

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.initial['email'] == email:
            return email
        try:
            account = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Почта "{}" уже используется.'.format(email))


class RecoverUserPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Новый пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Повторите пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
