import datetime

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)


class Card(models.Model):
    date = models.DateField(default=datetime.datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Task(models.Model):
    name = models.TextField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    noted = models.BooleanField(default=False)

