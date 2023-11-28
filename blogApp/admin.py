from django.contrib import admin

from blogApp.models import Post


# Register your models here.

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'date_posted')
    ordering = ['id']
