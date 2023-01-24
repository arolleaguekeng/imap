from django.db import models


# Create your models here.

class Batiment(models.Model):
    numero = models.CharField(max_length=5, primary_key=True)
    longr = models.FloatField()
    largr = models.FloatField()


class Etage(models.Model):
    numero = models.CharField(max_length=4, primary_key=True)
    id_batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE,)


class CheckPoint(models.Model):
    id_checkpoint = models.CharField(max_length=10, primary_key=True)
    id_batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE)
    id_etage = models.ForeignKey(Etage, on_delete=models.CASCADE)
    image = models.CharField(max_length=255)





class Salle(models.Model):
    numero = models.CharField(max_length=50, primary_key=True)
    id_batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE)
    numero_etage = models.ForeignKey(Etage, on_delete=models.CASCADE)


class Cable(models.Model):
    id_cp_origine = models.ForeignKey(CheckPoint, on_delete=models.CASCADE, related_name='id_cp_origine', null=True)
    id_cp_destination = models.ForeignKey(CheckPoint, on_delete=models.CASCADE, related_name='id_cp_destination')
    longr = models.FloatField()
    direction_origine = models.CharField(max_length=2)


