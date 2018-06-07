def test_validate(app, client):
    res = client.get('/api/v1/validate')
    assert res.status_code == 200
