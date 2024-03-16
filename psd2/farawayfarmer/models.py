from django.db import models

# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=100)
    last_watered = models.DateField()
    water_level = models.IntegerField()
    floor_level = models.IntegerField()

    def __str__(self):
        return self.name