from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_at'
    list_display = ('title', 'category', 'create_at', 'update_at', 'is_published', 'get_photo', 'author')
    list_display_links = ('title',)
    search_fields = ('title', 'body', 'author')
    list_editable = ('is_published',)
    list_filter = ('category', 'is_published')
    readonly_fields = ('create_at', 'update_at', 'get_photo')
    fieldsets = (
        (None, {
            'fields': ('title',
                       'body',
                       'category',
                       'author',
                       'is_published',
                       'create_at',
                       'update_at',
                       'photo',
                       'get_photo',),
        }),
    )

    @admin.display(description="Фотография")
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75"')
        else:
            return 'Нет фотографии'


@admin.register(models.Category)
class NewsAdmin(admin.ModelAdmin):
    search_fields = ('title',)


admin.AdminSite.site_header = 'Управление новостями'
admin.AdminSite.site_title = 'Управление Новостями'
