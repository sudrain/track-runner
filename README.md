📁 track-runner/
├── app/
│   ├── __init__.py
│   ├── main.py               # Точка входа, создание FastAPI, подключение роутеров, статики
│   ├── config.py             # Настройки (строка подключения, секретные ключи)
│   ├── database.py           # Асинхронный движок SQLAlchemy, sessionmaker, Base
│   ├── models.py             # SQLAlchemy модели (User, CardioWorkout, CardioInterval, StrengthWorkout, Exercise, Set)
│   ├── schemas.py            # Pydantic схемы для валидации запросов/ответов
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py           # Роуты регистрации, логина, обновления токена
│   │   ├── cardio.py         # CRUD для кардио + интервалов
│   │   ├── strength.py       # CRUD для силовых
│   │   └── statistics.py     # Статистика по бегу
│   ├── dependencies.py       # Зависимости: получение текущего пользователя, проверка JWT
│   ├── utils/
│   │   ├── security.py       # Хеширование пароля, создание/проверка JWT
│   │   └── __init__.py
│   └── templates/            # Jinja2 шаблоны
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       └── dashboard.html    # Основная страница со списком тренировок и формами
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js             # fetch‑запросы для CRUD
│   ├── manifest.json          # PWA манифест
│   ├── sw.js                  # Service Worker (базовый кеш)
│   └── icons/                 # Иконки 192x192, 512x512
├── alembic/                   # Миграции (генерируются alembic init)
│   └── ...
├── alembic.ini
├── .env                       # Локальные переменные окружения (SECRET_KEY, DATABASE_URL)
├── pyproject.toml             # Зависимости (uv)
├── requirements.txt           # Альтернатива/экспорт
└── README.md