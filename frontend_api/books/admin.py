from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

class User(models.Model):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)