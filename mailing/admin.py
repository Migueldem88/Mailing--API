from django.contrib import admin

from .models import Article,Subscriber, Email


@admin.register(Article)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject','date','content','to')


admin.site.register(Subscriber)
#admin.site.register(Email)