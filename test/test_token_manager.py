import time
from authnid.token import TokenManager
from test.helpers import is_token

token_maker = TokenManager('some-secret')

def test_can_build_token():
    token = token_maker.token()
    assert is_token(token)

def test_can_validate_token():
    token = token_maker.token()
    assert token_maker.validate(token)
    assert not token_maker.validate('abc123def')

def test_wont_validate_expired_token(monkeypatch):
    now = int(time.time())
    monkeypatch.setattr('authnid.token.TokenManager._timestamp', lambda s: now - 3)
    token = token_maker.token()
    monkeypatch.undo()
    assert not token_maker.validate(token)
