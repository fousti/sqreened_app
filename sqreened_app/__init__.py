import os
import logging.config

from flask import Flask
from werkzeug.utils import import_string

from sqreened_app.views import hooks_bp

CONFIG_NAME = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
}

def get_config(config_name=None):
    flask_config_name = os.getenv('FLASK_CONFIG', 'development')
    if config_name is not None:
        flask_config_name = config_name
    return import_string(CONFIG_NAME[flask_config_name])

def create_app(config_name=None, **kwargs):
    app = Flask(__name__, **kwargs)

    try:
        app.config.from_object(get_config(config_name))
    except ImportError:
        raise Exception('Invalid Config')

    logging.config.dictConfig(app.config["LOGGING_CONFIG"])

    app.register_blueprint(hooks_bp)
    return app


