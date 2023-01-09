from django.core.management.base import BaseCommand, CommandError

from filter_page.models import App
from filter_page.utils import ParcerApps


class Command(BaseCommand):
    def handle(self, *args, **options):
        parser = ParcerApps.run()
        bulk_objects = []
        for company in parser.get_date():
            bulk_objects.append(
                App(name_app=company['title'],
                   company=company['company'],
                   email=company['email'],
                   release=company['release_year']))
        App.objects.bulk_create(bulk_objects, ignore_conflicts=True)
        print('Elem created')

