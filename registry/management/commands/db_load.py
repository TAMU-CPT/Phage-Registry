from django.db import transaction
from registry.models import RegistryEntry, DatabaseSource
from django.contrib.auth.models import User
import json
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Loads data into DB from specially formatted files'

    def add_arguments(self, parser):
        parser.add_argument('file', type=file)
        parser.add_argument('user', type=str, help='Username')
        parser.add_argument('database', type=str, help='Linked Database')

    @transaction.atomic
    def _proc(self, data, db, user):
        i = 0
        for row in data:
            try:
                x = RegistryEntry.objects.get(
                    phagename=row[1]
                )
            except RegistryEntry.DoesNotExist:
                re = RegistryEntry(
                    owner=user,
                    phagename=row[1],
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
            results = self._proc(data, db, user)
            self.stdout.write(self.style.SUCCESS("Successfully loaded %s objects" % results))
        except Exception, e:
            raise CommandError(e)
