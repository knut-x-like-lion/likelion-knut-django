from django.urls import path
from www import views

app_name = 'www'
urlpatterns = [
    path('', views.index, name='index'),
]
