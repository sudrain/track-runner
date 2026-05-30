# Track-Runner — AI Agent Context

## Стек

| Слой | Технологии |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 async, Alembic, Pydantic v2 |
| DB | SQLite (dev), PostgreSQL + asyncpg (prod) |
| Auth | bcrypt, JWT (access ~30m + refresh ~7d) в http-only cookies |
| Frontend | Svelte 5, TypeScript 6, Vite 8, Tailwind 4 |
| Тесты | pytest-asyncio, httpx.AsyncClient, pytest-cov |
| Инструменты | uv (пакетный менеджер), Ruff (линтер) |

## Команды

```bash
make help               # Список всех команд

# Dev
make start              # Backend (uvicorn --reload, порт 8000)
make frontend-dev       # Frontend (Vite, порт 5173)
make dev                # Backend + frontend одновременно

# Проверки
make lint               # Ruff (backend)
make frontend-check     # Svelte-check + tsc (frontend)
make check              # lint + test + frontend-check
make test               # Pytest (backend, 132 теста)
make test-cov           # Pytest с coverage
make frontend-test      # Vitest (frontend)

# Сборка
make frontend-build     # Production build фронта

# Установка / настройка
make install            # uv sync + npm install
make setup              # install + migrate
make migrate            # Миграции БД (M="desc" — создать новую)

# Утилиты
make clean              # Удалить кэш и артефакты
```

## Архитектура

```
app/
├── main.py              # FastAPI app, CORS, lifespan, /health
├── config.py            # Env-конфиг (DATABASE_URL, SECRET_KEY, JWT, CORS, LOG_LEVEL)
├── database.py          # async SQLAlchemy engine + sessionmaker
├── models.py            # ORM: User, CardioWorkout, CardioInterval, StrengthWorkout, Exercise, Set, RevokedRefreshToken
├── schemas.py           # Pydantic схемы (register, login, cardio/strength CRUD, stats)
├── dependencies.py      # DI: get_db, get_current_user, PaginatedParams
├── utils/
│   ├── security.py      # bcrypt hash/verify, JWT create/decode
│   └── rate_limit.py    # In-memory sliding window rate limiter (по IP)
└── routers/
    ├── auth.py          # POST /api/auth/{register,login,refresh,logout}, GET /api/auth/me
    ├── cardio.py        # CRUD /api/cardio
    ├── strength.py      # CRUD /api/strength
    └── statistics.py    # GET /api/statistics/running (week/month/year distance + avg tempo)
```

```
frontend/src/
├── main.ts, App.svelte, app.css
├── lib/
│   ├── router.svelte.ts       # Hash-based SPA роутер (runes)
│   ├── api/
│   │   └── client.ts          # HTTP-клиент с auto-refresh
│   ├── stores/
│   │   ├── auth.svelte.ts     # Auth store
│   │   ├── toast.svelte.ts    # Toast-уведомления
│   │   ├── confirm.svelte.ts  # Confirm-диалог
│   │   ├── stats.svelte.ts    # Статистика бега
│   │   └── workouts.svelte.ts # CardioStore + StrengthStore
│   ├── components/
│   │   ├── Layout.svelte      # Обёртка страницы (Navbar + TabBar)
│   │   ├── Navbar.svelte      # Верхняя навигация (десктоп)
│   │   ├── TabBar.svelte      # Нижняя навигация (мобилки)
│   │   ├── Skeleton.svelte    # Пульсирующий плейсхолдер загрузки
│   │   ├── Toast.svelte       # Всплывающие уведомления
│   │   ├── ConfirmDialog.svelte # Модальное подтверждение
│   │   ├── Pagination.svelte  # Пагинация
│   │   ├── CardioForm.svelte  # Форма кардиотренировки
│   │   ├── StrengthForm.svelte # Форма силовой тренировки
│   │   ├── IntervalList.svelte # Таблица интервалов (read-only)
│   │   └── ExerciseList.svelte # Список упражнений (read-only)
│   └── utils/
│       ├── format.ts          # Форматирование дат, расстояний
│       └── tempo.ts           # Расчёт и форматирование темпа
└── routes/                    # Home, Login, Register, CardioList/Detail/New, StrengthList/Detail/New
```

## Переменные окружения (.env)

| Переменная | По умолчанию | Описание |
|---|---|---|
| DATABASE_URL | sqlite+aiosqlite:///./dev.db | PostgreSQL для prod |
| SECRET_KEY | change-me-in-production | JWT secret |
| ACCESS_TOKEN_EXPIRE_MINUTES | 30 | Время жизни access token |
| REFRESH_TOKEN_EXPIRE_DAYS | 7 | Время жизни refresh token |
| LOG_LEVEL | INFO | DEBUG/INFO/WARNING/ERROR |
| AUTO_MIGRATE | true | Миграции при старте |
| COOKIE_SECURE | false | Secure flag для кук |
| TRUSTED_PROXY | false | Trust X-Real-IP/X-Forwarded-For |

## Быстрый старт (если проект свежий)

```bash
cp .env.example .env
make setup
make start
```

## Конвенции

- **Не добавлять комментарии в код** без явной просьбы.
- Ruff: line-length=88, target py312, правила E,F,I,N,W,UP,B,SIM.
- Ruff игнорирует B008, в `tests/conftest.py` — E402.
- Коммиты только по явной просьбе.
- После изменений запускать `make check` (lint + test + frontend-check).
- TypeScript, без `any`, строгие типы.
- Svelte 5 runes ($state, $derived, $effect) — современный синтаксис.
- Изменения тестов только по явной просьбе.

## Правила работы AI-агента

- **Объяснять команды простыми словами** — перед тем как выполнить команду, я поясню что делаю и зачем.
- **Не трогать лишнего** — я меняю только те файлы, которые нужны для задачи.
- **Проверка после изменений** — после любых правок я запускаю `make lint` и `make test`.
- Если тесты падают — объясняю причину и исправляю.
- **Правила коммитов**:
  - Сообщения только на английском.
  - Один коммит = логически связанная группа изменений.
  - Показывать `git diff --stat` перед коммитом.
  - Добавлять только нужные файлы (без `-a`, staged carefully).
  - Не коммитить секреты, `.env`, `*.db`, `node_modules`.
  - Коммиты только по явной просьбе.
  - Перед пушем проверять, что `make check` проходит.
- **Безопасная работа с git**:
  - Я не делаю commit/push без твоего разрешения.
  - Если хочешь сохранить изменения — скажи «закоммить».
  - Перед коммитом я покажу что изменилось (git diff).

## Как попросить помощи

- Если что-то непонятно — просто напиши «объясни».
- Если ошибка — покажи текст ошибки, я помогу её понять.
- Если хочешь отменить изменения — скажи «отмени».
- Если я делаю что-то не так — напиши «стоп» и объясни что не так.

## Тестирование

- 137 тестов, `pytest -v` для запуска.
- Фикстуры: `client`, `test_user`, `auth_client`, `second_user`, `second_auth_client`.
- Временная SQLite БД на сессию, очистка таблиц после каждого теста.
