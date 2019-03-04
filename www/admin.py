from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from www.models import AdvancedUser
from .models import Post, Maxim, TypeWrite

# Register your models here.


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class AdvancedUserInline(admin.StackedInline):
    model = AdvancedUser
    verbose_name = '프로필'
    verbose_name_plural = '프로필'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (AdvancedUserInline,)


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('공지사항 리스트', {'fields': ['title', 'author', 'summary']}),
        ('공지 내용', {'fields': ['content', 'html_render', 'image']}),
    ]

    list_display = ('title', 'summary', 'author', 'date_created')


admin.site.register(Maxim)
admin.site.register(TypeWrite)
admin.site.register(Post, PostAdmin)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
