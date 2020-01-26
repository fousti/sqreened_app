.ONESHELL:

APP_NAME = sqreened_app

all: run

clean:
	rm -rf venv
	rm -rf *.egg-info
	rm -rf dist
	rm -rf *.log*

venv:
	virtualenv --python=python3 venv

dev-env: venv
	. venv/bin/activate
	pip install -r dev-requirements.txt
	pip install -e .

run: venv
	FLASK_APP=$(APP_NAME) SQREEN_APP_NAME=$(APP_NAME) FLASK_ENV=development venv/bin/python run.py

test: venv
	FLASK_APP=$(APP_NAME) SQREEN_APP_NAME=$(APP_NAME) FLASK_ENV=testing tox

sdist: venv test
	venv/bin/python setup.py sdist
