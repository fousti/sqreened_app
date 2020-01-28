import json

import pytest

from sqreened_app.tasks import trigger_dispatchers
from sqreened_app.default_config import TestingConfig


def test_signature_req_OK(mocker, test_client, request_sig, request_body, celery_app, celery_worker):
    mocked_logging_dispatcher = mocker.patch("sqreened_app.tasks.logging_dispatcher.delay")
    mocked_http_dispatcher = mocker.patch("sqreened_app.tasks.http_dispatcher.delay")
    resp = test_client.post("/webhooks/",
                            data=request_body,
                            headers={"X-Sqreen-Integrity": request_sig(request_body),
                                     "Content-type": "application/json"})
    assert resp.status_code == 200
    assert mocked_http_dispatcher.call_count == 1
    assert mocked_logging_dispatcher.call_count == 2

def test_signature_req_NOK(test_client, request_sig, request_body):
    resp = test_client.post("/webhooks/",
                            data=request_body,
                            headers={"X-Sqreen-Integrity": b"1234355"})
    assert resp.status_code == 401

