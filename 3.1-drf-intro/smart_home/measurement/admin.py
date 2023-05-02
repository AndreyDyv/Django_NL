from django.contrib import admin

from measurement.models import *

admin.site.register(Sensor)
admin.site.register(Measurement)
