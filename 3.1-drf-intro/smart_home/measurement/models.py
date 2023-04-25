from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)
class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    pass


class Measurement(models.Model):
    temperature = models.FloatField()
    created_at = models.DateTimeField()
    pass

