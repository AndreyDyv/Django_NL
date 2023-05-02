from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=100, verbose_name='Датчик')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.FloatField(verbose_name='Температура датчика')
    created_at = models.DateTimeField(verbose_name='Время измерения')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return str(self.temperature)
