start:
	uv run uvicorn app.main:app --reload

lint:
	uv run ruff check app/ tests/

test:
	uv run pytest -v

test-cov:
	uv run pytest -v --cov=app --cov-branch

# make migrate M="description"  — создать миграцию (autogenerate) и применить
# make migrate                 — только применить непрописанные миграции (upgrade head)
migrate:
ifneq ($(M),)
	uv run alembic revision --autogenerate -m "$(M)"
endif
	uv run alembic upgrade head

check: lint test