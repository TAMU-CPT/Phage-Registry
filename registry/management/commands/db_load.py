from django.db import transaction
from registry.models import RegistryEntry, DatabaseSource
from django.contrib.auth.models import User
import re
import json
from django.core.management.base import BaseCommand, CommandError

phage_in_middle = re.compile('^(?P<host>.*)\s*phage (?P<phage>.*)$')
bacteriophage_in_middle = re.compile('^(?P<host>.*)\s*bacteriophage (?P<phage>.*)$')
starts_with_phage = re.compile('^(bacterio|vibrio|Bacterio|Vibrio|)?[Pp]hage (?P<phage>.*)$')
new_style_names = re.compile('(?P<phage>v[A-Z]_[A-Z][a-z]{2}_.*)')

class Command(BaseCommand):
    help = 'Loads data into DB from specially formatted files'

    def add_arguments(self, parser):
        parser.add_argument('file', type=file)
        parser.add_argument('user', type=str, help='Username')
        parser.add_argument('database', type=str, help='Linked Database')
        parser.add_argument('--clean_name', action='store_true', help='Clean phage names')


    def name_parser(self, name):
        host = None
        phage = None
        name = name.replace(', complete genome', '')

        m = bacteriophage_in_middle.match(name)
        if m:
            host = m.group('host')
            phage = m.group('phage')
            return (host, phage)

        m = phage_in_middle.match(name)
        if m:
            host = m.group('host')
            phage = m.group('phage')
            return (host, phage)

        m = starts_with_phage.match(name)
        if m:
            phage = m.group('phage')
            return (host, phage)

        m = new_style_names.match(name)
        if m:
            phage = m.group('phage')
            return (host, phage)

        return (host, phage)

    @transaction.atomic
    def _proc(self, data, db, user, clean_name=False):
        i = 0
        for row in data:
            phage_name = row[1]
            if clean_name:
                (x, phage_name) = self.name_parser(phage_name)

            if phage_name is None:
                continue

            if len(phage_name) > 50:
                continue

            try:
                x = RegistryEntry.objects.get(
                    phagename=phage_name,
                )
            except RegistryEntry.DoesNotExist:
                re = RegistryEntry(
                    owner=user,
                    phagename=phage_name,
                    extid=row[0],
                    database=db,
                )
                re.save()
                i += 1
        return i

    def handle(self, *args, **options):
        data = json.load(options['file'])
        db = DatabaseSource.objects.get(name=options['database'])
        user = User.objects.get(username=options['user'])
        try:
            results = self._proc(data, db, user, clean_name=options['clean_name'])
            self.stdout.write(self.style.SUCCESS("Successfully loaded %s objects" % results))
        except Exception, e:
            raise CommandError(e)
