from django.db import models
from utils import get_lat_long_ranges, distance

class PlaceManager (models.Manager):

    def nearby(self, lat, lon, radius):
        """
        Returns a queryset of places approximately within the given
        bounding radius of the given latitude and longitude. Some places
        may be further than the specified radius, since a bounding box
        is used instead of a bounding sphere for simplicity and speed.
        The bounding box calculation may also be slightly off for large
        radius values, since the number of miles in a degree of longitude
        varies by latitude, but is only calculated once for the given
        latitude and longitude. All that said, it should be "close enough",
        and if you needed more precision, you probably wouldn't be using
        this package to begin with.
        """
        lat_range, long_range = get_lat_long_ranges(lat, lon, radius)
        return self.filter(latitude__range=lat_range, longitude__range=long_range)

    def closest(self, lat, lon, radius=100, start_radius=5):
        """
        Returns the closest place to the given latitude and longitude, within
        the given radius. This method is not very efficient, as it loops over
        nearby places, calculating the distance to each. In order to keep the
        number of calculations down, it starts with places in a small radius,
        and only expands the search if none are found.
        """
        if start_radius > radius:
            return None, None
        places = list(self.nearby(lat, lon, start_radius))
        if not places:
            return self.closest(lat, lon, radius, start_radius*2)
        min_distance = radius
        closest_place = None
        for place in places:
            d = distance(lat, lon, place.latitude, place.longitude)
            if d < min_distance:
                min_distance = d
                closest_place = place
        return closest_place, min_distance
