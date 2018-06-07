from authnid.jwt import JWTManager
from test.helpers import is_jwt

jwt_maker = JWTManager('some-secret')

def test_can_build_jwt():
    token = jwt_maker.token()
    assert is_jwt(token)

def test_can_validate_jwt():
    token = jwt_maker.token()
    assert jwt_maker.validate(token)
    assert not jwt_maker.validate('abc.123.def')
    parts = token.split('.')
    bad_token = '.'.join([parts[0], parts[1], 'somethingelseentirely'])
    assert not jwt_maker.validate(bad_token)
