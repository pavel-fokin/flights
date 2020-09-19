.PHONY: all
all: help

.PHONY: help
help:
	@echo 'Makefile help:                                       '
	@echo '                                                     '
	@echo '   lint              Run linters                     '
	@echo '   migrate           Run migrations                  '
	@echo '   migrations        Make migrations                 '
	@echo '   install           Install requirements            '
	@echo '   requirements      Compile files with requirements '
	@echo '   run               Run web app                     '
	@echo '   tests             Run unit tests                  '

.PHONY: requirements
requirements:
	@pip-compile requirements/dev.in -o requirements/dev.txt
	@pip-compile requirements/prod.in -o requirements/prod.txt

.PHONY: install
install:
	@pip install -r requirements/dev.txt
	@pip install -r requirements/prod.txt

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
	python manage.py runserver 0.0.0.0:5000
