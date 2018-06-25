import pytest
import requests
import re
from test.helpers import is_token, relative_dir, DOD_SDN, DOD_SDN_INFO
from authnid.root import STUB_EMAIL


def test_log_in_with_cac(request_client):
    r = request_client.login()
    assert r.status_code == 302
    assert re.search("bearer-token", r.headers["Location"])


def test_log_in_fails_without_cac(request_client):
    r = request_client.login(certs=())
    assert r.status_code == 403


def test_log_in_with_revoked_certificate(request_client):
    certs=(
        relative_dir("ssl/client-certs/bad-atat.mil.crt"),
        relative_dir("ssl/client-certs/bad-atat.mil.key"),
    )
    r = request_client.login(certs)
    assert r.status_code == 403


def test_log_in_with_cac_redirects_with_token(request_client):
    response = request_client.login()
    location = response.headers['Location']
    token = re.search('bearer-token=([^;]+)', location)[1]
    assert len(location) < 2000 # ensure URL is under a safe limit
    assert response.status_code == 302
    assert is_token(token)


@pytest.fixture(autouse=True)
def reset(app, request_client):
    yield
    app.user_repo.db.connection.rollback()


def test_adds_new_user_to_the_database(monkeypatch, app, client):
    user_count = app.user_repo.count()
    monkeypatch.setattr('authnid.root.is_valid_certificate', lambda r: True)
    resp = client.get('/', environ_base={
        'HTTP_X_SSL_CLIENT_VERIFY': 'SUCCESS',
        'HTTP_X_SSL_CLIENT_S_DN': DOD_SDN
    })
    assert app.user_repo.count() == user_count + 1
    new_user = app.user_repo.all()[-1]
    assert new_user['dod_id'] == DOD_SDN_INFO['dod_id']


def test_does_not_add_existing_user(monkeypatch, app, client):
    monkeypatch.setattr('authnid.root.is_valid_certificate', lambda r: True)
    user_info = DOD_SDN_INFO.copy()
    user_info['email'] = STUB_EMAIL
    app.user_repo.add_user(**user_info)
    user_count = app.user_repo.count()
    resp = client.get('/', environ_base={
        'HTTP_X_SSL_CLIENT_VERIFY': 'SUCCESS',
        'HTTP_X_SSL_CLIENT_S_DN': DOD_SDN
    })
    assert app.user_repo.count() == user_count

