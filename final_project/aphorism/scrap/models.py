from django.db import models
from django.contrib.auth.models import User

class Authors(models.Model):
    author=models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f'{self.author}'

class Tags(models.Model):
    tag=models.CharField(max_length=50, unique=True, null=False)


    def __str__(self):
        return f'{self.tag}'

class Quotas(models.Model):
    quota=models.TextField(null=False)
    author=models.ForeignKey(Authors, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tags)

    def __str__(self):
        return f'{self.quota}'

