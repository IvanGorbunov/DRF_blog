# Тестовое задание на разработку REST API 
### Задача:
Реализовать REST API для системы комментариев блога.

### Функциональные требования:
У системы должны быть методы API, которые обеспечивают
- Добавление статьи (Можно чисто номинально, как сущность, к которой крепятся комментарии).
- Добавление комментария к статье.
- Добавление коментария в ответ на другой комментарий (возможна любая вложенность).
- Получение всех комментариев к статье вплоть до 3 уровня вложенности.
- Получение всех вложенных комментариев для комментария 3 уровня.
- По ответу API комментариев можно воссоздать древовидную структуру.

### Нефункциональные требования:
- Использование Django ORM.
- Следование принципам REST.
- Число запросов к базе данных не должно напрямую зависеть от количества комментариев, уровня вложенности.
- Решение в виде репозитория на Github, Gitlab или Bitbucket.
- readme, в котором указано, как собирать и запускать проект. Зависимости указать в requirements.txt либо использовать poetry/pipenv.
- Использование свежих версий python и Django.

### Будет плюсом:
- Использование PostgreSQL.
- docker-compose для запуска api и базы данных.
- Swagger либо иная документация к апи.

Всё остальное (авторизация, админки, тесты) - по желанию, оцениваться не будет. Использование DRF не обязательно.

## Краткое описание рекализации:
Директории проекта:
```
- DRF_blog - настройки проекта
- blog - модуль блога
- utils - инструменты
```


## Установка и запуск:
1. Клонировать репозиторий:
   ```bash
   git clone 
   ```
2. Создать и заполнить файл`.env` по шаблону `/DRF_blog/.env.template`. Файл`.env` дожен находится в одной директории с `settings.py`
   Переменные для заполнения
   - для запуска локально:
      ```
      DEBUG=on
      SQL_DEBUG=on
      SECRET_KEY=XXXXXX
      DATABASE_URL=psql://drf_blog:drf_blog@127.0.0.1:5432/drf_blog
      DJANGO_ALLOWED_HOSTS=*
      STATIC_ROOT=var/www/staticfiles
      ```
   - для запуска в контейнере `Docker`:
      ```
      DEBUG=on
      SQL_DEBUG=on
      SECRET_KEY=XXXXXX
      DATABASE_URL=psql://postgres:postgres@db:5432/postgres
      DJANGO_ALLOWED_HOSTS=*
      STATIC_ROOT=var/www/staticfiles
      ```
   
3. Установить витуальное окружение для проекта `venv` в директории проекта:
    ```bash
    python3 -m venv venv
    ```
4. Активировать виртуальное окружение:
   - для Linux: 
       ```bash
       source venv/bin/activate
       ```
   - для Windows:
       ```bash
       .\venv\Scripts\activate.ps1
       ```
5. Установить зависимости из `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
6. Выполнить миграции:
    ```bash
    python3 manage.py migrate
    ```
7. Запустить сервер:
    ```bash
    python3 manage.py runserver
    ```
8. Список эндпоинтов:
   ```angular2html
   http://127.0.0.1:8000/swagger/ - документация к API
   http://127.0.0.1:8000/api/blog/ - список  (GET, POST)
   ```
9. Запуск в контейнерах:
    ```bash
    mkdir -p ./Data/db/
    docker-compose up -d --build
    docker-compose run --rm web sh -c "python3 manage.py migrate"
    docker-compose run --rm web sh -c "python3 manage.py createsuperuser"
    ```
10. Запуск тестов в контейнере:
    ```bash
    docker-compose run --rm web ./manage.py test
    ```


