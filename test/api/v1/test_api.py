import json

def test_validate_valid_token(monkeypatch, app, client):
    monkeypatch.setattr('authnid.user_repo.UserRepo.get_user', lambda s, **kwargs: {})
    token = app.token_manager.token('1234')
    data = json.dumps({"token": token})
    res = client.post(
        "/api/v1/validate", content_type="application/json", data=data
    )
    resp_json = res.get_json()
    assert resp_json['status'] == 'success'
    assert res.status_code == 200

def test_validate_returns_user(user_repo, dod_user, app, client):
    uuid = user_repo.add_user(**dod_user)
    token = app.token_manager.token(uuid)
    data = json.dumps({"token": token})
    res = client.post(
        "/api/v1/validate", content_type="application/json", data=data
    )
    resp_json = res.get_json()
    assert resp_json['user']['id'] == uuid

def test_validate_invalid_token(app, client):
    token = 'abc123'
    data = json.dumps({"token": token})
    res = client.post(
        "/api/v1/validate", content_type="application/json", data=data
    )
    resp_json = res.get_json()
    assert resp_json['status'] == 'error'
    assert res.status_code == 401
