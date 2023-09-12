from django.contrib import admin
from .models import Post, Comment
# Register your models here.

# ----- post added to admin panel -------


@admin.register(Post)  # = admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'published', 'status']
    list_filter = ['author', 'created', 'published', 'status']
    search_fields = ['title', 'body']
    # when write title make slug automatically as title first-post
    prepopulated_fields = {'slug': ('title',)}
    # add users by id = 1 instead of dropdown for thousands of users
    raw_id_fields = ['author']
    date_hierarchy = 'published'
    ordering = ['status', 'published']

# ----- comment added to admin panel -------


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
