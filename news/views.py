from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from .models import News, Category
from .forms import NewsForm, SendMailForm
from .utils import ErrorMessageMixin


class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    http_method_names = ['get']
    context_object_name = 'news'
    paginate_by = 10
    paginate_orphans = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список новостей'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).order_by('-create_at').select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/index.html'
    http_method_names = ['get']
    context_object_name = 'news'
    paginate_by = 10
    paginate_orphans = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        one_category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        context['title'] = 'Список новостей по категории {}'.format(one_category)
        return context

    def get_queryset(self):
        return News.objects.filter(
            is_published=True, category_id=self.kwargs['category_id']).order_by('-create_at').select_related('category')


class ViewNews(DetailView):
    model = News
    template_name = 'news/views_news.html'
    context_object_name = 'news_item'
    http_method_names = ['get']

    def get_queryset(self):
        return News.objects.filter(pk=self.kwargs['pk']).select_related('author').select_related('category')


class AddNews(LoginRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    http_method_names = ['get', 'post']
    login_url = reverse_lazy('home')
    success_message = 'Новость успешно опубликована!'
    error_message = 'Произошла ошибка, повторите снова!'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(AddNews, self).form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial.update({'author': self.request.user})
        return initial


class SendMail(FormView):
    form_class = SendMailForm
    template_name = 'news/send_mail_support.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        message_body = form.cleaned_data['body']
        rendered = render_to_string('news/support_message.html',
                                    context={'body': message_body,
                                             'username': self.request.user.username
                                             }
                                    )
        send_mail(subject='Сообщение поддержки',
                  message=''.format(message_body),
                  from_email=None,
                  recipient_list=['ivshavrin@gmail.com'],
                  html_message=rendered
                  )
        return super().form_valid(form)
