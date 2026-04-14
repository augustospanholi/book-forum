from django.contrib import admin
from core.models import Post, Reply, Rules


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'published']
    list_filter = ['category', 'published', 'author']
    search_fields = ['title', 'content']


admin.site.register(Post, PostAdmin)
admin.site.register(Reply)
admin.site.register(Rules)
