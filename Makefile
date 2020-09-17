.PHONY: all
all: help

.PHONY: help
help:
	@echo 'Makefile help:                                       '
	@echo '                                                     '
	@echo '   migrate           Run migrations                  '
	@echo '   migrations        Make migrations                 '
	@echo '   run               Run web app                     '
	@echo '   lint              Run linters                     '
	@echo '   tests             Run unit tests                  '

.PHONY: migrations
migrations:
	python manage.py makemigrations

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: lint
lint:
	@flake8 flights tests
	@pylint --exit-zero --rcfile setup.cfg flights tests

.PHONY: tests
tests:
	@PYTHONPATH=. pytest tests --cov -Wignore

.PHONY: run
run:
	@export GIT_REV=`git rev-parse HEAD`;\
	python manage.py runserver 5000
