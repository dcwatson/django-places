from django.db import models
from django.contrib.localflavor.us.models import USStateField
from managers import PlaceManager
from utils import distance

class Place (models.Model):
    state = USStateField(db_index=True)
    name = models.CharField(max_length=200)
    land_area = models.PositiveIntegerField()
    water_area = models.PositiveIntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    geo_id = models.CharField(max_length=7)
    ansi_code = models.CharField(max_length=8)

    objects = PlaceManager()

    def __unicode__(self):
        return self.name

    def distance_to(self, *args):
        if len(args) == 2:
            lat, lon = args[0], args[1]
        else:
            lat, lon = args[0].latitude, args[0].longitude
        return distance(self.latitude, self.longitude, lat, lon)
