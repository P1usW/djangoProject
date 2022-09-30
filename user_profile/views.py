from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetConfirmView, LogoutView, PasswordResetView, LoginView,\
    PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, FormView
from .forms import RecoverPasswordForm, RecoverSetPasswordForm, UserRegisterForm, UserAuthForms,\
    RecoverUserProfileForm, RecoverUserPasswordForm
from .utils import SuccessAndErrorMessageMixin


class Register(SuccessAndErrorMessageMixin, CreateView):
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
        return User.objects.filter(pk=self.kwargs['pk']).annotate(news__count=Count('news_author'))


class RecoverPasswordRequest(SuccessAndErrorMessageMixin, PasswordResetView):
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


class RecoverPassword(SuccessAndErrorMessageMixin, PasswordResetConfirmView):
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


class RecoverUserProfile(SuccessAndErrorMessageMixin, LoginRequiredMixin, FormView):
    form_class = RecoverUserProfileForm
    template_name = 'user_profile/recover_user_profile.html'
    login_url = reverse_lazy('home')
    success_message = 'Данные успешно изменены!'
    error_message = 'Произошла ошибка, попробуйте ещё раз!'

    def get_initial(self):
        initial = super().get_initial()
        initial.update({'username': self.request.user.username,
                        'first_name': self.request.user.first_name,
                        'last_name': self.request.user.last_name,
                        'email': self.request.user.email,
                        })
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})


# class RecoverUserProfile(LoginRequiredMixin, SuccessAndErrorMessageMixin, UpdateView):
#     model = User
#     form_class = RecoverUserProfileForm
#     template_name = 'user_profile/recover_user_profile.html'
#     login_url = reverse_lazy('home')
#     success_message = 'Данные успешно изменены!'
#     error_message = 'Произошла ошибка, попробуйте ещё раз!'
#
#     def get_initial(self):
#         initial = super().get_initial()
#         initial.update({'username': self.request.user.username,
#                         'first_name': self.request.user.first_name,
#                         'last_name': self.request.user.last_name,
#                         'email': self.request.user.email,
#                         })
#         return initial
#
#     def get_success_url(self):
#         return reverse('profile', kwargs={'pk': self.request.user.pk})
#
#     def get_object(self, queryset=None):
#         if queryset is None:
#             queryset = self.get_queryset()
#         queryset = queryset.filter(pk=self.request.user.pk)
#         obj = queryset.get()
#         return obj


class RecoverUserPassword(LoginRequiredMixin, SuccessAndErrorMessageMixin, PasswordChangeView):
    form_class = RecoverUserPasswordForm
    template_name = 'user_profile/recover_user_password.html'
    login_url = reverse_lazy('home')
    success_message = 'Данные успешно изменены!'
    error_message = 'Произошла ошибка, попробуйте ещё раз!'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})


class UserLogin(SuccessAndErrorMessageMixin, LoginView):
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
