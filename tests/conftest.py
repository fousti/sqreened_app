import hmac
import hashlib
import json

import pytest

from sqreened_app import create_app
from sqreened_app.default_config import TestingConfig

@pytest.fixture(scope="module")
def test_client():
    app = create_app(config_name="testing")
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()

@pytest.fixture(scope="function")
def request_sig(test_client):
    def make_req_sig(data):
        sig = hmac.new(bytes(TestingConfig.SQREEN_TOKEN.encode()),
                       msg=data,
                       digestmod=hashlib.sha256).hexdigest()
        return sig
    return make_req_sig

@pytest.fixture(scope="function")
def request_body():
    with open("tests/data/notifications.json", "rb") as fd:
        data = fd.read()
        return data

@pytest.fixture(scope="session")
def celery_config():
    return {"broker_url": "memory://"}
