import csv
import os

from django.core.management.base import BaseCommand
from kds_stroy import settings
from orders.models import Region, District, City, CityType

DEFAULT_PATH = str(settings.BASE_DIR) + '/data/'


class Command(BaseCommand):
    help = 'Command to load cities from csv files.'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--files', type=str, nargs='+',
                            help='File names to load in database.')

        parser.add_argument('-a', '--all', action='store_true',
                            help='Upload all files from the folder.')

        parser.add_argument('-l', '--log', action='store_true',
                            help='Show logs.')

        parser.add_argument('-p', '--path', type=str,
                            help='Input path to the folder with files.')

        parser.add_argument('-c', '--clear', action='store_true',
                            help='Clear all cities in the database.')

    def handle(self, *args, **options):
        log = True if options['log'] else False
        folder_path = options['path'] or DEFAULT_PATH

        if options['clear']:
            City.objects.all().delete()
            CityType.objects.all().delete()
            District.objects.all().delete()
            Region.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('All cities are deleted'))
            return

        if options['all']:
            files = os.listdir(folder_path)
        elif options['files']:
            files = options['files']
        else:
            self.stdout.write(self.style.ERROR(
                'Please, provide file names or '
                'use --all flag to load all files from the folder.'
            ))
            return

        file_names = [file for file in files if file.endswith('.csv')]

        for file_name in file_names:
            file_path = folder_path + file_name

            with open(file_path, newline='\n', encoding='utf-8') as file:
                data = csv.DictReader(file)

                city_counter = 0
                city_skipped = 0

                for city_data in data:
                    region, is_region_created = Region.objects.get_or_create(
                        name=city_data.get('region')
                    )
                    if log and is_region_created:
                        self.print_stdout(f'{region} is loaded')

                    district, is_district_created = District.objects.get_or_create(
                        name=city_data.get("district"),
                        region=region,
                        short_name=city_data.get("district_short")
                    )
                    if log and is_district_created:
                        self.print_stdout(f'{district} is loaded')

                    city_type, is_city_type_created = CityType.objects.get_or_create(
                        name=city_data.get("type"),
                        short_name=city_data.get("type_short")
                    )
                    if log and is_city_type_created:
                        self.print_stdout(f'{city_type} is loaded')

                    city, is_city_created = City.objects.get_or_create(
                        district=district,
                        type=city_type,
                        name=city_data.get("name"),
                        latitude=float(city_data.get("latitude")),
                        longitude=float(city_data.get("longitude")),
                        is_district_shown=bool(int(city_data.get(
                            "is_district_shown"
                        ))),
                    )

                    if is_city_created:
                        city_counter += 1
                    else:
                        city_skipped += 1

            self.print_stdout(
                f'{file_name} is loaded\n'
                f'{city_counter} cities are loaded\n'
                f'{city_skipped} cities are skipped, '
                f'because they are already in the database')

    def print_stdout(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))
