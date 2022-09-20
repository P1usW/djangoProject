from django import forms
from .models import News
import re
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField


class NewsForm(forms.ModelForm):
    """Если использовать этот класс, то в файле view нужно использовать не
    news = News.objects.create(**form.cleaned_data), а news = form.save()
    """

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выбрать категорию'

    class Meta:
        model = News
        exclude = ['create_at', 'update_at']
        labels = {
            'title': 'Заголовок',
            'body': 'Текст статьи',
            'photo': 'Фото',
            'is_published': 'Опубликовать',
            'category': 'Выбрать категорию',
            'author': 'Автор статьи'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'title': 'Максимальная длина 64 символа',
            'body': 'Максимальная длина 1024 символа'
        }

    # Кастомынй валидатор
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начнаться с цифры')
        return title


class SendMailForm(forms.Form):
    body = forms.CharField(max_length=1024,
                           label='Сообщение',
                           help_text='Максимальная длина 1024 символа',
                           widget=forms.Textarea(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='Каптча')
