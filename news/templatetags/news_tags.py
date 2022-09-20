from django import template
from django.db.models import Count, F
from news.models import Category
# from django.core.cache import cache

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    # categories = cache.get('categories')
    # if not categories:
    #     categories = Category.objects.annotate(news_count = Count('news'), filter=F('news__is_published'))
    #     cache.set('categories', categories, 30)

    categories = Category.objects.annotate(news_count=Count('news'), filter=F('news__is_published'))

    return {
        'categories': categories,
    }
