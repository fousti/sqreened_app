import os
import logging.config

from flask import Flask
from werkzeug.utils import import_string
import sqreen

import sqreened_app.default_config
from sqreened_app.views import hooks_bp

CONFIG_NAME = {
    'development': default_config.DevelopmentConfig,
    'testing': default_config.TestingConfig,
    'production': default_config.ProductionConfig
}

def create_app(config_name=None, **kwargs):
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

    app.register_blueprint(hooks_bp)
    sqreen.start()

    return app


