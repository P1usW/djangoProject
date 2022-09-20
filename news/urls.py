from django.urls import path
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
    path('', views.HomeNews.as_view(), name='home'),
    # path('category/<int:category_id>/', cache_page(60)(views.NewsByCategory.as_view()), name='category'),
    path('category/<int:category_id>/', views.NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', views.ViewNews.as_view(), name='view_news'),
    path('news/add_news', views.AddNews.as_view(), name='add_news'),
    path('support/', views.SendMail.as_view(), name='support'),
    path('search/', views.Search.as_view(), name='search')
]

