#!/bin/sh

poetry run alembic upgrade head

poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 &

sleep 2

poetry run python -m pytest tests/