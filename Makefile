install:
	pip install -r requirements.txt

start:
	uvicorn app.main:app --host localhost --port 8000 --reload

build:
	docker compose build --no-cache

freeze:
	pip list --format=freeze > requirements.txt

up: clean freeze
	docker compose up -d

test:
	python -m pytest

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache