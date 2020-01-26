import json


def test_homepage(test_client, request_sig):
    body = {'data': 'test'}
    resp = test_client.post("/webhooks/",
                            json=body,
                            headers={"X-Sqreen-Integrity": request_sig(json.dumps(body))})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "data" in data
    assert data["data"] == "Welcome to Sqreened App!"


