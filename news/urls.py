from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', views.NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', views.ViewNews.as_view(), name='view_news'),
    path('news/add_news', views.AddNews.as_view(), name='add_news'),
    path('support', views.SendMail.as_view(), name='support')
]

