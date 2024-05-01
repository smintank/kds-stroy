import csv
import os

from django.core.management.base import BaseCommand
from kds_stroy import settings
from orders.models import Region, District, City, CityType

DEFAULT_PATH = str(settings.BASE_DIR) + '/data/'


class Command(BaseCommand):
    help = 'Команда для загрузки городов из .csv файлов в базу данных.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--files', type=str, nargs='+',
            help='Файлы которые будут загружены'
        )

        parser.add_argument(
            '-a', '--all', action='store_true',
            help='Загрузить все файлы в директории'
        )

        parser.add_argument(
            '-l', '--log', action='store_true',
            help='Выводить логи загруженных городов'
        )

        parser.add_argument(
            '-p', '--path', type=str,
            help='Путь к загружаемым файлам'
        )

    def handle(self, *args, **options):
        log = True if options['log'] else False
        folder_path = options['path'] or DEFAULT_PATH
        if options['all']:
            files = os.listdir(folder_path)
        elif options['files']:
            files = options['files']
        else:
            self.stdout.write(self.style.ERROR(
                'Не указаны файлы для загрузки. Используйте -f или -a ключи.'
            ))
            return

        file_names = [file for file in files if file.endswith('.csv')]

        for file_name in file_names:
            file_path = folder_path + file_name

            with open(file_path, newline='\n', encoding='utf-8') as file:
                data = csv.DictReader(file)
                counter = 0
                for city_data in data:
                    region, is_region_created = Region.objects.get_or_create(
                        name=city_data.get('region')
                    )
                    if log and is_region_created:
                        self.stdout.write(self.style.SUCCESS(f'{is_region_created} is loaded'))

                    district, is_district_created = District.objects.get_or_create(
                        name=city_data.get("district"),
                        region=region,
                        short_name=city_data.get("district_short")
                    )
                    if log and is_district_created:
                        self.stdout.write(self.style.SUCCESS(f'{is_district_created} is loaded'))

                    city_type, is_city_type_created = CityType.objects.get_or_create(
                        name=city_data.get("type"),
                        short_name=city_data.get("type_short")
                    )
                    if log and is_city_type_created:
                        self.stdout.write(self.style.SUCCESS(f'{is_city_type_created} is loaded'))

                    city, is_city_created = City.objects.get_or_create(
                        district=district,
                        type=city_type,
                        name=city_data.get("name"),
                        latitude=float(city_data.get("latitude")),
                        longitude=float(city_data.get("longitude")),
                        is_district_shown=bool(int(city_data.get("is_district_shown"))),
                    )
                    if log and is_city_created:
                        self.stdout.write(self.style.SUCCESS(f'{city} is loaded'))
                    if is_city_created:
                        counter += 1

            self.stdout.write(self.style.SUCCESS(f'{file_name} is loaded'))
            self.stdout.write(self.style.SUCCESS(f'{counter} cities are loaded'))
