from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f' {self.id}'



class University(models.Model):
    rank = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=150, null=False, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    score = models.CharField(max_length=20, null=False)

    def __str__(self):
        return f'rank:{self.rank}, name:{self.name}, country:{self.country}'