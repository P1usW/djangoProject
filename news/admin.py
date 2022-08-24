from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_at'
    list_display = ('title', 'category', 'create_at', 'update_at', 'is_published', 'get_photo')
    list_display_links = ('title',)
    search_fields = ('title', 'body')
    list_editable = ('is_published',)
    list_filter = ('category', 'is_published')
    readonly_fields = ('create_at', 'update_at', 'get_photo')
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'category', 'is_published', 'create_at', 'update_at',  'photo', 'get_photo',),
        }),
    )

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75"')
        else:
            return 'Нет фотографии'

    get_photo.short_description = "Фотография"

@admin.register(models.Category)
class NewsAdmin(admin.ModelAdmin):
    search_fields = ('title',)


admin.AdminSite.site_header = 'Управление новостями'
admin.AdminSite.site_title = 'Управление Новостями'
