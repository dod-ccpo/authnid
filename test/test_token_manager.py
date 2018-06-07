from authnid.token import TokenManager
from test.helpers import is_token

token_maker = TokenManager('some-secret')

def test_can_build_jwt():
    token = token_maker.token()
    assert is_token(token)

def test_can_validate_jwt():
    token = token_maker.token()
    assert token_maker.validate(token)
    assert not token_maker.validate('abc.123.def')
    parts = token.split('.')
    bad_token = '.'.join([parts[0], parts[1], 'somethingelseentirely'])
    assert not token_maker.validate(bad_token)
