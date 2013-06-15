from django.core.management.base import BaseCommand, CommandError

def should_discard(word):
    if not word or word == 'CDP':
        return True
    # Uppercased words and numbers
    if word[0].isupper() or word.isdigit():
        return False
    # Apostrophes in lowercased proper nouns, e.g. d'Alene
    if word[1] == "'" and word[2].isupper():
        return False
    # Aliases, e.g. Fredonia (Biscoe)
    if word[0] == '(' and word[1].isupper():
        return False
    return True

class Command (BaseCommand):
    help = 'Loads place entries from the specified file.'
    args = '<place_file>'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('You must specify a place file to load.')
        from django.db import models
        places = models.get_app('places')
        model = places.Place
        with open(args[0], 'rb') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) != 10 or len(parts[0]) != 2:
                    continue
                name = unicode(parts[3], 'iso-8859-1').replace('"', '').strip()
                words = name.split()
                while words and should_discard(words[-1]):
                    words.pop()
                model.objects.create(state=parts[0], name=u' '.join(words),
                    land_area=parts[4], water_area=parts[5],
                    latitude=parts[8], longitude=parts[9],
                    geo_id=parts[1], ansi_code=parts[2])
