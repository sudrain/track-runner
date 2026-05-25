start:
	uv run uvicorn app.main:app --reload

lint:
	uv run ruff check app/ tests/

test:
	uv run pytest -v

test-cov:
	uv run pytest -v --cov=app --cov-branch

check: lint test