import json

from flask import Blueprint, jsonify, current_app

hooks_bp = Blueprint("webhooks", __name__, url_prefix="/webhooks")

@hooks_bp.route('/')
def index():
    current_app.logger.info('Index route')
    return jsonify({"data": "Hello world!"})
