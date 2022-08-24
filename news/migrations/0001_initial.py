# Generated by Django 4.0.6 on 2022-08-03 08:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('body', models.TextField(blank=True, max_length=1024)),
                ('create_at', models.DateTimeField(default=datetime.datetime(2022, 8, 3, 8, 5, 40, 501180, tzinfo=utc))),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(upload_to='photo_news/%Y/%m/%d/')),
                ('is_published', models.BooleanField(default=True)),
            ],
        ),
    ]