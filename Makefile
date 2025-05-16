.PHONY: all

load-fixtures:
	@python manage.py loaddata main/fixtures/fixt_cv.json

run-all-tests:
	@python manage.py test


pre-commit-run-all:
	@pre-commit run --all-files

migrate:
	@python manage.py makemigrations
	@python manage.py migrate
