from django.db import models

# Create your models here.


class Maxim(models.Model):
    content = models.CharField(max_length=500)
    by_who = models.CharField(max_length=50)

    def __str__(self):
        return '' + self.id.__str__() + ': ' + self.by_who


