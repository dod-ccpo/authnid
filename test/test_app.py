import re
from unittest.mock import MagicMock
import pytest
import requests
from test.helpers import is_token, relative_dir, DOD_SDN, DOD_SDN_INFO
from authnid.make_app import make_config
from authnid.user_repo import UserRepo
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

@pytest.fixture
def dod_user():
    user_info = DOD_SDN_INFO.copy()
    user_info['email'] = STUB_EMAIL
    return user_info

def test_adds_new_user_to_the_database(monkeypatch, user_repo, client, dod_user):
    added_user = {}
    magic = MagicMock(return_value='123')
    monkeypatch.setattr('authnid.root.is_valid_certificate', lambda r: True)
    monkeypatch.setattr('authnid.user_repo.UserRepo.add_user', magic)
    resp = client.get('/', environ_base={
        'HTTP_X_SSL_CLIENT_VERIFY': 'SUCCESS',
        'HTTP_X_SSL_CLIENT_S_DN': DOD_SDN
    })
    magic.assert_called_with(**dod_user)


def test_does_not_add_existing_user(monkeypatch, user_repo, client):
    monkeypatch.setattr('authnid.root.is_valid_certificate', lambda r: True)
    user_info = DOD_SDN_INFO.copy()
    user_info['email'] = STUB_EMAIL
    user_repo.add_user(**user_info)
    user_count = user_repo.count()
    resp = client.get('/', environ_base={
        'HTTP_X_SSL_CLIENT_VERIFY': 'SUCCESS',
        'HTTP_X_SSL_CLIENT_S_DN': DOD_SDN
    })
    assert user_repo.count() == user_count

