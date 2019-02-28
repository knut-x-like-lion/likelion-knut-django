from django.contrib import admin
from .models import *

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('공지사항 리스트', {'fields': ['title', 'author', 'summary']}),
        ('공지 내용', {'fields': ['content', 'html_render', 'image']}),
    ]

    list_display = ('title', 'summary', 'author', 'date_created')


admin.site.register(Maxim)
admin.site.register(TypeWrite)
admin.site.register(Post, PostAdmin)
