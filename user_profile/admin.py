from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class PofileAdmin(admin.ModelAdmin):
    search_fields = ('facebook',
                     'twitter',
                     'instagram',
                     )
