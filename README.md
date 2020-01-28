# sqreened-app

sqreened-app is a Flask + Celery app for processing webhooks from sqreen backend (https://docs.sqreen.com/integrations/webhooks/)

It supports currently 2 backends : HTTP endpoint & Logging

You can via a configuration (inspired by how the python logging module is configured)
select which message types/events/event kinds are dispatched to.

You can find an example of configuration in `sqreened_app/default_config.py`.
This example dispatch all message of type `security_event` with the category `authentication` to a log file (so all event kind will be logged) and all message of type `security_event` with the category `authentication` and the event kind `auth_new_location` to an http backend.

All fields are well documented in comments.

The app use standard Flask configuration, you can override `sqreened_app/default_config.py` via the `FLASK_CONFIG` env variable pointing to your own config.py

## Quick Start

Run the all application: (make sure you have docker & docker-compose installed on your system):

    docker-compose up -d

You can test the API on http://localhost:5000/webhooks/

## Development

Use the Makefile to setup your dev env.
Make sure you have a fonctionning `make` on your system, and install virtualenv :
`pip install virtualenv`

Setup your env : `make venv`

Run the API locally: `make run`

Run the tests suite : `make test`

Make a python package (wheel) : `make package`

the `main.py`  at the project root provide a uwsgi callable `app`

## TODO
- Validate JSON schema for the `webhooks/` endpoint.
- Increase coverage with different configurations setups
- Track task status using celery result backend & local DB
- Add target backend (SMS, slack ?)

