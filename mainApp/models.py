from django.core.validators import MinValueValidator
from django.db import models


class Dori(models.Model):
    nom = models.CharField(max_length=255)
    ishlab_chiqaruvchi = models.CharField(max_length=255)
    turi = models.CharField(max_length=255)
    narx = models.FloatField(validators=[MinValueValidator(0)])
    miqdor = models.IntegerField(validators=[MinValueValidator(0)])
    kelgan_sana = models.DateField(auto_now_add=True)
    muddat = models.DateField()

    def __str__(self):
        return self.nom


class Sotuv(models.Model):
    dori = models.ForeignKey(Dori, on_delete=models.CASCADE)
    miqdor = models.IntegerField(validators=[MinValueValidator(0)])
    summa = models.FloatField(validators=[MinValueValidator(0)])
    sana = models.DateField(auto_now_add=True)

