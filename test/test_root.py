import pytest
from unittest.mock import MagicMock
from test.helpers import DOD_SDN, DOD_SDN_INFO

@pytest.fixture
def dod_user():
    user_info = DOD_SDN_INFO.copy()
    return user_info

def test_adds_new_user_to_the_database(monkeypatch, user_repo, client, dod_user):
    magic = MagicMock(return_value='123')
    monkeypatch.setattr('authnid.root.is_valid_certificate', lambda r: True)
    monkeypatch.setattr('authnid.user_repo.UserRepo.add_user', magic)
    resp = client.get('/', environ_base={
        'HTTP_X_SSL_CLIENT_VERIFY': 'SUCCESS',
        'HTTP_X_SSL_CLIENT_S_DN': DOD_SDN
    })
    magic.assert_called_with(**dod_user)


def test_does_not_add_existing_user(monkeypatch, user_repo, client, dod_user):
    monkeypatch.setattr('authnid.root.is_valid_certificate', lambda r: True)
    user_repo.add_user(**dod_user)
    user_count = user_repo.count()
    resp = client.get('/', environ_base={
        'HTTP_X_SSL_CLIENT_VERIFY': 'SUCCESS',
        'HTTP_X_SSL_CLIENT_S_DN': DOD_SDN
    })
    assert user_repo.count() == user_count
