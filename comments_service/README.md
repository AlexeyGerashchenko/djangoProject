# Сервис комментариев к постам

Проект на Django для создания и управления постами, комментариями и лайками.

## Функциональность

- CRUD операции для пользователей, постов и комментариев
- Система лайков для постов и комментариев
- API для взаимодействия с сервисом
- Документация API через Swagger
- Аутентификация и авторизация пользователей

## Технологии

- Python 3.9+
- Django 4.2
- Django REST Framework
- PostgreSQL
- Docker и Docker Compose

## Установка и запуск

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd comments_service
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

3. Запустите базу данных PostgreSQL:
```bash
cd storage
./start_db.sh
cd ..
```

4. Примените миграции и создайте суперпользователя:
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Запустите сервер разработки:
```bash
python manage.py runserver
```

### Запуск с использованием Docker

1. Соберите и запустите контейнеры:
```bash
docker-compose up -d
```

2. Примените миграции:
```bash
docker-compose exec web python manage.py migrate
```

3. Создайте суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Использование Makefile

Проект содержит Makefile для удобного запуска команд:

```bash
# Показать список доступных команд
make help

# Установить зависимости
make install

# Применить миграции
make migrate

# Запустить сервер разработки
make run

# Запустить тесты
make test

# Запустить контейнеры Docker
make docker-up
```

## API Endpoints

- `/api/users/` - Управление пользователями
- `/api/profiles/` - Управление профилями пользователей
- `/api/posts/` - Управление постами
- `/api/comments/` - Управление комментариями
- `/api-token-auth/` - Получение токена аутентификации
- `/swagger/` - Документация API (Swagger UI)
- `/redoc/` - Документация API (ReDoc)

## Тестирование

Для запуска тестов выполните:

```bash
python manage.py test
# или
make test
``` 