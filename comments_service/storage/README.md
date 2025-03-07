# Хранилище данных для сервиса комментариев

Эта директория содержит настройки для хранилища данных проекта.

## Структура базы данных

База данных PostgreSQL содержит следующие основные таблицы:
- `users` - информация о пользователях
- `posts` - посты пользователей
- `comments` - комментарии к постам
- `post_likes` - лайки к постам
- `comment_likes` - лайки к комментариям

## Применение миграций

Для применения миграций выполните следующие команды:

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя для доступа к админке
python manage.py createsuperuser
```

## Запуск с использованием Docker

```bash
# Сборка и запуск контейнеров
docker-compose up -d

# Применение миграций внутри контейнера
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser
``` 