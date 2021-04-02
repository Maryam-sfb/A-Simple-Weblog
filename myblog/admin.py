from django.contrib import admin
from .models import Article, Category, IPAddress, ArticleHit


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'jpublish', 'status', 'category_to_str')
    list_filter = ('status', 'writer', 'publish_time')
    list_editable = ('status',)
    search_fields = ('title', 'body')
    raw_id_fields = ('writer',)
    prepopulated_fields = {'slug': ('title',)}

    def category_to_str(self, obj):
        return '، '.join([category.title for category in obj.category_published()])
    category_to_str.short_description = 'دسته بندی'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(IPAddress)
admin.site.register(ArticleHit)















