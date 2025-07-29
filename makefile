.PHONY: up down build logs restart test test-down

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

restart: down build up

test-down:
	docker compose -f docker-compose.test.yaml down

test-up:
	docker compose -f docker-compose.test.yaml up --build -d 

test:
	docker compose -f docker-compose.test.yaml down
	docker compose -f docker-compose.test.yaml up --build -d 
