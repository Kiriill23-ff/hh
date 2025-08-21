MyTwitter API Service


Описание проекта
API-сервис, имитирующий функционал Twitter, разработан с использованием FastAPI и PostgreSQL. Поддерживает основные
возможности, такие как создание твитов, лайки, подписки, загрузка медиафайлов и управление профилем.


Основной функционал


Создание твитов


URL: POST /api/tweets


Тело запроса:

{
  "tweet_data": "string",
  "tweet_media_ids": [1, 2] // Опционально
}

Ответ:

{
  "result": true,
  "tweet_id": 123
}

Удаление твита


URL: DELETE /api/tweets/<id>


Ответ:

{
  "result": true
}

Лайки


Добавление лайка:


URL: POST /api/tweets/<id>/likes


Ответ:

{
  "result": true
}

Удаление лайка:


URL: DELETE /api/tweets/<id>/likes


Ответ:

{
  "result": true
}

Подписки


Подписаться на пользователя:


URL: POST /api/users/<id>/follow


Ответ:

{
  "result": true
}

Отписаться от пользователя:


URL: DELETE /api/users/<id>/follow


Ответ:

{
  "result": true
}

Загрузка медиафайлов


URL: POST /api/medias


Форма:

form: file="image.jpg"

Ответ:

{
  "result": true,
  "media_id": 456
}

Профиль пользователя


Получение информации о себе:


URL: GET /api/users/me


Ответ:

{
  "result": true,
  "user": {
    "id": 11,
    "name": "Test User",
    "followers": [
      {"id": 6, "name": "Jeremy Smith"},
      {"id": 9, "name": "Lisa Wilcox"}
    ],
    "following": [
      {"id": 1, "name": "Kathleen Meyer"}
    ]
  }
}

Получение информации о другом пользователе:


URL: GET /api/users/<id>


Ответ:

{
  "result": true,
  "user": {
    "id": 12,
    "name": "Other User",
    "followers": [...],
    "following": [...]
  }
}

Лента твитов


URL: GET /api/tweets


Ответ:

{
  "result": true,
  "tweets": [
    {
      "id": 101,
      "content": "Hello World!",
      "attachments": ["/media/1", "/media/2"],
      "author": {
        "id": 11,
        "name": "Test User"
      },
      "likes": [
        {"user_id": 6, "name": "Jeremy Smith"},
        {"user_id": 9, "name": "Lisa Wilcox"}
      ]
    }
  ]
}

Технические особенности


Язык: Python 3.12.6

Фреймворк: FastAPI

База данных: PostgreSQL

Контейнеризация: Docker и docker-compose

Тестирование: pytest

Линтинг: mypy, black, isort


Установка и запуск

Локальный запуск


Клонируйте репозиторий:

git clone <repository-url>
cd <repository-folder>

Установите зависимости:

pip install -r requirements.txt

Настройте переменные окружения, используя файл .env.template:

cp .env.template .env
Заполните необходимые значения в файле .env. Обратите внимание на переменную MODE=TEST. Это значение используется
для запуска тестов. Вы можете заменить его на любое значение, соответствующее режиму работы вашего приложения (например,
MODE=development или MODE=production), в зависимости от ваших потребностей.


Выполните миграции базы данных:

alembic upgrade head

Запустите сервер разработки:

uvicorn app.main:app --reload

Документация будет доступна по адресу: http://127.0.0.1:8000/docs



Запуск с использованием Docker


Настройте переменные окружения, используя файл .env.template:

cp .env.template .env
Заполните необходимые значения в файле .env. Обратите внимание на переменную MODE=TEST. Это значение используется
для запуска тестов. Вы можете заменить его на любое значение, соответствующее режиму работы вашего приложения (например,
MODE=development или MODE=production), в зависимости от ваших потребностей.


Убедитесь, что значения из файла .env соответствуют параметрам в docker-compose.yml. Замените переменные окружения
для PostgreSQL:
environment:

  - POSTGRES_USER=<ваше_значение>
  - POSTGRES_PASSWORD=<ваше_значение>
  - POSTGRES_DB=<ваше_значение>
healthcheck:
  test: [ "CMD-SHELL", "pg_isready -U <ваше_значение> -d <ваше_значение>" ]

Соберите и запустите контейнеры:

docker-compose up -d

Убедитесь, что приложение работает: http://127.0.0.1:80



Тестирование
Для запуска тестов выполните:

pytest tests

Используемые технологии


FastAPI: Для создания веб-API.

PostgreSQL: Для хранения данных.

Docker: Для контейнеризации приложения.