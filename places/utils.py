import decimal
import math

# The radius of the Earth in miles.
EARTH_RADIUS = decimal.Decimal('3963.1676')

# Number of miles in 1 degree of latitude.
LATITUDE_MILES = decimal.Decimal('69.172')

def longitude_to_miles(lat):
    """
    Returns the number of miles in 1 degree longitude at the specified
    latitude (given in degrees).
    """
    miles = math.radians(1) * math.cos(math.radians(lat)) * float(EARTH_RADIUS)
    return decimal.Decimal(str(miles))

def get_lat_long_ranges(start_lat, start_long, radius):
    """
    For the given latitude and longitude, and a radius (given in miles),
    returns a tuple of ranges suitable for using with Django's __range
    lookup, for instance:
        lat_range, long_range = get_lat_long_ranges(lat, long, 5)
        Place.objects.filter(latitude__range=lat_range, longitude__range=long_range)
    """
    start_lat = decimal.Decimal(str(start_lat))
    start_long = decimal.Decimal(str(start_long))
    radius = decimal.Decimal(str(radius))
    long_miles = longitude_to_miles(start_lat)
    lat_min = start_lat - (radius / LATITUDE_MILES)
    lat_max = start_lat + (radius / LATITUDE_MILES)
    long_min = start_long - (radius / long_miles)
    long_max = start_long + (radius / long_miles)
    return ((lat_min, lat_max), (long_min, long_max))

def distance(start_lat, start_long, end_lat, end_long):
    """
    Computes the distance between two latitude/longitude pairs, taking
    into account the curvature of the Earth.
    """
    a1 = math.radians(start_lat)
    b1 = math.radians(start_long)
    a2 = math.radians(end_lat)
    b2 = math.radians(end_long)
    x1 = math.cos(a1) * math.cos(b1) * math.cos(a2) * math.cos(b2)
    x2 = math.cos(a1) * math.sin(b1) * math.cos(a2) * math.sin(b2)
    x3 = math.sin(a1) * math.sin(a2)
    miles = math.acos(x1 + x2 + x3) * float(EARTH_RADIUS)
    return decimal.Decimal(str(miles))
