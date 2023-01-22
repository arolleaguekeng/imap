from django.db import models


# Create your models here.

class Batiment(models.Model):
    numero = models.CharField(max_length=5, primary_key=True)
    longr = models.FloatField()
    largr = models.FloatField()


class CheckPoint(models.Model):
    id_batiment = models.IntegerField()
    id_etage = models.IntegerField()
    image = models.CharField(max_length=255)


class Etage(models.Model):
    numero = models.IntegerField(primary_key=True)
    id_batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, primary_key=True)


class Salle(models.Model):
    numero = models.CharField(max_length=50)
    id_batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE)
    numero_etage = models.ForeignKey(Etage, on_delete=models.CASCADE)


class Cable(models.model):
    id_cp_origine = models.ForeignKey(CheckPoint, on_delete=models.CASCADE)
    id_cp_destination = models.ForeignKey(CheckPoint, on_delete=models.CASCADE)
    longr = models.FloatField()
    direction = models.CharField(max_length=10)
