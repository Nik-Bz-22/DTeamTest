.PHONY: all

run:
	@python manage.py runserver 0.0.0.0:8000

load-fixtures:
	@python manage.py loaddata main/fixtures/fixt_cv.json

run-all-tests:
	@python manage.py test


pre-commit-run-all:
	@pre-commit run --all-files

migrate:
	@python manage.py makemigrations
	@python manage.py migrate


# Docker commands

docker-run:
	docker compose up --build

create-superuser-docker:
	@docker compose exec web python manage.py createsuperuser

load-fixtures-docker:
	@docker compose exec web python manage.py loaddata main/fixtures/fixt_cv.json
