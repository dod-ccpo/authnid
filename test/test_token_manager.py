import time
from authnid.token import TokenManager
from test.helpers import is_token

token_maker = TokenManager('some-secret')

def test_can_build_token():
    token = token_maker.token('1234')
    assert is_token(token)

def test_can_validate_token():
    token = token_maker.token('1234')
    assert token_maker.validate(token)
    assert not token_maker.validate('abc123def')

def test_wont_validate_expired_token(monkeypatch):
    now = int(time.time())
    monkeypatch.setattr('authnid.token.TokenManager._timestamp', lambda s: now - 3)
    token = token_maker.token('1234')
    monkeypatch.undo()
    assert not token_maker.validate(token)

def test_can_parse_token(monkeypatch):
    monkeypatch.setattr('authnid.token.TokenManager._timestamp', lambda s: '5678')
    token = token_maker.token('1234')
    parsed = token_maker.parse(token)
    assert parsed['id'] == '1234'
    assert parsed['timestamp'] == '5678'
