# VoiceAnswerBot

ТГ-бот для ответов на аудио-вопросы и анализа изображений

## Функциональные возможности

- Асинхронная обработка задач и взаимодействие с базой данных.
- Поддержка обработки и анализа фотографий через модули `file_manager` и `ai_helper`.
- Интеграция Docker для удобного развертывания.
- Управление миграциями базы данных с помощью Alembic.
- Реализация хранилища векторов для улучшения хранения и поиска данных.

## Структура проекта

- **ai_helper**: Модули для работы с задачами ИИ и вспомогательные функции.
- **amplitude_client**: Клиентские инструменты для интеграции с аналитикой Amplitude.
- **database**: Модули для взаимодействия с базой данных.
- **file_manager**: Функции для загрузки, обработки и анализа файлов.
- **migrations**: Модули для миграций базы данных с использованием Alembic.
- **Dockerfile**: Конфигурация для сборки Docker-образа.
- **docker-compose.yml**: Файл Docker Compose для оркестрации многоконтейнерных приложений.
- **main.py**: Основная точка входа приложения.

## Установка и настройка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Nikichel/your-repo-name.git
   cd your-repo-name

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python3 -m venv venv
    source venv/bin/activate

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt

4. Запустите приложение:
    ```bash
    python main.py

## Развертывание с помощью Docker

Чтобы развернуть приложение с использованием Docker:

1. Соберите Docker-образ:
    ```bash
    docker build -t your-app-name .

2. Запустите приложение с помощью Docker Compose:
    ```bash
    docker-compose up

## Миграции

Для работы с миграциями базы данных используйте Alembic:

1. Инициализируйте Alembic:
    ```bash
    alembic init migrations

2. Сгенерируйте новую миграцию после изменения моделей:
    ```bash
    alembic revision --autogenerate -m "Сообщение миграции"

3. Примените миграции:
    ```bash
    alembic upgrade head
