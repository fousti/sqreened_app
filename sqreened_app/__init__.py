import os
import logging.config

from flask import Flask
from werkzeug.utils import import_string
from celery import Celery
import sqreen

import sqreened_app.default_config

CONFIG_NAME = {
    'development': default_config.DevelopmentConfig,
    'testing': default_config.TestingConfig,
    'docker': default_config.DockerConfig,
    'production': default_config.ProductionConfig
}


def create_app(config_name=None, celery=None, **kwargs):
    app = Flask(__name__, **kwargs)

    env = app.env
    app.config.from_object(CONFIG_NAME[env])

    if "FLASK_CONFIG" in os.environ:
        app.config.from_envvar("FLASK_CONFIG")

    print(app.config)
    sqreen_token = os.getenv("SQREEN_TOKEN")
    if sqreen_token and not "SQREEN_TOKEN" in app.config:
        app.config["SQREEN_TOKEN"] = sqreen_token

    logging.config.dictConfig(app.config["LOGGING_CONFIG"])

    if celery:
        init_celery(celery, app)
    from sqreened_app.views import hooks_bp
    app.register_blueprint(hooks_bp)
    sqreen.start()

    return app

def make_celery(app_name=__name__):
    return Celery(__name__)

def init_celery(celery, app):
    celery.conf.update(app.config)
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask


celery = make_celery()
