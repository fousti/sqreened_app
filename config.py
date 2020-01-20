import os


DEFAULT_LOGGING_CONFIG = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}

class BaseConfig:
    DEBUG=False
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    LOGGING_CONFIG = DEFAULT_LOGGING_CONFIG

class DevelopmentConfig(BaseConfig):
    ENV='development'
    DEBUG = True
    HOST = 'localhost'
    PORT = 5000
