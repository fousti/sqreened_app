import json
import hmac
import hashlib

from flask import Blueprint, jsonify, current_app, request, abort

from sqreened_app import tasks
from sqreened_app.tasks import trigger_dispatchers


hooks_bp = Blueprint("webhooks", __name__, url_prefix="/webhooks")

@hooks_bp.before_request
def check_signature():
    sig = request.headers.get("X-Sqreen-Integrity")
    if sig is None:
        abort(401)

    secret = current_app.config["SQREEN_TOKEN"]
    body = request.data
    hasher = hmac.new(bytes(secret.encode()), request.data, hashlib.sha256)
    dig = hasher.hexdigest()
    if not hmac.compare_digest(dig, sig):
        abort(401)

    current_app.logger.debug("VALID SIG")

@hooks_bp.route('/', methods=("POST",))
def webhooks():
    dispatchers = current_app.config["DISPATCHERS"]
    body = request.get_json()
    if isinstance(body, list):
        for msg in body:
            current_app.logger.debug("Trigger dispatch for msg %s" % msg)
            trigger_dispatchers(msg, dispatchers)
    else:
        current_app.logger.debug("Trigger dispatch for msg %s" % body)
        trigger_dispatchers(body, dispatchers)
    return 'Ok', 200
