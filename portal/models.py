from django.db import models

# Create your models here.

class Usuari(models.Model):
    nom = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    data_naixement = models.IntegerField()
    nascut_a = models.CharField(max_length=100)
    resideix_a = models.CharField(max_length=100)
    registrat = models.DateTimeField(auto_now_add=True)

class Registre(models.Model):
    ip = models.CharField(max_lenght=20, primary_key=True)
    registrat = models.DateTimeField(auto_now_add=True)
