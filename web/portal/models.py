from django.db import models
from postgres_copy import CopyManager

# Create your models here.

class Usuari(models.Model):
    nom = models.CharField(max_length=100)
    cognom = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    edat = models.IntegerField()
    sexe = models.CharField(max_length=100)
    resideix_a = models.CharField(max_length=100)
    registrat = models.DateTimeField(auto_now_add=True)
    objects = CopyManager()


class Registre(models.Model):
    ip = models.CharField(max_length=20, primary_key=True)
    registrat = models.DateTimeField(auto_now_add=True)
