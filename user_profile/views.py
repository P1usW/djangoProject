from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserAuthForms
from django.contrib import messages
from django.contrib.auth import login
from .forms import RecoverPasswordForm, RecoverSetPasswordForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView, LogoutView


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрировались!')
            return redirect('home')
        else:
            messages.error(request, 'Произошла ошибка, повторите снова!')
    else:
        form = UserRegisterForm()
    return render(request, template_name='user_profile/register.html', context={'form': form})


def recover_password_request(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RecoverPasswordForm(request.POST)
        if form.is_valid():
            for all_user in form.get_users(form.cleaned_data['email']):
                user = all_user
            form.save(subject_template_name='user_profile/tema.html',
                      email_template_name='user_profile/telo.html',
                      request=request,
                      html_email_template_name='user_profile/password_message.html',
                      )
            messages.success(request ,'Письмо отправлено, проверьте почту')
        else:
            messages.error(request, 'Произошла ошибка, повторите снова!')
    else:
        form = RecoverPasswordForm()
    return render(request, template_name='user_profile/recover_password_request.html', context={'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserAuthForms(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Произошла ошибка, повторите снова!')
    else:
        form = UserAuthForms()
    return render(request, template_name='user_profile/login.html', context={'form': form})


class RecoverPassword(PasswordResetConfirmView):
    template_name = 'user_profile/recover_password.html'
    post_reset_login = True
    form_class = RecoverSetPasswordForm
    success_url = reverse_lazy('home')


class UserLogout(LogoutView):
    next_page = reverse_lazy('login')

