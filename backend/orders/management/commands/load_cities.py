import csv
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
            '-p', '--path', type=str,
            help='Путь к загружаемым файлам'
        )

    def handle(self, *args, **options):
        folder_path = options['path'] or DEFAULT_PATH
        file_names = [file if file.endswith('.csv') else f'{file}.csv'
                      for file in options['files']]

        for file_name in file_names:
            file_path = folder_path + file_name

            with open(file_path, newline='\n', encoding='utf-8') as file:
                data = csv.DictReader(file)

                for city_data in data:
                    region, _ = Region.objects.get_or_create(
                        name=city_data.get('region')
                    )
                    district, _ = District.objects.get_or_create(
                        name=city_data.get("district"),
                        region=region,
                        short_name=city_data.get("district_short")
                    )
                    city_type, _ = CityType.objects.get_or_create(
                        name=city_data.get("type"),
                        short_name=city_data.get("type_short")
                    )
                    city, _ = City.objects.get_or_create(
                        district=district,
                        type=city_type,
                        name=city_data.get("name"),
                        latitude=float(city_data.get("latitude")),
                        longitude=float(city_data.get("longitude")),
                        is_district_shown=bool(int(city_data.get("is_district_shown"))),
                    )
            self.stdout.write(self.style.SUCCESS(f'{file_name} is loaded'))
