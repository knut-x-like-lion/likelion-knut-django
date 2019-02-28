from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('root/', admin.site.urls),
    path('', include('www.urls'), name='index'),
]
