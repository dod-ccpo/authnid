import json

def test_validate_valid_token(app, client):
    token = app.token_manager.token('1234')
    data = json.dumps({"token": token})
    res = client.post(
        "/api/v1/validate", content_type="application/json", data=data
    )
    resp_json = res.get_json()
    assert resp_json['status'] == 'success'
    assert res.status_code == 200

def test_validate_invalid_token(app, client):
    token = 'abc123'
    data = json.dumps({"token": token})
    res = client.post(
        "/api/v1/validate", content_type="application/json", data=data
    )
    resp_json = res.get_json()
    assert resp_json['status'] == 'error'
    assert res.status_code == 401
