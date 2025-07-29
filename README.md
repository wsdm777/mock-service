# ЦБ РФ API Mock

Mock сервис, имитирующий ответ от **XML API**


## Структура проекта

```
├── alembic/               # Миграции
│
├── src/                  
│   ├── config.py          # Конфигурация приложения
│   ├── logger.py          # Логирование
│   ├── main.py            # Точка входа
│   ├── repository.py      # Работа с БД (репозиторий)
│   ├── router.py          # API-роут
│   ├── schemas.py         # Pydantic-схемы
│   ├── service.py         # Слой сервиса
│   └── database/
│       ├── database.py    # Настройка подключения к БД
│       ├── models.py      # SQLAlchemy модели
│       ├── db_init.py     # Инициализация БД
│       └── initial_currency_data.py  # Стартовые данные
│
├── tests/
│   └── test_service.py    # Тесты сервиса
├── alembic.ini            # Конфиг Alembic (миграции БД)
├── entrypoint.sh          # Скрипт запуска контейнера
├── pyproject.toml         # Зависимости Poetry
├── poetry.lock            # Фиксированные версии зависимостей
```


## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/wsdm777/mock-service.git
cd mock-service
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

3. Запустите приложение с помощью Make:
```bash
make up
```

## Документация API

Swagger UI доступен по адресу:

```
http://localhost:8000/docs
```


### Запуск тестов

1. Создайте файл `test.env` на основе `.env.example`:
```bash
cp .env.example test.env
```
2. Запустите тесты с помощью Make
```bash
make test
```