.PHONY: up down shell lint typecheck test check logs migrate

up:
	docker-compose up --build

down:
	docker-compose down

shell:
	docker-compose exec django python manage.py shell

lint:
	docker-compose exec django ruff check .

typecheck:
	docker-compose exec django mypy .

test:
	docker-compose exec django python manage.py test

check: lint typecheck test

logs:
	docker-compose logs -f

migrate:
	docker-compose exec django python manage.py migrate