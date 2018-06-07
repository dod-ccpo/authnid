from authnid.jwt import JWTManager
from test.helpers import is_jwt

def test_can_build_jwt():
    jwt_maker = JWTManager('some-secret')
    token = jwt_maker.token()
    assert is_jwt(token)
