start:
	uv run uvicorn app.main:app --reload

test:
	uv run pytest -v

test-cov:
	uv run pytest -v --cov=app