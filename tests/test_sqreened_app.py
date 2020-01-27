import json


def test_signature_req_OK(test_client, request_sig):
    body = {'data': 'test'}
    resp = test_client.post("/webhooks/",
                            json=body,
                            headers={"X-Sqreen-Integrity": request_sig(json.dumps(body))})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "data" in data
    assert data["data"] == "Welcome to Sqreened App!"

def test_signature_req_NOK(test_client, request_sig):
    body = {'data': 'test'}
    resp = test_client.post("/webhooks/",
                            json=body,
                            headers={"X-Sqreen-Integrity": b"1234"})
    assert resp.status_code == 401
