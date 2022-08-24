from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category
from .forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    http_method_names = ['get']
    context_object_name = 'news'
    paginate_by = 10
    paginate_orphans = 4
    # ordering = ['-create_at']
    # extra_context = {'title': 'Список новостей'}

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


class AddNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    http_method_names = ['get', 'post']
    login_url = reverse_lazy('home')


# def index(request):
#     news = News.objects.order_by('-create_at')
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context=context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'title': 'Список новостей по категории: {}'.format(category.title),
#         'news': news,
#         'one_category': category
#     }
#     return render(request, 'news/category.html', context=context)


# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     context = {
#         'news_item': news_item
#     }
#     return render(request, 'news/views_news.html', context=context)


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', context={'form': form})
