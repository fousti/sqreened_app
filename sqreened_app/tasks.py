import sys
import json

from flask import current_app
from celery.utils.log import get_task_logger

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
    excs = []
    for dispatcher in dispatchers:
        message_types = dispatcher.get("MESSAGE_TYPES", [])
        to_dispatch = is_valid_type(msg["message_type"], message_types)
        for key in ("event_type", "event_category", "event_kind"):
            to_dispatch &= is_valid_type(msg["message"].get(key),
                                         dispatcher.get(key.upper()))
        if to_dispatch:
            for task_name, task_config in dispatcher.get("TASK_HANDLERS", {}).items():
                if not task_config:
                    raise InvalidDispatcherConfigException("No config for %s handler tasks" % task_name)
                task = getattr(sys.modules[__name__], task_name, None)
                if not task:
                    raise UndefinedTaskHandlerException("No class found for %s" % task_name)
                current_app.logger.info("Sending task to celery broker %s" % msg)
                task.delay(task_config, msg["message"])
        else:
            current_app.logger.warn("Not dispatcher for msg %s" %s)

@celery.task
def logging_dispatcher(config, msg):
    task_logger.info("Receive log dispatch task with config : %s" % config)
    target_log_file = config.get('target_log_file')
    if not target_log_file:
        raise InvalidDispatcherConfigException("Missing target_log_file")
    try:
        with open(target_log_file, 'a') as fd:
            fd.write(json.dumps(msg))
    except IOError as exc:
        raise DispatcherException(str(exc))
