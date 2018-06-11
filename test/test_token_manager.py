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
