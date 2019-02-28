from django.db import models

# Create your models here.


class Maxim(models.Model):
    content = models.CharField(max_length=500, blank=False)
    by_who = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return '' + self.id.__str__() + ': ' + self.by_who


class TypeWrite(models.Model):
    content = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.content


class Post(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False)
    summary = models.CharField(max_length=50, null=True, blank=True)
    author = models.CharField(max_length=20, null=False, blank=False, default='운영진')
    date_created = models.DateField(null=False, auto_now=True)
    content = models.TextField(max_length=1024, null=True, blank=False)
    html_render = models.BooleanField('HTML 렌더링 (non-safe)')
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

