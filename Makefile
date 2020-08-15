.PHONY: up build down

up:
	docker-compose up --build --force-recreate

up/d:
	docker-compose up -d --build --force-recreate

down:
	docker-compose down
