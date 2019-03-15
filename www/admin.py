from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django_summernote.admin import SummernoteModelAdmin
from .models import *

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


class NoticeAdmin(SummernoteModelAdmin):
    search_fields = ['content', 'summary']
    list_filter = ['author', 'date_created']
    date_hierarchy = 'date_created'
    ordering = ['date_created']
    # fieldsets = [
    #     ('개요', {'fields': ['title', 'summary']}),
    #     ('내용', {'fields': ['content', 'file']}),
    # ]
    fields = ['title', 'summary', 'date_created', 'content', 'file']
    list_display = ('title', 'summary', 'author', 'date_created')


class PortfolioAdmin(SummernoteModelAdmin):
    search_fields = ['content', 'summary']


admin.site.register(Maxim)
admin.site.register(TypeWrite)
admin.site.register(Member)
admin.site.register(Notice, NoticeAdmin)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Faq)
admin.site.register(FaqTag)
admin.site.register(PortfolioTag)
admin.site.register(Portfolio, PortfolioAdmin)
