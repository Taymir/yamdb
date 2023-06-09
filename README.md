[![Badge](https://github.com/Taymir/Yamdb/actions/workflows/yamdb.yaml/badge.svg)](https://github.com/Taymir/yamdb/actions/workflows/yamdb.yaml)
# API Yamdb
Yamdb предоставляет API для работы с рецензиями на фильмы, книги, музыкальные произведения и другие подобные объекты

### Установка и запуск
Для установки, вам нужно запустить docker compose:
```shell
docker compose up
```
При этом создастся и запустится два контейнера: web - сервер gunicorn и db - контейнер с субд PostgreSQL

### Применение миграций
После первого запуска контейнеров, вам потребуется применить миграции. Для этого в отдельной консоли введите команду:
```shell
docker compose exec python manage.py migrate
```
### Создание суперпользователя
Для создания суперпользователя, выполните команду:
```shell
docker compose exec python manage.py createsuperuser
```
и введите данные суперпользователя
### Заполнение начальными данными
Для того чтобы заполнить базу данных начальными данными, введите команду:
```shell
docker compose exec python manage.py loaddata fixtures.json
```