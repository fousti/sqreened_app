import hmac
import hashlib

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
                       msg=bytes(data.encode()),
                       digestmod=hashlib.sha256).hexdigest()
        return sig
    return make_req_sig
