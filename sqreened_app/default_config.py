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

# MESSAGE_TYPES = [] # What type of message type do you want to dispatch, if empty, all message type will be dispatch
# EVENT_TYPES = [] # What types of Event do you want to dispatch (https://docs.sqreen.com/integrations/webhooks/#security-events)
# EVENT_CATEGORY = [] # For security event, what type of category, if empty, all category will be dispatch
# EVENT_KIND = [] # security event subcategory to dispatch, if empty all subcategory will be dispatch
# TASKS_HANDLERS = {} # A dict containing each task name to dispatch to with
# their specific config as a Value
# Dispatch task must have the signature f(config, message)

AuthenticationDispatcherConfig = {
    "MESSAGE_TYPES": ["security_event"],
    "EVENT_CATEGORY": ["authentication"],
    "TASK_HANDLERS": {"logging_dispatcher":
                {"target_log_file":"/tmp/auth_event.log"}
              }
}

HTTPDispatcherConfig = {
    "MESSAGE_TYPES": ["security_event"],
    "EVENT_CATEGORY": ["authentication"],
    "EVENT_KIND": ["auth_new_location"],
    "TASK_HANDLERS": {"http_dispatcher":
                      {"endpoint":"http://localhost:8080",
                       "headers": {"X-Token": "12345"}}
              }
}
class BaseConfig:
    DEBUG = False
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    LOGGING_CONFIG = DEFAULT_LOGGING_CONFIG
    DISPATCHERS = [AuthenticationDispatcherConfig, HTTPDispatcherConfig]
    SQREEN_TOKEN = "1234"

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    HOST = "localhost"
    PORT = 5000
    CELERY_BROKER_URL = "redis://localhost:6379/0"

class TestingConfig(BaseConfig):
    TESTING = True

class DockerConfig(BaseConfig):
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000
    CELERY_BROKER_URL = "redis://redis:6379/0"

class ProductionConfig(BaseConfig):
    pass
