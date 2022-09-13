from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetConfirmView, LogoutView, PasswordResetView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from .forms import RecoverPasswordForm, RecoverSetPasswordForm, UserRegisterForm, UserAuthForms
from .utils import ErrorMessageMixin


class Register(SuccessMessageMixin, ErrorMessageMixin, CreateView):
    template_name = 'user_profile/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    success_message = 'Вы успешно зарегестрировались!'
    error_message = 'Произошла ошибка, повторите снова!'
    http_method_names = ['get', 'post']

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class Profile(DetailView):
    template_name = 'user_profile/profile.html'
    context_object_name = 'user_profile'

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk']).annotate(Count('news'))


class RecoverPasswordRequest(SuccessMessageMixin, ErrorMessageMixin, PasswordResetView):
    template_name = 'user_profile/recover_password_request.html'
    form_class = RecoverPasswordForm
    email_template_name = 'user_profile/telo.html'
    subject_template_name = 'user_profile/tema.html'
    html_email_template_name = 'user_profile/password_message.html'
    success_url = reverse_lazy('password_reset')
    success_message = 'Письмо отправлено на почту!'
    error_message = 'Произошла ошибка, попробуйте ещё раз!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Смена пароля'
        return context


class RecoverPassword(SuccessMessageMixin, ErrorMessageMixin, PasswordResetConfirmView):
    template_name = 'user_profile/recover_password.html'
    post_reset_login = True
    form_class = RecoverSetPasswordForm
    success_url = reverse_lazy('home')
    success_message = 'Ваш пароль сменён!'
    error_message = 'Произошла ошибка, попробуйте ещё раз!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Смена пароля'
        return context


class UserLogin(SuccessMessageMixin, ErrorMessageMixin, LoginView):
    template_name = 'user_profile/login.html'
    redirect_authenticated_user = True
    authentication_form = UserAuthForms
    next_page = reverse_lazy('home')
    success_message = 'Вы успешно вошли в систему'
    error_message = 'Произошла ошибка, попробуйте ещё раз!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context


class UserLogout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login')
    login_url = reverse_lazy('home')
