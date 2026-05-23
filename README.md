# Track-Runner

Дневник тренировок — FastAPI REST API.

## Запуск

```bash
uv sync
cp .env.example .env        # и отредактировать SECRET_KEY, DATABASE_URL
make run                    # uvicorn app.main:app --reload
```

## Миграции

```bash
make migrate                # автогенерация + apply
```

## Тесты и линтинг

```bash
make test                   # pytest
make lint                   # ruff check
```

## Проект

```
📁 track-runner/
├── app/
│   ├── main.py             # Точка входа, FastAPI app, middleware, exception handler
│   ├── config.py           # Настройки (SECRET_KEY, DATABASE_URL, CORS, rate limit)
│   ├── database.py         # Асинхронный SQLAlchemy движок + сессия
│   ├── models.py           # ORM модели (User, CardioWorkout, StrengthWorkout, …)
│   ├── schemas.py          # Pydantic схемы запросов/ответов
│   ├── routers/
│   │   ├── auth.py         # /api/auth: register, login, refresh, logout
│   │   ├── cardio.py       # /api/cardio: CRUD + bulk delete
│   │   ├── strength.py     # /api/strength: CRUD + bulk delete
│   │   └── statistics.py   # /api/stats: недельная/месячная статистика
│   ├── dependencies.py     # Зависимости: JWT auth, пагинация
│   └── utils/
│       ├── security.py     # bcrypt, JWT, cookie helpers
│       └── rate_limit.py   # In-memory rate limiter (X-Real-IP)
├── alembic/                # Миграции БД
├── tests/                  # pytest тесты (66 тестов)
├── alembic.ini
├── pyproject.toml          # uv-зависимости
└── Makefile                # run / test / lint / migrate
```

## API

| Endpoint               | Описание                |
|------------------------|-------------------------|
| `POST /api/auth/register` | Регистрация          |
| `POST /api/auth/login`    | Вход (access + refresh в куки) |
| `POST /api/auth/refresh`  | Refresh токена        |
| `POST /api/auth/logout`   | Выход                 |
| `GET /api/auth/me`        | Текущий пользователь  |
| `CRUD /api/cardio`        | Кардиотренировки      |
| `CRUD /api/strength`      | Силовые тренировки    |
| `GET /api/stats/running`  | Беговая статистика    |