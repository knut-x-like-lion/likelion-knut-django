from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User


# Create your models here.


class AdvancedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, null=True, blank=True)
    picture = models.ImageField(upload_to='www/images/profile', null=True, blank=True)
    background = models.ImageField(upload_to='www/images/profile', null=True, blank=True)
    message = models.CharField(max_length=20, null=True, blank=True)
    link1 = models.URLField(max_length=200, null=True, blank=True)
    link2 = models.URLField(max_length=200, null=True, blank=True)
    link3 = models.URLField(max_length=200, null=True, blank=True)


class Member(models.Model):
    class Meta:
        verbose_name = '멤버'
        verbose_name_plural = '멤버'
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return self.email


class Maxim(models.Model):
    class Meta:
        verbose_name = '격언'
        verbose_name_plural = '격언'

    content = models.CharField(max_length=500, blank=False)
    by_who = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return '' + self.id.__str__() + ': ' + self.by_who


class TypeWrite(models.Model):
    class Meta:
        verbose_name = '움직이는 글자'
        verbose_name_plural = '움직이는 글자'

    content = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.content


class Post(models.Model):
    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'

    title = models.CharField(max_length=30, null=False, blank=False, verbose_name='제목')
    summary = models.CharField(max_length=50, null=True, blank=True, verbose_name='요약')
    author = models.CharField(max_length=20, null=False, blank=False, default='운영진', verbose_name='작성자')
    date_created = models.DateField(auto_now_add=True, verbose_name='작성일')
    content = models.TextField(max_length=5000, null=True, blank=False, verbose_name='내용')
    html_render = models.BooleanField('HTML 렌더링 (non-safe)')
    image = models.ImageField(upload_to='www/images', null=True, blank=True)
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(320, 100)], format='JPEG', options={'quality': 90})

    def __str__(self):
        return self.title


class Portfolio(models.Model):
    class Meta:
        verbose_name = '포트폴리오'
        verbose_name_plural = '포트폴리오'
    title = models.CharField(max_length=30, null=False, blank=False)
    content = models.CharField(max_length=50, null=True, blank=True)
    tags = models.CharField(max_length=50, null=True, blank=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='www/portfolio/thumbnail', null=True, blank=True)
    link1 = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class Tags(models.Model):
    class Meta:
        verbose_name = '포트폴리오 태그'
        verbose_name_plural = '포트폴리오 태그'
    label = models.CharField(max_length=30, null=False, blank=False)
    tag_name = models.CharField(max_length=15, null=True, blank=True)
