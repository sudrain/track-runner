.PHONY: help start dev lint test test-cov migrate check \
        frontend-dev frontend-build frontend-check frontend-test \
        install setup clean

.DEFAULT_GOAL := help

help:  ## Показать список доступных команд
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# === Dev ===

start:  ## Запустить backend (uvicorn --reload, порт 8000)
	uv run uvicorn app.main:app --reload

frontend-dev:  ## Запустить frontend (Vite dev server, порт 5173)
	cd frontend && npm run dev

dev:  ## Запустить backend и frontend одновременно
	@trap 'kill 0' EXIT; \
		$(MAKE) start & \
		$(MAKE) frontend-dev; \
		wait

# === Testing ===

lint:  ## Проверить backend линтером (ruff)
	uv run ruff check app/ tests/

frontend-check:  ## Проверить frontend (svelte-check + tsc)
	cd frontend && npm run check

check: lint test frontend-check  ## Запустить все проверки (линтер + тесты + typecheck)

test:  ## Запустить backend-тесты (pytest)
	uv run pytest -v

test-cov:  ## Запустить backend-тесты с coverage
	uv run pytest -v --cov=app --cov-branch

frontend-test:  ## Запустить frontend-тесты (vitest)
	cd frontend && npx vitest run

# === Build ===

frontend-build:  ## Собрать frontend для production
	cd frontend && npm run build

# === Setup ===

install:  ## Установить все зависимости (backend + frontend)
	uv sync && cd frontend && npm install

setup: install migrate  ## Полная настройка проекта (установка + миграции)

migrate:  ## Применить миграции БД; M="описание" — создать новую
ifneq ($(M),)
	uv run alembic revision --autogenerate -m "$(M)"
endif
	uv run alembic upgrade head

# === Clean ===

clean:  ## Удалить кэш Python и артефакты сборки
	rm -rf __pycache__ .pytest_cache .ruff_cache
	rm -rf frontend/dist
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
