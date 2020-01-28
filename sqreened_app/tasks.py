import sys
import json

from flask import current_app
from celery.utils.log import get_task_logger
import requests

from sqreened_app import celery


task_logger = get_task_logger(__name__)

class DispatcherException(Exception):
    pass

class InvalidDispatcherConfigException(DispatcherException):
    pass

class UndefinedTaskHandlerException(DispatcherException):
    pass


def is_valid_type(type_, types):
    return (not types or (type_ in types))

def trigger_dispatchers(msg, dispatchers):
    for dispatcher in dispatchers:
        message_types = dispatcher.get("MESSAGE_TYPES", [])
        to_dispatch = is_valid_type(msg["message_type"], message_types)
        for key in ("event_category", "event_kind"):
            to_dispatch = to_dispatch and is_valid_type(msg["message"].get(key),
                                                        dispatcher.get(key.upper()))
        if to_dispatch:
            for task_name, task_config in dispatcher.get("TASK_HANDLERS", {}).items():
                if not task_config:
                    raise InvalidDispatcherConfigException("No config for %s handler tasks" % task_name)
                task = getattr(sys.modules[__name__], task_name, None)
                if not task:
                    raise UndefinedTaskHandlerException("No class found for %s" % task_name)
                current_app.logger.debug("Sending task %s to celery broker %s" % (task_name, msg))
                task.delay(task_config, msg)
        else:
            current_app.logger.warn("No dispatcher for msg %s" % msg)

@celery.task
def logging_dispatcher(config, msg):
    msg_id = msg.get("message_id", msg.get("id"))
    task_logger.debug("Receive log dispatch task for msg ID: %s" % msg_id)
    target_log_file = config.get('target_log_file')
    if not target_log_file:
        raise InvalidDispatcherConfigException("Missing target_log_file for log dispatch")
    try:
        with open(target_log_file, 'a') as fd:
            fd.write(json.dumps(msg))
    except IOError as exc:
        raise DispatcherException(str(exc))

@celery.task
def http_dispatcher(config, msg):
    msg_id = msg.get("message_id", msg.get("id"))
    task_logger.debug("Receive log dispatch task for msg ID: %s" % msg_id)
    endpoint = config.get("endpoint")
    headers = config.get("headers")
    if not (endpoint and headers):
        raise InvalidDispatcherConfigException("Missing either endpoint or headers config for http dispatch")
    try:
        requests.post(endpoint, headers=headers, json=msg)
    except requests.exceptions.RequestException as exc:
        raise DispatcherException(str(exc))
