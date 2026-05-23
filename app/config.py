import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set. Create a .env file or set the environment variable."
    )
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is not set. Create a .env file or set the environment variable."
    )

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"
# За reverse proxy (nginx/Caddy) выставить TRUSTED_PROXY=true
# и настроить прокси на передачу X-Real-IP / X-Forwarded-For
TRUSTED_PROXY = os.getenv("TRUSTED_PROXY", "false").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173")
