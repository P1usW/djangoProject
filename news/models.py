from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=64)
    body = models.TextField(max_length=1024, blank=True)
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photo_news/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def get_absolute_url(self):
        """Выбрав такое имя метода, мы так же добавляем ссылку в адимнке"""
        return reverse('view_news', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Category(models.Model):
    title = models.CharField(max_length=64, db_index=True, unique=True)

    def get_absolute_url(self):
        """Выбрав такое имя метода, мы так же добавляем ссылку в адимнке"""
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
