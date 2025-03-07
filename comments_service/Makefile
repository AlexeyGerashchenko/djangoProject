.PHONY: help install migrate makemigrations run test shell createsuperuser startapp startproject clean docker-build docker-up docker-down docker-logs

# Более простое определение путей
VENV_PYTHON = venv/bin/python
VENV_PIP = venv/bin/pip
SYSTEM_PYTHON = python
SYSTEM_PIP = python -m pip

# Проверяем наличие виртуального окружения
ifeq ($(wildcard $(VENV_PYTHON)),)
    PYTHON = $(SYSTEM_PYTHON)
    PIP = $(SYSTEM_PIP)
else
    PYTHON = $(VENV_PYTHON)
    PIP = $(VENV_PIP)
endif

help:
	@echo "Доступные команды:"
	@echo "  make install         - Установить зависимости"
	@echo "  make migrate         - Применить миграции"
	@echo "  make makemigrations  - Создать миграции"
	@echo "  make run             - Запустить сервер разработки"
	@echo "  make test            - Запустить тесты"
	@echo "  make shell           - Запустить Django shell"
	@echo "  make createsuperuser - Создать суперпользователя"
	@echo "  make clean           - Очистить временные файлы"
	@echo "  make docker-build    - Собрать Docker образ"
	@echo "  make docker-up       - Запустить контейнеры Docker"
	@echo "  make docker-down     - Остановить контейнеры Docker"
	@echo "  make docker-logs     - Показать логи контейнеров Docker"

install:
	$(PIP) install -r requirements.txt

migrate:
	$(PYTHON) manage.py migrate

makemigrations:
	$(PYTHON) manage.py makemigrations

run:
	$(PYTHON) manage.py runserver 0.0.0.0:8001

test:
	$(PYTHON) manage.py test

shell:
	$(PYTHON) manage.py shell

createsuperuser:
	$(PYTHON) manage.py createsuperuser

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	find . -name "*.pyo" -delete
	find . -name "*.orig" -delete

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f 