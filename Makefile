.ONESHELL:

APP_NAME = sqreened_app

all: run

clean:
	rm -rf venv
	rm -rf *.egg-info
	rm -rf dist
	rm -rf *.log*
	rm -rf .tox

venv:
	virtualenv --python=python3 venv
	. venv/bin/activate
	pip install -r dev-requirements.txt
	pip install -e .

deps:
	pip install -r dev-requirements.txt
	pip install -e .

run: venv
	FLASK_APP=$(APP_NAME) SQREEN_APP_NAME=$(APP_NAME) FLASK_ENV=development venv/bin/python main.py

test: venv
	FLASK_APP=$(APP_NAME) SQREEN_APP_NAME=$(APP_NAME) FLASK_ENV=testing tox

sdist: venv test
	venv/bin/python setup.py sdist

docker-cmd: deps
	FLASK_APP=$(APP_NAME) SQREEN_APP_NAME=$(APP_NAME) FLASK_ENV=docker python main.py

docker-cmd-worker: deps
	FLASK_ENV=docker celery worker -A celery_worker.celery --loglevel=debug --pool=solo
