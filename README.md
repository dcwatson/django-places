django-places
=============

A django model for US census place information.
To populate the database, download the places file from:

http://www.census.gov/geo/maps-data/data/gazetteer2010.html

Then run the following command:

./manage.py loadplaces <places_file>

Finding Places
==============

Place.objects.nearby(lat, lon, radius)
	Returns a queryset of Places within the given radius of lat/lon.

Place.objects.closest(lat, lon, radius)
	Returns the closest Place and the distance to the lat/lon, within
	the given radius.

Place.distance_to(place)
Place.distance_to(lat, lon)
	Returns the distance in miles between a Place and another Place
	or lat/lon coordinates.

PlaceManager
============

You can use the PlaceManager in places.managers with any model that has
decimal fields named "longitude" and "latitude".
