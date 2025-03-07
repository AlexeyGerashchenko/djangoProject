#!/bin/bash

# Переходим в корневую директорию проекта
cd ..

# Запускаем только сервис базы данных
docker-compose up -d db

echo "База данных PostgreSQL запущена на порту 5432"
echo "Данные для подключения:"
echo "  Хост: localhost"
echo "  Порт: 5432"
echo "  Пользователь: postgres"
echo "  Пароль: postgres"
echo "  База данных: comments_db" 