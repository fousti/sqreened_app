import json
import hmac
import hashlib

from flask import Blueprint, jsonify, current_app, request, abort


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
    print("HEX:")
    print(dig)
    if not hmac.compare_digest(dig, sig):
        abort(401)

@hooks_bp.route('/', methods=("POST",))
def webhooks():
    current_app.logger.info('Webhook route')
    return jsonify({"data": "Welcome to Sqreened App!"})
