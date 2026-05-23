# Track-Runner

Дневник тренировок — FastAPI REST API.

## Запуск (разработка)

```bash
uv sync
cp .env.example .env        # и отредактировать SECRET_KEY, DATABASE_URL
make run                    # uvicorn app.main:app --reload
```

## Деплой на VPS без домена (через IP)

```bash
# 1. Клонировать
git clone <repo> /opt/track-runner
cd /opt/track-runner

# 2. Установить uv (если нет)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Установить зависимости (от пользователя, без root)
uv sync --no-dev

# 4. Запустить деплой (установит nginx, PostgreSQL, настроит всё)
sudo bash deploy/setup.sh

# 5. Готово
curl http://<IP-вашей-VPS>/health
```

Скрипт автоматически подставит IP в `.env` и nginx.
Куки работают без HTTPS (COOKIE_SECURE=false).

## Миграции

```bash
make migrate                # автогенерация + apply
```

## Тесты и линтинг

```bash
make check                  # ruff + pytest (все сразу)
make test                   # pytest (101 тестов)
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
│   │   └── statistics.py   # /api/statistics/running: недельная/месячная статистика
│   ├── dependencies.py     # Зависимости: JWT auth, пагинация
│   └── utils/
│       ├── security.py     # bcrypt, JWT, cookie helpers
│       └── rate_limit.py   # In-memory rate limiter (X-Real-IP)
├── alembic/                # Миграции БД
├── tests/                  # pytest тесты (101 тест)
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
| `POST /api/auth/logout`   | Выход (refresh token удаляется, access token живёт до expiry — ~15 мин, stateless JWT) |
| `GET /api/auth/me`        | Текущий пользователь  |
| `CRUD /api/cardio`        | Кардиотренировки      |
| `CRUD /api/strength`      | Силовые тренировки    |
| `GET /api/statistics/running` | Беговая статистика |