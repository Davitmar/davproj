from django.db import models
from django.contrib.auth.models import User



class Authors(models.Model):
    author = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f'{self.author}'


class Tags(models.Model):
    tag = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return f'{self.tag}'


class Quotas(models.Model):
    quota = models.TextField(null=False)
    author = models.ForeignKey(Authors, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tags)
    fav = models.ManyToManyField(User, related_name='favor', blank=True)
    picture = models.ImageField(upload_to='media', blank=True, null=True)
    download = models.FileField(upload_to='media', blank=True, null=True)
    date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f'{self.quota}'


class Messege(models.Model):
    messege = models.TextField(null=True,  blank=True)
    nkar = models.ImageField(upload_to='media', blank=True, null=True)
    sender = models.ForeignKey(User, related_name='send', on_delete=models.SET_NULL, null=True)
    reciever = models.ForeignKey(User, related_name='reciev', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f'{self.messege}'

class UsersPhotos(models.Model):
    comment = models.CharField(max_length=50)
    is_main = models.BooleanField(default=False)
    image = models.ImageField(upload_to='media', blank=False)
    date = models.DateTimeField(auto_now=True, blank=True)
    user_photo=models.ForeignKey(User, blank=False, on_delete=models.CASCADE)

class Friends(models.Model):

    friend_sender = models.ForeignKey(User, related_name='f_s', on_delete=models.CASCADE, null=True)
    friend_reciever = models.ForeignKey(User, related_name='f_r', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now=True, blank=True)
    subscribe = models.BooleanField(default=False)