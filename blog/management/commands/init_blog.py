import json
import time
from os import listdir
from django.apps import apps
from os.path import join, isdir, isfile, splitext
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection, transaction

from blog.models import User, Article


def seeder_factory(mdl, data, parent=None):
    max_ids = []
    for d in data:
        try:
            children = d.pop('children')
        except KeyError:
            children = None
        try:
            if parent is None:
                el, _ = mdl.objects.get_or_create(**d)
            else:
                el, _ = mdl.objects.get_or_create(**{**d, 'parent': parent})
            if 'id' in d:
                max_ids.append(d['id'])
        except Exception as ex:
            print(ex)
            continue

        if children is not None:
            max_ids.append(seeder_factory(mdl, children, el))

    return max(max_ids) if max_ids else None


class Command(BaseCommand):
    help = 'Развертываение приложения "Блог"'
    seed_path = join(settings.BASE_DIR, 'blog/management/seed')

    def handle(self, *args, **options):
        start_time = time.time()
        self.stdout.write('Инициализация приложения "Блог"')

        with transaction.atomic():
            app_dirs = [name for name in listdir(join(self.seed_path)) if isdir(join(self.seed_path, name))]
            app_dirs.sort()
            for app_name in app_dirs:
                self.stdout.write(f'    Приложение {app_name[4:]}')
                app_path = join(self.seed_path, app_name)
                mdls_name = [name for name in listdir(app_path) if isfile(join(app_path, name))]
                mdls_name.sort()
                for mdl_name in mdls_name:
                    mdl_path = join(app_path, mdl_name)
                    mdl, _ = splitext(mdl_name)
                    self.stdout.write(f'        Модель {mdl}')
                    model = apps.get_model(app_name[4:], mdl[4:])
                    with open(mdl_path, encoding='utf-8') as file:
                        max_id: int or None = seeder_factory(model, json.load(file))
                    if max_id is not None:
                        with connection.cursor() as cursor:
                            cursor.execute(f'alter sequence {app_name[4:].lower()}_{mdl[4:].lower()}_id_seq restart with {max_id + 1}')

        # добавление статей в цикле
        with transaction.atomic():
            admin = User.objects.first()
            Article.objects.bulk_create([Article(title=f'Статья {str(i)}', author=admin) for i in range(0, 20000)], ignore_conflicts=True)

        self.stdout.write(f'Инициализация приложения завершена за время: {str((time.time() - start_time / 60))} минут')